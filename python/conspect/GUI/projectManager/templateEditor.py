from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from widgets import templateEditor_UIs as ui
import os, json


templateFile =os.path.join(os.path.dirname(__file__), 'template.json')

class templateEditorClass(QWidget, ui.Ui_templateEditor):
    def __init__(self):
        super(templateEditorClass, self).__init__()
        self.setupUi(self)
        # ui
        # включаем Drug'n'drop перемещение врутри виджета
        self.tree.setDragDropMode(QAbstractItemView.InternalMove)
        # метод выделения ctrl or shift
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # connects связываем кнопки с функциями
        self.add_btn.clicked.connect(self.addItem)
        self.remove_btn.clicked.connect(self.removeItem)
        self.save_btn.clicked.connect(self.saveTemplate)
        self.close_btn.clicked.connect(self.close)
        # start
        self.loadTemplate()

    def addItem(self, name = 'Folder', parent = None):
        if not parent:
            parent = self.tree.invisibleRootItem()
        item = QTreeWidgetItem()
        # переименование по двойному клику перезаписываем флаги (их надо перезаписать все)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
        item.setText(0, name)
        parent.addChild(item)
        item.setExpanded(1)
        return item

    def removeItem(self):
        """ удаление выдеелных item"""
        items = self.tree.selectedItems()
        for i in items:
            (i.parent() or self.tree.invisibleRootItem()).takeChild(self.tree.indexFromItem(i).row())

    def saveTemplate(self):
        template = self.getStructure()
        #print(template)
        with open(templateFile, 'w') as f:
            json.dump(template, f, indent = 4)
        self.close()

    def getStructure(self, parent = None):
        level = []
        # пробегаемся по списку рекурсивно для обхода всех вложений
        if not parent:
            parent = self.tree.invisibleRootItem()
        for i in range (parent.childCount()):
            ch = parent.child(i)
            content = self.getStructure(ch)
            level.append({
                'name':ch.text(0),
                'content':content})
        return level

    def loadTemplate(self):
        if os.path.exists(templateFile):
            with open(templateFile) as f:
                template = json.load(f)
                self.restoreStructure(template)

    def restoreStructure(self, data, parent=None):
        if not parent:
            parent = self.tree.invisibleRootItem()
        for i in data:
            item = self.addItem(i['name'], parent)
            self.restoreStructure(i['content'], item)






if __name__ == '__main__':
    app = QApplication([])
    w = templateEditorClass()
    w.show()
    app.exec_()
