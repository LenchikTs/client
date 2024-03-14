# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Events\RelatedActionListPage.ui'
#
# Created: Wed May 22 14:33:33 2019
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_RelatedActionListPage(object):
    def setupUi(self, RelatedActionListPage):
        RelatedActionListPage.setObjectName(_fromUtf8("RelatedActionListPage"))
        RelatedActionListPage.resize(522, 384)
        self.verticalLayout = QtGui.QVBoxLayout(RelatedActionListPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkCurrentEvent = QtGui.QCheckBox(RelatedActionListPage)
        self.chkCurrentEvent.setChecked(True)
        self.chkCurrentEvent.setObjectName(_fromUtf8("chkCurrentEvent"))
        self.verticalLayout.addWidget(self.chkCurrentEvent)
        self.chkCurrentDate = QtGui.QCheckBox(RelatedActionListPage)
        self.chkCurrentDate.setChecked(True)
        self.chkCurrentDate.setObjectName(_fromUtf8("chkCurrentDate"))
        self.verticalLayout.addWidget(self.chkCurrentDate)
        self.tblRelatedActionList = CTableView(RelatedActionListPage)
        self.tblRelatedActionList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblRelatedActionList.setObjectName(_fromUtf8("tblRelatedActionList"))
        self.verticalLayout.addWidget(self.tblRelatedActionList)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOpen = QtGui.QPushButton(RelatedActionListPage)
        self.btnOpen.setObjectName(_fromUtf8("btnOpen"))
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnAdd = QtGui.QPushButton(RelatedActionListPage)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDel = QtGui.QPushButton(RelatedActionListPage)
        self.btnDel.setObjectName(_fromUtf8("btnDel"))
        self.horizontalLayout.addWidget(self.btnDel)
        self.btnClose = QtGui.QPushButton(RelatedActionListPage)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RelatedActionListPage)
        QtCore.QMetaObject.connectSlotsByName(RelatedActionListPage)

    def retranslateUi(self, RelatedActionListPage):
        RelatedActionListPage.setWindowTitle(_translate("RelatedActionListPage", "Form", None))
        self.chkCurrentEvent.setText(_translate("RelatedActionListPage", "прикрепленные к данной истории", None))
        self.chkCurrentDate.setText(_translate("RelatedActionListPage", "только за текущую дату", None))
        self.btnOpen.setText(_translate("RelatedActionListPage", "Открыть", None))
        self.btnAdd.setText(_translate("RelatedActionListPage", "Добавить в событие", None))
        self.btnDel.setText(_translate("RelatedActionListPage", "Удалить", None))
        self.btnClose.setText(_translate("RelatedActionListPage", "Закрыть", None))

from library.TableView import CTableView
