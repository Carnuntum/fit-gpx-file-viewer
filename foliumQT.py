import io
import sys

import folium

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtGui import QIcon
from gpxplotter import read_gpx_file, create_folium_map, add_segment_to_map, add_all_tiles
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import btnMethods

#import sklearn.neighbors.typedefs
#import sklearn.neighbors.quad_tree
#import sklearn.tree
#import sklearn.tree._utils

class FitReader(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr("FIT File Vizualizer"))
        self.setGeometry(200, 200, 1280, 720)
        self.setWindowIcon(QIcon('mountain.png')) 
        self.buttonUI()

    def loadFile(self):
        return(btnMethods.loadFile(self))

    def changeToMap(self):
        return(btnMethods.changeToMap(self))

    def changeToHr(self):
        return(btnMethods.changeToHr(self))

    def changeToEle(self):
        return(btnMethods.changeToEle(self))

    def buttonUI(self):
        btnOpen = QtWidgets.QPushButton("Open")
        btnMap = QtWidgets.QPushButton("Map")
        btnHr = QtWidgets.QPushButton("Hear Rate")
        btnElev = QtWidgets.QPushButton("Elevation")

        btnOpen.setFixedSize(120, 50)
        btnOpen.clicked.connect(self.loadFile)

        btnMap.setFixedSize(120, 50)
        btnMap.clicked.connect(self.changeToMap)

        btnHr.setFixedSize(120, 50)
        btnHr.clicked.connect(self.changeToHr)

        btnElev.setFixedSize(120, 50)
        btnElev.clicked.connect(self.changeToEle)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(0,0,0,0)

        self.hr = QtWidgets.QWidget()
        self.ele = QtWidgets.QWidget()
        self.hearRateLay = QtWidgets.QVBoxLayout(self.hr)
        self.elevationLay = QtWidgets.QVBoxLayout(self.ele)

        self.hrFigure = plt.figure()
        self.eleFigure = plt.figure()

        self.hrCanvas = FigureCanvas(self.hrFigure)
        self.eleCanvas = FigureCanvas(self.eleFigure)
        self.hrToolbar = NavigationToolbar(self.hrCanvas, self)
        self.eleToolbar = NavigationToolbar(self.eleCanvas, self)

        self.hearRateLay.addWidget(self.hrCanvas)
        self.hearRateLay.addWidget(self.hrToolbar)
        self.elevationLay.addWidget(self.eleCanvas)
        self.elevationLay.addWidget(self.eleToolbar)
        

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout(central_widget)

        btnContainer = QtWidgets.QWidget()
        btnContainerLay = QtWidgets.QVBoxLayout(btnContainer)
        btnContainerLay.setSpacing(20)
        btnContainerLay.addWidget(btnOpen)
        btnContainerLay.addWidget(btnMap)
        btnContainerLay.addWidget(btnHr)
        btnContainerLay.addWidget(btnElev)
        btnContainerLay.addStretch()

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.view)
        self.stack.addWidget(self.hr)
        self.stack.addWidget(self.ele)

        layout.addWidget(btnContainer)
        layout.addWidget(self.stack)

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    app = FitReader()
    app.show()
    sys.exit(App.exec())
    