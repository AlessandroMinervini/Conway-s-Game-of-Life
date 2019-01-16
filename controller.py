import toQimage
import numpy as np
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QSize, QTimer, Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

''' Constants to align the coordinates to the label '''
margin_y = 65
margin_x = 30


class Controller(QWidget):

    '''

    This class provides the methods to allow the dialog between view and model.

    Are implemented methods to manage input events, to send the new cells drawn to model,
    to get the next state from model, to update the cells matrix with next state and create the image from it.

    Moreover are implemented the controls play/pause, clear, zoom out, set frame rate, set heatmap (cells history),
    set generations, set active cells.

    Attributes:
        structure           reference to an object of class structure (model MVC)
        m, n                size of cells matrix
        m_pixmap            height of image created from cells matrix
        n_pixmap            width of image created from cells matrix
        path                path drawn
        coords              cells matrix (or coordinates matrix)
        Qim                 image created from cells matrix
        label               label to set image of current state
        pixmap              representation of current state as image
        frame rate          frame rate value
        count_generations   number of generations
        zoom                zoom value
        is_playing          boolean to indicate if the game is running
        m_start             start row index of submatrix to show
        m_end               end row index of submatrix to show
        n_start             start column index of submatrix to show
        n_end               end column index of submatrix to show
        m_zoom              number of rows of submatrix
        n_zoom              number of column of submatrix
    '''

    def __init__(self, structure, m_pixmap=400, n_pixmap=700):
        QWidget.__init__(self)
        self.structure = structure
        self.m, self.n = self.structure.getSize()
        self.m_zoom, self.n_zoom = self.structure.getSizeSubmatrix()
        self.m_pixmap = m_pixmap
        self.n_pixmap = n_pixmap
        self.path = QPainterPath()
        self.coords = np.zeros((self.m, self.n))
        self.Qim = toQimage.toQImage(np.require(self.coords, np.uint8, 'C'))
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.Qim)
        self.pixmap = self.pixmap.scaled(self.n_pixmap, self.m_pixmap)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(QRect(margin_x, margin_y, self.n_pixmap, self.m_pixmap))
        self.label.show()
        self.framerate = 30
        self.count_generations = 0
        self.zoom = 0
        self.is_playing = False
        self.m_default, self.n_default = self.structure.getSizeSubmatrix()
        self.n_start = int((self.n / 2) - (self.n_default / 2))
        self.n_end = self.n_zoom + self.n_start
        self.m_start = int((self.m / 2) - (self.m_default / 2))
        self.m_end = self.m_zoom + self.m_start

    def mousePressEvent(self, event):
        ''' Compute the mouse click coordinates. Draw or delete cells and update the current state '''
        self.path.moveTo(event.pos())
        m = (int(self.path.currentPosition().y())) - margin_y
        n = (int(self.path.currentPosition().x())) - margin_x
        if event.button() == Qt.LeftButton:
            self.setCoords(m, n)
        elif event.button() == Qt.RightButton:
            self.delCoords(m, n)
        self.update_view(self.m_start, self.m_end, self.n_start, self.n_end)

    def mouseMoveEvent(self, event):
        ''' Compute the mouse path coordinates. Draw the cells and update the current state '''
        self.path.lineTo(event.pos())
        m = (int(self.path.currentPosition().y())) - margin_y
        n = (int(self.path.currentPosition().x())) - margin_x
        self.setCoords(m, n)
        self.update_view(self.m_start, self.m_end, self.n_start, self.n_end)

    def sizeHint(self):
        ''' Size of widget '''
        return QSize(self.m_pixmap, self.n_pixmap)

    def getCoords(self):
        ''' Return the cells (or coordinates) matrix '''
        return self.coords

    def setCoords(self, m, n):
        ''' Set active a drawn cell '''
        m, n = self.resize_coords(m, n)
        if 0 <= m < self.m_zoom and 0 <= n < self.n_zoom:
            self.coords[m + self.m_start, n + self.n_start] = 255

    def delCoords(self, m, n):
        ''' Delete a drawn cell '''
        m, n = self.resize_coords(m, n)
        if 0 <= m < self.m_zoom and 0 <= n < self.n_zoom:
            self.coords[m + self.m_start, n + self.n_start] = 0

    def update_view(self, m_start, m_end, n_start, n_end):
        ''' Update the image of current state from submatrix '''
        self.Qim = toQimage.toQImage(np.require(self.coords[self.m_start:self.m_end, self.n_start:self.n_end], np.uint8,'C'))
        self.pixmap = QPixmap(self.Qim)
        self.pixmap = self.pixmap.scaled(self.n_pixmap, self.m_pixmap)
        self.label.setPixmap(self.pixmap)
        self.label.show()

    def generation(self):
        ''' Count number of generations and start the generations of cells every msec = frame rate '''
        if self.is_playing:
            self.count_generations += 1
            self.structure.setState(self.coords)
            self.coords = self.structure.getState()
            self.update_view(self.m_start, self.m_end, self.n_start, self.n_end)
            QTimer.singleShot(self.framerate, self.generation)

    def resize_coords(self, m, n):
        ''' Scale the coordinates to pixmap size '''
        m = int((self.m_zoom * m)/self.m_pixmap)
        n = int((self.n_zoom * n)/self.n_pixmap)
        return m, n

    def getActiveCells(self):
        ''' Get active cells from model '''
        return self.structure.getActiveCells()

    def getCountGenerations(self):
        ''' Get the number of generations'''
        return self.count_generations

    def play(self):
        ''' Play/pause the game '''
        if not self.is_playing:
            self.is_playing = True
            self.generation()
        else:
            self.is_playing = False

    def clear(self):
        ''' Clear the image (game board) and reinitialize the game statistic '''
        self.structure.setClear()
        self.is_playing = False
        self.coords = np.zeros((self.m, self.n))
        self.count_generations = 0
        self.update_view(self.m_start, self.m_end, self.n_start, self.n_end)

    def setHeatmap(self):
        ''' Activate and deactivate the heatmap mode '''
        self.structure.setHeatmap()

    def setFramerate(self, framerate):
        ''' Set the frame rate from frame rate slider value '''
        self.framerate = framerate

    def zoomImage(self, rate):
        '''' Compute the indices of submatrix to show according to a zoom rate, and this make the zoom effect '''
        self.n_zoom = int(self.n_default + rate)
        self.m_zoom = int(self.m_default * (100 + rate)) / 100

        self.n_start = int(self.n_zoom / 2)
        self.n_start = int((self.n / 2) - self.n_start)
        self.n_end = int(self.n - self.n_start)

        self.m_start = int(self.m_zoom / 2)
        self.m_start = int((self.m / 2) - self.m_start)
        self.m_end = int(self.m - self.m_start)

        self.update_view(self.m_start, self.m_end, self.n_start, self.n_end)