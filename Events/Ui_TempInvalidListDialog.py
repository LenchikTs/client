# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\Events\TempInvalidListDialog.ui'
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

class Ui_TempInvalidList(object):
    def setupUi(self, TempInvalidList):
        TempInvalidList.setObjectName(_fromUtf8("TempInvalidList"))
        TempInvalidList.resize(1180, 957)
        self.verticalLayout = QtGui.QVBoxLayout(TempInvalidList)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabTempInvalidAndAegrotat = QtGui.QTabWidget(TempInvalidList)
        self.tabTempInvalidAndAegrotat.setObjectName(_fromUtf8("tabTempInvalidAndAegrotat"))
        self.tabTempInvalid = QtGui.QWidget()
        self.tabTempInvalid.setObjectName(_fromUtf8("tabTempInvalid"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabTempInvalid)
        self.verticalLayout_5.setMargin(4)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.grpTempInvalid = CTempInvalid(self.tabTempInvalid)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpTempInvalid.sizePolicy().hasHeightForWidth())
        self.grpTempInvalid.setSizePolicy(sizePolicy)
        self.grpTempInvalid.setChecked(False)
        self.grpTempInvalid.setObjectName(_fromUtf8("grpTempInvalid"))
        self.verticalLayout_5.addWidget(self.grpTempInvalid)
        self.tabTempInvalidAndAegrotat.addTab(self.tabTempInvalid, _fromUtf8(""))
        self.tabAegrotat = QtGui.QWidget()
        self.tabAegrotat.setObjectName(_fromUtf8("tabAegrotat"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabAegrotat)
        self.verticalLayout_4.setMargin(4)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.grpAegrotat = CTempInvalid(self.tabAegrotat)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpAegrotat.sizePolicy().hasHeightForWidth())
        self.grpAegrotat.setSizePolicy(sizePolicy)
        self.grpAegrotat.setChecked(False)
        self.grpAegrotat.setObjectName(_fromUtf8("grpAegrotat"))
        self.verticalLayout_4.addWidget(self.grpAegrotat)
        self.tabTempInvalidAndAegrotat.addTab(self.tabAegrotat, _fromUtf8(""))
        self.tabDisability = QtGui.QWidget()
        self.tabDisability.setObjectName(_fromUtf8("tabDisability"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabDisability)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.grpDisability = CTempInvalid(self.tabDisability)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpDisability.sizePolicy().hasHeightForWidth())
        self.grpDisability.setSizePolicy(sizePolicy)
        self.grpDisability.setChecked(False)
        self.grpDisability.setObjectName(_fromUtf8("grpDisability"))
        self.verticalLayout_2.addWidget(self.grpDisability)
        self.tabTempInvalidAndAegrotat.addTab(self.tabDisability, _fromUtf8(""))
        self.tabVitalRestriction = QtGui.QWidget()
        self.tabVitalRestriction.setObjectName(_fromUtf8("tabVitalRestriction"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tabVitalRestriction)
        self.verticalLayout_6.setMargin(4)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.grpVitalRestriction = CTempInvalid(self.tabVitalRestriction)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpVitalRestriction.sizePolicy().hasHeightForWidth())
        self.grpVitalRestriction.setSizePolicy(sizePolicy)
        self.grpVitalRestriction.setChecked(False)
        self.grpVitalRestriction.setObjectName(_fromUtf8("grpVitalRestriction"))
        self.verticalLayout_6.addWidget(self.grpVitalRestriction)
        self.tabTempInvalidAndAegrotat.addTab(self.tabVitalRestriction, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabTempInvalidAndAegrotat)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TempInvalidList)
        self.tabTempInvalidAndAegrotat.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidList.reject)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidList)

    def retranslateUi(self, TempInvalidList):
        TempInvalidList.setWindowTitle(_translate("TempInvalidList", "Dialog", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabTempInvalid), _translate("TempInvalidList", "Листок &нетрудоспособности", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabAegrotat), _translate("TempInvalidList", "С&правка", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabDisability), _translate("TempInvalidList", "Инвалидность", None))
        self.tabTempInvalidAndAegrotat.setTabText(self.tabTempInvalidAndAegrotat.indexOf(self.tabVitalRestriction), _translate("TempInvalidList", "&Ограничения жизнедеятельности", None))

from Events.TempInvalid import CTempInvalid
