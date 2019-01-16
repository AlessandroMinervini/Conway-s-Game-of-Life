from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import QSize, pyqtSignal, QTimer, Qt
import controller, structure
import sys
import qdarkstyle


class View(QWidget):

    '''
    This class provides to display the current state of game and to setting the application GUI.

    The interaction with users is manage by this class.

    The section of GUI code is was created with use of Qt Designer.

    Attributes:
        control     reference to an object of class controller (controller MVC)
        timer       a Qtimer used to start generations
    '''

    def __init__(self, structure, parent=None):
        QWidget.__init__(self, parent)
        self.control = controller.Controller(structure)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.control)
        timer = QTimer()
        timer.timeout.connect(self.control.generation)
        timer.start(1000)
        self.setupUi(self)

    def setupUi(self, Form):
        ''' Set up the elements that shape the GUI.
            Component used:
            input widget as Qslider
            buttons as Qcheckbox, QPushButton
            containers QGroupBox
            display widgets as Qlabel
        '''
        Form.setObjectName("Form")
        Form.resize(801, 600)
        self.info_generation_Timer = QTimer()
        self.info_alive_Timer = QTimer()
        self.controls_box = QtWidgets.QGroupBox(Form)
        self.controls_box.setGeometry(QtCore.QRect(20, 500, 761, 81))
        self.controls_box.setObjectName("controls_box")
        self.Play = QtWidgets.QPushButton(self.controls_box)
        self.Play.setGeometry(QtCore.QRect(30, 30, 141, 41))
        self.Play.setObjectName("Play")
        self.Play.clicked.connect(self.play)
        self.Clear = QtWidgets.QPushButton(self.controls_box)
        self.Clear.setGeometry(QtCore.QRect(190, 30, 71, 41))
        self.Clear.setObjectName("Clear")
        self.Clear.clicked.connect(self.clear)
        self.Heatmap = QtWidgets.QCheckBox(self.controls_box)
        self.Heatmap.setGeometry(QtCore.QRect(470, 40, 91, 22))
        self.Heatmap.setObjectName("Heatmap")
        self.Heatmap.clicked.connect(self.checkHeatmap)
        self.zoom = QtWidgets.QSlider(self.controls_box)
        self.zoom.setGeometry(QtCore.QRect(600, 40, 121, 22))
        self.zoom.setOrientation(QtCore.Qt.Horizontal)
        self.zoom.setObjectName("zoom")
        self.zoom.setValue(0)
        self.zoom.valueChanged.connect(self.setZoom)
        self.label_zoom = QtWidgets.QLabel(self.controls_box)
        self.label_zoom.setGeometry(QtCore.QRect(640, 30, 71, 16))
        self.label_zoom.setObjectName("label_zoom")
        self.info_box = QtWidgets.QGroupBox(Form)
        self.info_box.setGeometry(QtCore.QRect(20, 0, 761, 61))
        self.info_box.setObjectName("info_box")
        self.framerate = QtWidgets.QSlider(self.info_box)
        self.framerate.setGeometry(QtCore.QRect(130, 30, 121, 22))
        self.framerate.setOrientation(QtCore.Qt.Horizontal)
        self.framerate.setObjectName("framerate")
        self.framerate.valueChanged.connect(self.setFramerate)
        self.Framerate_label = QtWidgets.QLabel(self.info_box)
        self.Framerate_label.setGeometry(QtCore.QRect(40, 30, 78, 20))
        self.Framerate_label.setObjectName("Framerate_label")
        self.activeCells_label = QtWidgets.QLabel(self.info_box)
        self.activeCells_label.setGeometry(QtCore.QRect(390, 30, 81, 22))
        self.activeCells_label.setObjectName("activeCells_label")
        self.generations_label = QtWidgets.QLabel(self.info_box)
        self.generations_label.setGeometry(QtCore.QRect(580, 30, 81, 22))
        self.generations_label.setObjectName("generations_label")
        self.n_active_cells = QtWidgets.QLabel(self.info_box)
        self.n_active_cells.setGeometry(QtCore.QRect(480, 30, 60, 22))
        self.n_active_cells.setObjectName("n_active_cells")
        self.info_alive_Timer.timeout.connect(self.setActiveCells)
        self.n_generations = QtWidgets.QLabel(self.info_box)
        self.n_generations.setGeometry(QtCore.QRect(670, 30, 60, 22))
        self.n_generations.setObjectName("n_generations")
        self.info_generation_Timer.timeout.connect(self.setGenerations)
        self.info_generation_Timer.start(1000)
        self.info_alive_Timer.start(1000)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        ''' Handle the translation of the string properties of the form '''
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Game of Life"))
        self.controls_box.setTitle(_translate("Form", "Controls"))
        self.Play.setText(_translate("Form", "Play"))
        self.Clear.setText(_translate("Form", "Clear"))
        self.Heatmap.setText(_translate("Form", "History"))
        self.label_zoom.setText(_translate("Form", "Zoom Out"))
        self.info_box.setTitle(_translate("Form", "Info"))
        self.Framerate_label.setText(_translate("Form", "Frame Rate"))
        self.activeCells_label.setText(_translate("Form", "Active Cells:"))
        self.generations_label.setText(_translate("Form", "Generations:"))
        self.n_active_cells.setText(_translate("Form", "0"))
        self.n_generations.setText(_translate("Form", "0"))

    def play(self):
        ''' Slot for the pushbutton Play/Pause '''
        self.control.play()
        if self.Play.text() == 'Play':
            self.Play.setText('Pause')
        else:
            self.Play.setText('Play')

    def clear(self):
        ''' Slot for the pushbutton Clear'''
        self.control.clear()
        self.Play.setText('Play')
        self.n_active_cells.setText('0')
        self.n_generations.setText('0')

    def checkHeatmap(self):
        ''' Slot for the checkbutton Heatmap'''
        if self.Heatmap.isChecked():
            self.control.setHeatmap()
        else:
            self.control.setHeatmap()

    def setFramerate(self):
        ''' Slot for frame rate slider. Slider values are in range 0, 99 '''
        self.control.setFramerate(100 - self.framerate.value())

    def setGenerations(self):
        ''' Slot for generation statistic '''
        gen_str = str(self.control.getCountGenerations())
        self.n_generations.setText(gen_str)

    def setActiveCells(self):
        ''' Slot for number of active cells statistic '''
        alive_str = str(self.control.getActiveCells())
        self.n_active_cells.setText(alive_str)

    def setZoom(self):
        ''' Slot for zoom slider. Slider values are in range 0, 99'''
        self.control.zoomImage(self.zoom.value())

''' Launch application '''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    s = structure.Structure()
    w = View(s)
    w.show()
    sys.exit(app.exec_())