from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import computeArea_UIs
import math

class computeAreaClass(QMainWindow, computeArea_UIs.Ui_computeArea):
    def __init__(self):
        super(computeAreaClass, self).__init__()
        self.setupUi(self)

        # connects для изменения видимости при переключении переключателя
        self.shape_cbb.currentIndexChanged.connect(self.updateUI)
        self.compute_btn.clicked.connect(self.compute)

        # обновление свойства видимости
        self.updateUI()

    def compute(self):
        """ выбор формулы расчета """
        if self.shape_cbb.currentIndex() == 0:
            self.computeSquare()
        elif self.shape_cbb.currentIndex() == 1:
            self.computeCircle()

    def computeSquare(self):
        w =self.sq_weight_spx.value()
        h = self.sq_heigth_spx.value()
        area = w * h
        self.showResult(area)

    def computeCircle(self):
        r = self.cr_radius_spx.value()
        area =  math.pi * (r **2)
        self.showResult(area)

    def showResult(self, result):
        self.result_lb.setText('RESULT = %s' % result)    # такая форма вывода позволяет передать 1 аргумент

    def updateUI(self):
        """скрывает часть меню"""
        self.sq_gb.setVisible(self.shape_cbb.currentIndex() == 0)
        self.sr_gb.setVisible(self.shape_cbb.currentIndex() == 1)
        self.compute()



if __name__ == '__main__':
    app = QApplication([])
    w = computeAreaClass()
    w.show()
    app.exec_()
