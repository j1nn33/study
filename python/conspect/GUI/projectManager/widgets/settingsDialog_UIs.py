# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\SOURCE\projectManager\widgets\settingsDialog.ui',
# licensing of 'E:\SOURCE\projectManager\widgets\settingsDialog.ui' applies.
#
# Created: Mon Oct 15 15:16:29 2018
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settingDialog(object):
    def setupUi(self, settingDialog):
        settingDialog.setObjectName("settingDialog")
        settingDialog.resize(400, 300)
        self.layoutWidget = QtWidgets.QWidget(settingDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(self.layoutWidget)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(settingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), settingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), settingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settingDialog)

    def retranslateUi(self, settingDialog):
        settingDialog.setWindowTitle(QtWidgets.QApplication.translate("settingDialog", "Dialog", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settingDialog = QtWidgets.QDialog()
    ui = Ui_settingDialog()
    ui.setupUi(settingDialog)
    settingDialog.show()
    sys.exit(app.exec_())

