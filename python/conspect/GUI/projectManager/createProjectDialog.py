from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from widgets import createProject_UIs as ui
from widgets import projectListWidget
#from widgets import settingsdialog
import createProjectDialog

class projectManagerClass(QDialog, ui.Ui_createDialog):
    def __init__(self, parent):
        super(projectManagerClass,self).__init__(parent)
        self.setupUi(self)

        # connect
        self.create_btn.clicked.connect(self.doCreate)
        self.cancel_btn.clicked.connect(self.reject)

    def doCreate(self):
        """ запрещает создание проекта без имени """
        if self.name_lb.text():
            self.accept()

    def getDialogData(self):
        return dict(
            name = self.name_lb.text(),
            comment = self.comment_te.toPlainText()
        )




if __name__ == '__main__':
    app = QApplication([])
    w = projectManagerClass()
    w.show()
    app.exec_()
