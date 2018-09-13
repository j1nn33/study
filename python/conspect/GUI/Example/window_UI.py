# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\SOURCE\Pycharm\venv\Example1\window.ui',
# licensing of 'E:\SOURCE\Pycharm\venv\Example1\window.ui' applies.
#
# Created: Thu Sep 13 10:17:06 2018
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_example(object):
    def setupUi(self, example):
        example.setObjectName("example")
        example.resize(287, 276)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(example)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.additem_btn = QtWidgets.QPushButton(example)
        self.additem_btn.setObjectName("additem_btn")
        self.verticalLayout_2.addWidget(self.additem_btn)
        self.name_le = QtWidgets.QLineEdit(example)
        self.name_le.setObjectName("name_le")
        self.verticalLayout_2.addWidget(self.name_le)
        self.items_ly = QtWidgets.QVBoxLayout()
        self.items_ly.setObjectName("items_ly")
        self.verticalLayout_2.addLayout(self.items_ly)

        self.retranslateUi(example)
        QtCore.QMetaObject.connectSlotsByName(example)

    def retranslateUi(self, example):
        example.setWindowTitle(QtWidgets.QApplication.translate("example", "Form", None, -1))
        self.additem_btn.setText(QtWidgets.QApplication.translate("example", "Add", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    example = QtWidgets.QWidget()
    ui = Ui_example()
    ui.setupUi(example)
    example.show()
    sys.exit(app.exec_())

