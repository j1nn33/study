# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\SOURCE\projectManager\widgets\templateEditor.ui',
# licensing of 'E:\SOURCE\projectManager\widgets\templateEditor.ui' applies.
#
# Created: Wed Oct 24 16:33:59 2018
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_templateEditor(object):
    def setupUi(self, templateEditor):
        templateEditor.setObjectName("templateEditor")
        templateEditor.resize(400, 402)
        self.verticalLayout = QtWidgets.QVBoxLayout(templateEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_btn = QtWidgets.QPushButton(templateEditor)
        self.add_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.add_btn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_btn.setFont(font)
        self.add_btn.setObjectName("add_btn")
        self.horizontalLayout.addWidget(self.add_btn)
        self.remove_btn = QtWidgets.QPushButton(templateEditor)
        self.remove_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.remove_btn.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.remove_btn.setFont(font)
        self.remove_btn.setObjectName("remove_btn")
        self.horizontalLayout.addWidget(self.remove_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tree = QtWidgets.QTreeWidget(templateEditor)
        self.tree.setObjectName("tree")
        self.tree.headerItem().setText(0, "1")
        self.tree.header().setVisible(False)
        self.verticalLayout.addWidget(self.tree)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.save_btn = QtWidgets.QPushButton(templateEditor)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_2.addWidget(self.save_btn)
        self.close_btn = QtWidgets.QPushButton(templateEditor)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout_2.addWidget(self.close_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(templateEditor)
        QtCore.QMetaObject.connectSlotsByName(templateEditor)

    def retranslateUi(self, templateEditor):
        templateEditor.setWindowTitle(QtWidgets.QApplication.translate("templateEditor", "Form", None, -1))
        self.add_btn.setText(QtWidgets.QApplication.translate("templateEditor", "+", None, -1))
        self.remove_btn.setText(QtWidgets.QApplication.translate("templateEditor", "-", None, -1))
        self.save_btn.setText(QtWidgets.QApplication.translate("templateEditor", "Save", None, -1))
        self.close_btn.setText(QtWidgets.QApplication.translate("templateEditor", "Close", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    templateEditor = QtWidgets.QWidget()
    ui = Ui_templateEditor()
    ui.setupUi(templateEditor)
    templateEditor.show()
    sys.exit(app.exec_())

