import numpy as np
import scipy
import scipy.ndimage as spndmg


class Structure(object):

    '''
    This class describes the behavior of Game Of Life Model. (Model of MVC).

    The Game follows the rules:
    1. Each populated location with one or zero neighbors dies (from loneliness).
    2. Each populated location with four or more neighbors dies (from overpopulation).
    3. Each populated location with two or three neighbors survives.
    4. Each unpopulated location that becomes populated if it has exactly three populated neighbors.
    5. All updates are performed simultaneously in parallel.

    and these are implemented in this class by convolution.

    Here are implemented the methods to get the active cells and to compute the heatmap (cells history).

    Attributes:
        m, n           number of rows and columns.
        cells          of dimension (m,n) contains the current state. From this matrix will be generate the image board.
        heatmap        keep track how long cells live
        history_cells  state at the k-1 iteration
        active_cells   number of active cells
        heatmap_bool   boolean to indicate if to show the heatmap (History mode)
        clear          boolean to indicate to reset the active cells

    '''

    def __init__(self, m=113, n=199):
        self.m = m
        self.n = n
        self.m_default = 57
        self.n_default = 100
        self.heatmap_bool = False
        self.cells = np.zeros((self.m, self.m))
        self.history_cells = np.zeros((self.m, self.n))
        self.heatmap = np.zeros((self.m, self.n))
        self.active_cells = 0
        self.clear = False

    def computeNeighbours(self):
        ''' Compute cells neighbours based on convolution '''
        kernel = np.array([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
        self.cells = self.colorCode(self.cells, type='gray')
        conv_cells = spndmg.filters.convolve(self.cells, kernel, mode='constant', cval=0)
        return conv_cells

    def nextState(self):
        ''' Compute the next state of game '''
        conv_cells = self.computeNeighbours()
        for i in range(self.m):
            for j in range(self.n):
                if conv_cells[i, j] % 2 == 0:
                    if conv_cells[i, j] / 2 == 3:
                        self.setCellActive(i, j)
                    else:
                        self.setCellInactive(i, j)
                elif (conv_cells[i, j] - 1) / 2 == 2 or (conv_cells[i, j] - 1) / 2 == 3:
                    self.setCellActive(i, j)
                else:
                    self.setCellInactive(i, j)
        return self.computeHeatmap()

    def getState(self):
        ''' Return the current state of cells '''
        self.cells = self.nextState()
        return self.cells

    def setState(self, drawnCells):
        ''' Update with the drawn cells  '''
        self.cells = drawnCells

    def setCellActive(self, i, j):
        ''' Set a cell active and count the active cells '''
        self.cells[i, j] = 255
        self.active_cells = np.sum(self.cells == 255)

    def setCellInactive(self, i, j):
        ''' Set a cell inactive '''
        self.cells[i, j] = 0

    def colorCode(self, cells, type):
        ''' For choose the color code, RGB or Gray '''
        if type == 'gray':
            cells[cells > 0] = 1
        elif type == 'rgb':
            cells[cells == 1] = 255
        return cells

    def getSize(self):
        ''' Get the size of matrix that contains the current state '''
        return self.m, self.n

    def getSizeSubmatrix(self):
        ''' Get the size of submatrix to show '''
        return self.m_default, self.n_default

    def getActiveCells(self):
        ''' Get the number of active cells, if clear == True, reset active cells '''
        if self.clear:
            self.active_cells = 0
            self.clear = False
            return self.active_cells
        else:
            return self.active_cells

    def setClear(self):
        ''' Set the boolean clear True '''
        self.clear = True

    def setHeatmap(self):
        ''' Switch the heatmap_bool to activate or deactivate the history mode '''
        if not self.heatmap_bool:
            self.heatmap_bool = True
        else:
            self.heatmap_bool = False

    def computeHeatmap(self):
        ''' Keep in memory the previous state and compute the heatmap.
            The color switch allows to compute, with the product, the cells that keep alive from previous state
            to next state.
        '''
        if self.heatmap_bool:
            self.cells = self.colorCode(self.cells, type='gray')
            self.heatmap = self.cells * self.history_cells
            self.cells = self.colorCode(self.cells, type='rgb')
            self.cells[self.heatmap == 1] = 120
            self.history_cells = self.colorCode(np.copy(self.cells), type='gray')
        return self.cells
