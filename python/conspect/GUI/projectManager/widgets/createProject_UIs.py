# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\SOURCE\projectManager\widgets\newProject.ui',
# licensing of 'E:\SOURCE\projectManager\widgets\newProject.ui' applies.
#
# Created: Mon Oct 22 11:31:26 2018
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_createDialog(object):
    def setupUi(self, createDialog):
        createDialog.setObjectName("createDialog")
        createDialog.resize(396, 311)
        self.verticalLayout = QtWidgets.QVBoxLayout(createDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(createDialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name_lb = QtWidgets.QLineEdit(createDialog)
        self.name_lb.setObjectName("name_lb")
        self.gridLayout.addWidget(self.name_lb, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(createDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comment_te = QtWidgets.QPlainTextEdit(createDialog)
        self.comment_te.setObjectName("comment_te")
        self.gridLayout.addWidget(self.comment_te, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_btn = QtWidgets.QPushButton(createDialog)
        self.create_btn.setObjectName("create_btn")
        self.horizontalLayout.addWidget(self.create_btn)
        self.cancel_btn = QtWidgets.QPushButton(createDialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(createDialog)
        QtCore.QMetaObject.connectSlotsByName(createDialog)

    def retranslateUi(self, createDialog):
        createDialog.setWindowTitle(QtWidgets.QApplication.translate("createDialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("createDialog", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("createDialog", "Comment", None, -1))
        self.create_btn.setText(QtWidgets.QApplication.translate("createDialog", "Create", None, -1))
        self.cancel_btn.setText(QtWidgets.QApplication.translate("createDialog", "Cancel", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    createDialog = QtWidgets.QDialog()
    ui = Ui_createDialog()
    ui.setupUi(createDialog)
    createDialog.show()
    sys.exit(app.exec_())

