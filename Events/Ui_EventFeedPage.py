# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventFeedPage.ui'
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

class Ui_EventFeedPage(object):
    def setupUi(self, EventFeedPage):
        EventFeedPage.setObjectName(_fromUtf8("EventFeedPage"))
        EventFeedPage.resize(528, 428)
        self.gridLayout = QtGui.QGridLayout(EventFeedPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(EventFeedPage)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabClientFeed = QtGui.QWidget()
        self.tabClientFeed.setObjectName(_fromUtf8("tabClientFeed"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabClientFeed)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblClientFeed = CFeedInDocTableView(self.tabClientFeed)
        self.tblClientFeed.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblClientFeed.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblClientFeed.setObjectName(_fromUtf8("tblClientFeed"))
        self.gridLayout_2.addWidget(self.tblClientFeed, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabClientFeed, _fromUtf8(""))
        self.tabPatronFeed = QtGui.QWidget()
        self.tabPatronFeed.setObjectName(_fromUtf8("tabPatronFeed"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabPatronFeed)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblPatronFeed = CFeedInDocTableView(self.tabPatronFeed)
        self.tblPatronFeed.setObjectName(_fromUtf8("tblPatronFeed"))
        self.gridLayout_3.addWidget(self.tblPatronFeed, 1, 0, 1, 2)
        self.lblPatronName = QtGui.QLabel(self.tabPatronFeed)
        self.lblPatronName.setObjectName(_fromUtf8("lblPatronName"))
        self.gridLayout_3.addWidget(self.lblPatronName, 0, 0, 1, 2)
        self.tabWidget.addTab(self.tabPatronFeed, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 6)
        self.lblCreatePerson = QtGui.QLabel(EventFeedPage)
        self.lblCreatePerson.setObjectName(_fromUtf8("lblCreatePerson"))
        self.gridLayout.addWidget(self.lblCreatePerson, 1, 0, 1, 1)
        self.lblCreateDate = QtGui.QLabel(EventFeedPage)
        self.lblCreateDate.setText(_fromUtf8(""))
        self.lblCreateDate.setObjectName(_fromUtf8("lblCreateDate"))
        self.gridLayout.addWidget(self.lblCreateDate, 1, 1, 1, 1)
        self.lblModifyPerson = QtGui.QLabel(EventFeedPage)
        self.lblModifyPerson.setObjectName(_fromUtf8("lblModifyPerson"))
        self.gridLayout.addWidget(self.lblModifyPerson, 1, 2, 1, 1)
        self.lblModifyDate = QtGui.QLabel(EventFeedPage)
        self.lblModifyDate.setText(_fromUtf8(""))
        self.lblModifyDate.setObjectName(_fromUtf8("lblModifyDate"))
        self.gridLayout.addWidget(self.lblModifyDate, 1, 3, 1, 1)
        self.btnFeedPrint = QtGui.QPushButton(EventFeedPage)
        self.btnFeedPrint.setObjectName(_fromUtf8("btnFeedPrint"))
        self.gridLayout.addWidget(self.btnFeedPrint, 1, 4, 1, 1)
        self.btnGetMenu = QtGui.QPushButton(EventFeedPage)
        self.btnGetMenu.setObjectName(_fromUtf8("btnGetMenu"))
        self.gridLayout.addWidget(self.btnGetMenu, 1, 5, 1, 1)

        self.retranslateUi(EventFeedPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EventFeedPage)
        EventFeedPage.setTabOrder(self.tabWidget, self.tblClientFeed)
        EventFeedPage.setTabOrder(self.tblClientFeed, self.tblPatronFeed)
        EventFeedPage.setTabOrder(self.tblPatronFeed, self.btnFeedPrint)
        EventFeedPage.setTabOrder(self.btnFeedPrint, self.btnGetMenu)

    def retranslateUi(self, EventFeedPage):
        EventFeedPage.setWindowTitle(_translate("EventFeedPage", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabClientFeed), _translate("EventFeedPage", "Питание пациента", None))
        self.lblPatronName.setText(_translate("EventFeedPage", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPatronFeed), _translate("EventFeedPage", "Питание лица по уходу", None))
        self.lblCreatePerson.setText(_translate("EventFeedPage", "Автор: ", None))
        self.lblModifyPerson.setText(_translate("EventFeedPage", "Изменил: ", None))
        self.btnFeedPrint.setText(_translate("EventFeedPage", "Печать", None))
        self.btnGetMenu.setText(_translate("EventFeedPage", "Шаблон", None))

from Events.EventFeedModel import CFeedInDocTableView
