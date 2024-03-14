# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreF131.ui'
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

class Ui_PreF131Dialog(object):
    def setupUi(self, PreF131Dialog):
        PreF131Dialog.setObjectName(_fromUtf8("PreF131Dialog"))
        PreF131Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PreF131Dialog.resize(530, 700)
        self.gridLayout_3 = QtGui.QGridLayout(PreF131Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(PreF131Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpInspections = QtGui.QGroupBox(self.splitter)
        self.grpInspections.setObjectName(_fromUtf8("grpInspections"))
        self.gridLayout = QtGui.QGridLayout(self.grpInspections)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblDiagnostics = CInDocTableView(self.grpInspections)
        self.tblDiagnostics.setObjectName(_fromUtf8("tblDiagnostics"))
        self.gridLayout.addWidget(self.tblDiagnostics, 0, 0, 1, 4)
        self.btnSelectVisits = QtGui.QPushButton(self.grpInspections)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectVisits.sizePolicy().hasHeightForWidth())
        self.btnSelectVisits.setSizePolicy(sizePolicy)
        self.btnSelectVisits.setMinimumSize(QtCore.QSize(100, 0))
        self.btnSelectVisits.setAutoDefault(False)
        self.btnSelectVisits.setDefault(False)
        self.btnSelectVisits.setObjectName(_fromUtf8("btnSelectVisits"))
        self.gridLayout.addWidget(self.btnSelectVisits, 1, 1, 1, 1)
        self.btnDeselectVisits = QtGui.QPushButton(self.grpInspections)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDeselectVisits.sizePolicy().hasHeightForWidth())
        self.btnDeselectVisits.setSizePolicy(sizePolicy)
        self.btnDeselectVisits.setMinimumSize(QtCore.QSize(100, 0))
        self.btnDeselectVisits.setAutoDefault(False)
        self.btnDeselectVisits.setDefault(False)
        self.btnDeselectVisits.setObjectName(_fromUtf8("btnDeselectVisits"))
        self.gridLayout.addWidget(self.btnDeselectVisits, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(561, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.grpActions = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpActions.sizePolicy().hasHeightForWidth())
        self.grpActions.setSizePolicy(sizePolicy)
        self.grpActions.setMinimumSize(QtCore.QSize(100, 0))
        self.grpActions.setObjectName(_fromUtf8("grpActions"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpActions)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(561, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        self.btnSelectActions = QtGui.QPushButton(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectActions.sizePolicy().hasHeightForWidth())
        self.btnSelectActions.setSizePolicy(sizePolicy)
        self.btnSelectActions.setMinimumSize(QtCore.QSize(100, 0))
        self.btnSelectActions.setAutoDefault(False)
        self.btnSelectActions.setDefault(False)
        self.btnSelectActions.setObjectName(_fromUtf8("btnSelectActions"))
        self.gridLayout_2.addWidget(self.btnSelectActions, 2, 0, 1, 1)
        self.btnDeselectActions = QtGui.QPushButton(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDeselectActions.sizePolicy().hasHeightForWidth())
        self.btnDeselectActions.setSizePolicy(sizePolicy)
        self.btnDeselectActions.setMinimumSize(QtCore.QSize(100, 0))
        self.btnDeselectActions.setAutoDefault(False)
        self.btnDeselectActions.setDefault(False)
        self.btnDeselectActions.setObjectName(_fromUtf8("btnDeselectActions"))
        self.gridLayout_2.addWidget(self.btnDeselectActions, 2, 1, 1, 1)
        self.tblActions = CSortFilterProxyInDocTableView(self.grpActions)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout_2.addWidget(self.tblActions, 0, 0, 1, 4)
        self.edtNameFilter = QtGui.QLineEdit(self.grpActions)
        self.edtNameFilter.setObjectName(_fromUtf8("edtNameFilter"))
        self.gridLayout_2.addWidget(self.edtNameFilter, 1, 0, 1, 3)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox_3 = QtGui.QDialogButtonBox(PreF131Dialog)
        self.buttonBox_3.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_3.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_3.setObjectName(_fromUtf8("buttonBox_3"))
        self.gridLayout_3.addWidget(self.buttonBox_3, 1, 0, 1, 1)

        self.retranslateUi(PreF131Dialog)
        QtCore.QObject.connect(self.buttonBox_3, QtCore.SIGNAL(_fromUtf8("accepted()")), PreF131Dialog.accept)
        QtCore.QObject.connect(self.buttonBox_3, QtCore.SIGNAL(_fromUtf8("rejected()")), PreF131Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreF131Dialog)
        PreF131Dialog.setTabOrder(self.tblDiagnostics, self.btnSelectVisits)
        PreF131Dialog.setTabOrder(self.btnSelectVisits, self.btnDeselectVisits)
        PreF131Dialog.setTabOrder(self.btnDeselectVisits, self.tblActions)
        PreF131Dialog.setTabOrder(self.tblActions, self.edtNameFilter)
        PreF131Dialog.setTabOrder(self.edtNameFilter, self.btnSelectActions)
        PreF131Dialog.setTabOrder(self.btnSelectActions, self.btnDeselectActions)
        PreF131Dialog.setTabOrder(self.btnDeselectActions, self.buttonBox_3)

    def retranslateUi(self, PreF131Dialog):
        PreF131Dialog.setWindowTitle(_translate("PreF131Dialog", "Dialog", None))
        self.grpInspections.setTitle(_translate("PreF131Dialog", "Осмотры", None))
        self.btnSelectVisits.setText(_translate("PreF131Dialog", "Выбрать все", None))
        self.btnDeselectVisits.setText(_translate("PreF131Dialog", "Очистить выбор", None))
        self.grpActions.setTitle(_translate("PreF131Dialog", "Мероприятия", None))
        self.btnSelectActions.setText(_translate("PreF131Dialog", "Выбрать все", None))
        self.btnDeselectActions.setText(_translate("PreF131Dialog", "Очистить выбор", None))

from library.InDocTable import CInDocTableView
from library.SortFilterProxyInDocTableView import CSortFilterProxyInDocTableView
