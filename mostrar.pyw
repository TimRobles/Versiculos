import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mostrar.ui",self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()
        self.textEdit.setStyleSheet("background-color: rgba(0, 120, 185, 255); color: rgba(0, 120, 185, 255)")
        anchoMax=500
        altoMax=500
        self.textEdit.setMaximumSize(anchoMax, altoMax)
        self.textEdit.setMinimumSize(anchoMax, altoMax)
        self.widget.setMaximumSize(anchoMax, 300)
        self.widget.setMinimumSize(anchoMax, 300)

app=QApplication(sys.argv)
_main=Principal()
_main.show()
app.exec_()
