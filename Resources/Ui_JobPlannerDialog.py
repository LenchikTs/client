# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\samson\Resources\JobPlannerDialog.ui'
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

class Ui_JobPlannerDialog(object):
    def setupUi(self, JobPlannerDialog):
        JobPlannerDialog.setObjectName(_fromUtf8("JobPlannerDialog"))
        JobPlannerDialog.resize(656, 581)
        self.verticalLayout = QtGui.QVBoxLayout(JobPlannerDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(JobPlannerDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.calendar = CCalendarWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setGridVisible(False)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.treeOrgStructure = QtGui.QTreeView(self.splitter)
        self.treeOrgStructure.setObjectName(_fromUtf8("treeOrgStructure"))
        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnPrint = QtGui.QPushButton(self.widget)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 1, 1, 1, 1)
        self.btnClose = QtGui.QPushButton(self.widget)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(273, 23, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.btnFill = QtGui.QPushButton(self.widget)
        self.btnFill.setObjectName(_fromUtf8("btnFill"))
        self.gridLayout.addWidget(self.btnFill, 1, 0, 1, 1)
        self.tblJobs = CJobsView(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblJobs.sizePolicy().hasHeightForWidth())
        self.tblJobs.setSizePolicy(sizePolicy)
        self.tblJobs.setObjectName(_fromUtf8("tblJobs"))
        self.gridLayout.addWidget(self.tblJobs, 0, 0, 1, 5)
        self.btnApply = QtGui.QPushButton(self.widget)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.gridLayout.addWidget(self.btnApply, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.splitter_2)

        self.retranslateUi(JobPlannerDialog)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), JobPlannerDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(JobPlannerDialog)
        JobPlannerDialog.setTabOrder(self.calendar, self.treeOrgStructure)
        JobPlannerDialog.setTabOrder(self.treeOrgStructure, self.tblJobs)
        JobPlannerDialog.setTabOrder(self.tblJobs, self.btnFill)
        JobPlannerDialog.setTabOrder(self.btnFill, self.btnClose)

    def retranslateUi(self, JobPlannerDialog):
        JobPlannerDialog.setWindowTitle(_translate("JobPlannerDialog", "Планирование работ", None))
        self.btnPrint.setText(_translate("JobPlannerDialog", "Печать", None))
        self.btnClose.setText(_translate("JobPlannerDialog", "Закрыть", None))
        self.btnFill.setText(_translate("JobPlannerDialog", "Заполнить", None))
        self.btnApply.setText(_translate("JobPlannerDialog", "Применить", None))

from Resources.Jobs import CJobsView
from library.CalendarWidget import CCalendarWidget
