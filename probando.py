import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore

class AnimateBetweenNums(QtCore.QVariantAnimation):
    def __init__(self):
        QtCore.QVariantAnimation.__init__(self)

    def updateCurrentValue(self, value):
        print (value)

class MyProgressbar(QWidget):
    def __init__(self):
        super(MyProgressbar, self).__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(2, 2)
        self.anim = AnimateBetweenNums()
        self.anim.setDuration(1000)
        self.anim.valueChanged.connect(self.updateValue)
        self.value = 50

    def setValue(self, value):
        self.anim.setStartValue(self.value)
        self.anim.setEndValue(value)
        self.anim.start()

    def updateValue(self, value):
        self.value = QtCore.QVariant(int(value))[0]
        self.repaint()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
        till = int(((w / 100.0) * self.value))

        #the bar
        qp.setPen(QColor(255, 255, 255))
        qp.setBrush(QColor(0, 228, 47))
        qp.drawRect(0, 0, till, h)

        #the box
        pen = QPen(QColor(75,80,100), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        hbox = QVBoxLayout()
        self.button10 = QPushButton("10")
        hbox.addWidget(self.button10)
        self.button70 = QPushButton("70")
        hbox.addWidget(self.button70)
        self.progress = MyProgressbar()
        hbox.addWidget(self.progress)
        self.setLayout(hbox)
        self.setGeometry(300, 300, 390, 210)
        self.show()
        self.button10.clicked.connect(self.changeValue10)
        self.button70.clicked.connect(self.changeValue70)

    def changeValue10(self, value):
        self.progress.setValue(10)

    def changeValue70(self, value):
        self.progress.setValue(70)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
