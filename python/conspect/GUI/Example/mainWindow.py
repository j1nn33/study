from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import window_UI

# Созадем класс class exampleWindowClass который наследуется (QWidget) - тот класа который создали в Qt Designer
# наследует window_UI.Ui_example
class exampleWindowClass(QWidget, window_UI.Ui_example):
    def __init__(self):
        super(exampleWindowClass, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('FUCK')
        self.count = 1
        self.additem_btn.clicked.connect(self.addItem)     # завязка метода addItem на нажатие кнопки
        self.name_le.returnPressed.connect(self.addItem)   # завязка метода addItem на нажатие enter

    def addItem(self):
        # метод который получает текст из name_le и выводит
        text = self.name_le.text()
        if text:
            lb = QLabel('%s: %s' %(self.count,text))
            self.items_ly.addWidget(lb)
            self.count += 1


if __name__ == '__main__':

    app = QApplication([])
    w = exampleWindowClass()
    w.show()
    app.exec_()
