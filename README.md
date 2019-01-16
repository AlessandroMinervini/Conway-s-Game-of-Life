# Conway’s Game of Life

### What's Game of Life ? 

The Game of Life (an example of a cellular automaton) is played on an infinite two-dimensional rectangular grid of cells. Each cell can be either alive or dead. The status of each cell changes each turn of the game (also called a generation) depending on the statuses of that cell's 8 neighbors. Neighbors of a cell are cells that touch that cell, either horizontal, vertical, or diagonal from that cell.

The initial pattern is the first generation. The second generation evolves from applying the rules simultaneously to every cell on the game board, i.e. births and deaths happen simultaneously. Afterwards, the rules are iteratively applied to create future generations. For each generation of the game, a cell's status in the next generation is determined by a set of rules.

#### Rules

1. Each populated location with one or zero neighbors dies (from loneliness).
2. Each populated location with four or more neighbors dies (from overpopulation).
3. Each populated location with two or three neighbors survives.
4. Each unpopulated location that becomes populated if it has exactly three populated neighbors.
5. All updates are performed simultaneously in parallel.

### Implementation

The game is implemented in Python language, and the GUI framework chosen is PyQt.
The implementation is based on the MVC pattern (Model view controller).
The next state of the game works by scipy convolution.

#### Model

The model is described in Structure class. 
This class provides the behavior of 'Game Of Life', manages the data, and implements the game rules.
Here is compute the next state, based on convolution and the heatmap (to keep in memory cells history).

#### Controller

This class provides the methods to allow the dialog between view and model.
Are implemented methods to manage input events, to send the new cells drawn to model,
to get the next state from model, to update the cells matrix with next state and create the image from it.
Moreover are implemented the controls play/pause, clear, zoom out, set frame rate, set heatmap (cells history), set generations, set active cells.

#### View

This class provides to display the current state of game and to setting the application GUI. The interaction with users is manage by this class.
The section of GUI code is was created with use of Qt Designer.

### Features
- Play/Pause
- Clear
- History mode (heatmap)
- Variable frame rate
- Drawing/editing the state (in play and pause mode)
- Zoom out
- Statistic of active cells and generations

### Requirements

- Numpy
- Scipy 
- PyQt5
- qdarkstyle (to display the dark window)

### How to play?
To start playing, first of all you have to draw some cells, and draw your initial pattern!
Then play start and watch the evolution of cells.
You can pause the game, or if you try a new pattern, clear the board by pressing the clear button. If you draw a cell in a wrong place, delete it with the left button!
During the play mode, is possible change the frame rate, zoom out the board and switch to the History mode.

#### Watch a simple game play!
<p align="center">
  <img width="700" height="544" src="https://github.com/AlessandroMinervini/Conway-s-Game-of-Life/blob/master/images/gameplay2.gif">
</p>
![alt text]()

#### Now draw and have fun!
Below i want to give you some suggestions to try to draw your pattern!
<p align="center">
  <img width="600" height="466" src="https://github.com/AlessandroMinervini/Conway-s-Game-of-Life/blob/master/images/example.png">
</p>
<p align="center">
  <img width="600" height="594" src="https://github.com/AlessandroMinervini/Conway-s-Game-of-Life/blob/master/images/example2.png">
</p>
<p align="center">
  <img width="600" height="393" src="https://github.com/AlessandroMinervini/Conway-s-Game-of-Life/blob/master/images/example3.png">
</p>

