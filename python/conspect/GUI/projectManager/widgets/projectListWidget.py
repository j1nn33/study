"""
Создали вручную свой class projectListClass унаследованный от QListWidget

"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import settings, os, createProject

class projectListClass(QListWidget):
    def __init__(self):
        super(projectListClass, self).__init__()

    def updateProjectList(self):
        """ обновляет список проектов"""
        self.clear()
        data = settings.settingsClass().load()
        path = data.get('path')
        if path:
            if os.path.exists(path):
                for f in os.listdir(path):
                    fullPath = os.path.join(path, f)
                    if self.isProject(fullPath):
                        item = self.addProject(f)
                        item.setData(32, fullPath)  # занесение информации о пути расположения проекта

            return True
        else:
            return False

    def isProject(self, path):
        return os.path.exists(os.path.join(path, createProject.projectFile))

    def addProject(self,name):
        item = QListWidgetItem()
        item.setText(name)
        self.addItem(item)
        return item





if __name__ == '__main__':
    app = QApplication([])
    w = projectListClass()
    w.show()
    app.exec_()
