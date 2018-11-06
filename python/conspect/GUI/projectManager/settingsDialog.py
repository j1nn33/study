from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from widgets import settingsDialog_UIs as ui
import settings

class settingDialogClass(QDialog, ui.Ui_settingDialog):
    def __init__(self,parent):
        super(settingDialogClass, self).__init__(parent)
        self.setupUi(self)
        # ui
        self.table.setColumnCount(2)

        # start
        self.fillTable()



    def fillTable(self):
        data = settings.settingsClass().load()
        for key, value in data.items():
            self.addParm(key, value)

    def addParm (self, parm, value):
        # вставляет новый проект в конец таблицы (установка по значению числа строк)
        # значение числа строк на 1 больше так нумерация начинается с 0

        self.table.insertRow(self.table.rowCount())
        item = QTableWidgetItem()
        item.setText(parm)
        self.table.setItem(self.table.rowCount()-1, 0, item)

        item = QTableWidgetItem()
        item.setText(value)
        self.table.setItem(self.table.rowCount() - 1, 1, item)

    def getTableData(self):
        """ get data from table"""
        data = dict()
        for i in range(self.table.rowCount()):
            parm = self.table.item(i,0).text()
            value = self.table.item(i,1).text()
            data[parm] = value
        return data




if __name__ == '__main__':
    app = QApplication([])
    w = settingDialogClass()
    w.show()
    app.exec_()
