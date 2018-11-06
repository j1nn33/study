from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from widgets import projectManager_UIs as ui
from widgets import projectListWidget
#from widgets import settingsdialog
import createProjectDialog, settingsDialog, templateEditor, settings, createProject, webbrowser

class projectManagerClass(QMainWindow, ui.Ui_projectManager):
    def __init__(self):
        super(projectManagerClass,self).__init__()
        self.setupUi(self)

        # widgets
        self.projectList_lwd=projectListWidget.projectListClass()
        self.projectList_ly.addWidget(self.projectList_lwd)

        # connects to buttons
        self.create_btn.clicked.connect(self.createProject)
        self.setting_btn.clicked.connect(self.openSettingDialog)
        self.templateeditor_btn.clicked.connect(self.openTemplateEditorDialog)
        self.projectList_lwd.itemClicked.connect(self.showInfo)
        self.projectList_lwd.itemClicked.connect(self.openProject)

        # start
        # действия которые выполняем перед стартом программы
        # обновляем список
        self.info_lb.setText('')
        self.updateList()


    def updateList(self):
        """Обновляет список проектов"""
        if not self.projectList_lwd.updateProjectList():
            self.create_btn.setEnabled(0)          # кнопка становиться невидимой
        else:
            self.create_btn.setEnabled(1)

    def openSettingDialog(self):
        """открывает диалог настроек"""
        self.dial = settingsDialog.settingDialogClass(self)
        if self.dial.exec_():
            print ('SETTINGS OK')   # отладочная информация
            data = self.dial.getTableData()
            settings.settingsClass().save(data)
        self.updateList()



    def openTemplateEditorDialog(self):
        """открывает диалог настроек"""
        self.dial = templateEditor.templateEditorClass()
        if self.dial.show():
            print('TEMPLATE OK')

    def createProject(self):
        """открывает диалог создания проекта"""
        self.dial = createProjectDialog.projectManagerClass(self)
        #print(self.dial.exec_())    # вывод на экран 1 или 0 при нажатии клавиш
        if self.dial.exec_():
            data =self.dial.getDialogData()
            # print (data)
            createProject.createProject(data)
            self.updateList()



    def showInfo(self, item):
        """открывает окно информации"""
        # print(item.data(32))
        info = createProject.getProjectInfo(item.data(32))
        if info:
            text = '''Name:
%s 
        
Comment:
%s
''' %(info['name'], info['comment'])
        else:
            text = ''
        self.info_lb.setText(text)

    def openProject(self, item):
        """double click on project -> open folder with project"""
        path = item.data(32)
        webbrowser.open(path )









if __name__ == '__main__':
    app = QApplication([])
    w = projectManagerClass()
    w.show()
    app.exec_()
