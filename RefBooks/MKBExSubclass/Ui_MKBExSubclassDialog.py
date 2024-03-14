# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\MKBExSubclassDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MKBExSubclassDialog(object):
    def setupUi(self, MKBExSubclassDialog):
        MKBExSubclassDialog.setObjectName(_fromUtf8("MKBExSubclassDialog"))
        MKBExSubclassDialog.resize(704, 627)
        MKBExSubclassDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(MKBExSubclassDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(MKBExSubclassDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.tblExSubclass = CTableView(MKBExSubclassDialog)
        self.tblExSubclass.setObjectName(_fromUtf8("tblExSubclass"))
        self.vboxlayout.addWidget(self.tblExSubclass)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnAdd = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.hboxlayout.addWidget(self.btnAdd)
        self.btnEdit = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnDel = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnDel.setEnabled(True)
        self.btnDel.setObjectName(_fromUtf8("btnDel"))
        self.hboxlayout.addWidget(self.btnDel)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.gridlayout.addLayout(self.vboxlayout, 0, 0, 1, 1)
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(4)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label_2 = QtGui.QLabel(MKBExSubclassDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout1.addWidget(self.label_2)
        self.tblExSubclass_Item = CTableView(MKBExSubclassDialog)
        self.tblExSubclass_Item.setObjectName(_fromUtf8("tblExSubclass_Item"))
        self.vboxlayout1.addWidget(self.tblExSubclass_Item)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(4)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.btnAdd_Item = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnAdd_Item.setObjectName(_fromUtf8("btnAdd_Item"))
        self.hboxlayout1.addWidget(self.btnAdd_Item)
        self.btnEdit_Item = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnEdit_Item.setObjectName(_fromUtf8("btnEdit_Item"))
        self.hboxlayout1.addWidget(self.btnEdit_Item)
        self.btnDel_Item = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnDel_Item.setObjectName(_fromUtf8("btnDel_Item"))
        self.hboxlayout1.addWidget(self.btnDel_Item)
        self.vboxlayout1.addLayout(self.hboxlayout1)
        self.gridlayout.addLayout(self.vboxlayout1, 0, 1, 1, 1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(4)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem2)
        self.btnClose = QtGui.QPushButton(MKBExSubclassDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout2.addWidget(self.btnClose)
        self.gridlayout.addLayout(self.hboxlayout2, 1, 0, 1, 2)

        self.retranslateUi(MKBExSubclassDialog)
        QtCore.QMetaObject.connectSlotsByName(MKBExSubclassDialog)

    def retranslateUi(self, MKBExSubclassDialog):
        MKBExSubclassDialog.setWindowTitle(_translate("MKBExSubclassDialog", "Расширенная субклассификация МКБ", None))
        self.label.setText(_translate("MKBExSubclassDialog", "Расширенная субклассификация МКБ", None))
        self.btnAdd.setText(_translate("MKBExSubclassDialog", "Вставить F9", None))
        self.btnEdit.setText(_translate("MKBExSubclassDialog", "Правка F4", None))
        self.btnDel.setText(_translate("MKBExSubclassDialog", "Удалить", None))
        self.label_2.setText(_translate("MKBExSubclassDialog", "элемент субклассификации", None))
        self.btnAdd_Item.setText(_translate("MKBExSubclassDialog", "Вставить F9", None))
        self.btnEdit_Item.setText(_translate("MKBExSubclassDialog", "Правка F4", None))
        self.btnDel_Item.setText(_translate("MKBExSubclassDialog", "Удалить", None))
        self.btnClose.setText(_translate("MKBExSubclassDialog", "закрыть", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MKBExSubclassDialog = QtGui.QDialog()
    ui = Ui_MKBExSubclassDialog()
    ui.setupUi(MKBExSubclassDialog)
    MKBExSubclassDialog.show()
    sys.exit(app.exec_())

