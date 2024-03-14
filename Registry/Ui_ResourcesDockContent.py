# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Registry/ResourcesDockContent.ui'
#
# Created: Tue Nov 13 17:12:14 2018
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(202, 720)
        self.hboxlayout = QtGui.QHBoxLayout(Form)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.splitterMain = QtGui.QSplitter(Form)
        self.splitterMain.setOrientation(QtCore.Qt.Vertical)
        self.splitterMain.setChildrenCollapsible(False)
        self.splitterMain.setObjectName(_fromUtf8("splitterMain"))
        self.splitterOrgs = QtGui.QSplitter(self.splitterMain)
        self.splitterOrgs.setOrientation(QtCore.Qt.Horizontal)
        self.splitterOrgs.setHandleWidth(2)
        self.splitterOrgs.setChildrenCollapsible(False)
        self.splitterOrgs.setObjectName(_fromUtf8("splitterOrgs"))
        self.treeOrgStructure = CTreeView(self.splitterOrgs)
        self.treeOrgStructure.setObjectName(_fromUtf8("treeOrgStructure"))
        self.treeOrgPersonnel = CTreeView(self.splitterOrgs)
        self.treeOrgPersonnel.setObjectName(_fromUtf8("treeOrgPersonnel"))
        self.calendarWidget = CCalendarWidget(self.splitterMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.tabPlace = QtGui.QTabWidget(self.splitterMain)
        self.tabPlace.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabPlace.setObjectName(_fromUtf8("tabPlace"))
        self.tabAmbulatory = QtGui.QWidget()
        self.tabAmbulatory.setObjectName(_fromUtf8("tabAmbulatory"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabAmbulatory)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.tabAmbulatory)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(4)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblAmbTimeTable = CTableView(self.splitter)
        self.tblAmbTimeTable.setObjectName(_fromUtf8("tblAmbTimeTable"))
        self.tblAmbQueue = CTableView(self.splitter)
        self.tblAmbQueue.setObjectName(_fromUtf8("tblAmbQueue"))
        self.verticalLayout.addWidget(self.splitter)
        self.tabPlace.addTab(self.tabAmbulatory, _fromUtf8(""))
        self.tabHome = QtGui.QWidget()
        self.tabHome.setObjectName(_fromUtf8("tabHome"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabHome)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter_2 = QtGui.QSplitter(self.tabHome)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(4)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.tblHomeTimeTable = CTableView(self.splitter_2)
        self.tblHomeTimeTable.setObjectName(_fromUtf8("tblHomeTimeTable"))
        self.tblHomeQueue = CTableView(self.splitter_2)
        self.tblHomeQueue.setObjectName(_fromUtf8("tblHomeQueue"))
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.tabPlace.addTab(self.tabHome, _fromUtf8(""))
        self.hboxlayout.addWidget(self.splitterMain)

        self.retranslateUi(Form)
        self.tabPlace.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.treeOrgStructure, self.treeOrgPersonnel)
        Form.setTabOrder(self.treeOrgPersonnel, self.calendarWidget)
        Form.setTabOrder(self.calendarWidget, self.tabPlace)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.tabPlace.setTabText(self.tabPlace.indexOf(self.tabAmbulatory), _translate("Form", "Амбулаторно", None))
        self.tabPlace.setTabText(self.tabPlace.indexOf(self.tabHome), _translate("Form", "На дому", None))

from library.CalendarWidget import CCalendarWidget
from library.TreeView import CTreeView
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

