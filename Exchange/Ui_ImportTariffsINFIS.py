# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportTariffsINFIS.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(480, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.btnView = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnView.sizePolicy().hasHeightForWidth())
        self.btnView.setSizePolicy(sizePolicy)
        self.btnView.setObjectName(_fromUtf8("btnView"))
        self.gridLayout_3.addWidget(self.btnView, 0, 5, 1, 1)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.gridLayout_3.addWidget(self.btnSelectFile, 0, 4, 1, 1)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setText(_fromUtf8(""))
        self.edtFileName.setReadOnly(True)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.gridLayout_3.addWidget(self.edtFileName, 0, 2, 1, 2)
        self.gbRefBooks = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbRefBooks.sizePolicy().hasHeightForWidth())
        self.gbRefBooks.setSizePolicy(sizePolicy)
        self.gbRefBooks.setObjectName(_fromUtf8("gbRefBooks"))
        self.gridLayout = QtGui.QGridLayout(self.gbRefBooks)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblRbProfile = QtGui.QLabel(self.gbRefBooks)
        self.lblRbProfile.setObjectName(_fromUtf8("lblRbProfile"))
        self.gridLayout.addWidget(self.lblRbProfile, 0, 0, 1, 1)
        self.edtRbProfileFileName = QtGui.QLineEdit(self.gbRefBooks)
        self.edtRbProfileFileName.setObjectName(_fromUtf8("edtRbProfileFileName"))
        self.gridLayout.addWidget(self.edtRbProfileFileName, 0, 1, 1, 1)
        self.btnViewRbProfile = QtGui.QPushButton(self.gbRefBooks)
        self.btnViewRbProfile.setEnabled(False)
        self.btnViewRbProfile.setObjectName(_fromUtf8("btnViewRbProfile"))
        self.gridLayout.addWidget(self.btnViewRbProfile, 0, 6, 1, 1)
        self.lblRbLoadedInfo = QtGui.QLabel(self.gbRefBooks)
        self.lblRbLoadedInfo.setText(_fromUtf8(""))
        self.lblRbLoadedInfo.setObjectName(_fromUtf8("lblRbLoadedInfo"))
        self.gridLayout.addWidget(self.lblRbLoadedInfo, 2, 0, 1, 7)
        self.btnLoadRbProfile = QtGui.QPushButton(self.gbRefBooks)
        self.btnLoadRbProfile.setEnabled(False)
        self.btnLoadRbProfile.setObjectName(_fromUtf8("btnLoadRbProfile"))
        self.gridLayout.addWidget(self.btnLoadRbProfile, 0, 3, 1, 1)
        self.btnSelectFileRbProfile = QtGui.QToolButton(self.gbRefBooks)
        self.btnSelectFileRbProfile.setObjectName(_fromUtf8("btnSelectFileRbProfile"))
        self.gridLayout.addWidget(self.btnSelectFileRbProfile, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.gbRefBooks, 1, 0, 1, 6)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout_3.addWidget(self.log, 6, 0, 1, 6)
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.gridLayout_3.addWidget(self.btnImport, 7, 0, 1, 3)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName(_fromUtf8("labelNum"))
        self.gridLayout_3.addWidget(self.labelNum, 7, 3, 1, 1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout_3.addWidget(self.btnClose, 7, 5, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_3.addWidget(self.progressBar, 5, 0, 1, 6)
        self.frmOptions = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmOptions.sizePolicy().hasHeightForWidth())
        self.frmOptions.setSizePolicy(sizePolicy)
        self.frmOptions.setObjectName(_fromUtf8("frmOptions"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frmOptions)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.frmOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.chkLoadService = QtGui.QCheckBox(self.groupBox)
        self.chkLoadService.setObjectName(_fromUtf8("chkLoadService"))
        self.gridLayout_2.addWidget(self.chkLoadService, 4, 0, 1, 1)
        self.chkLoadVisit = QtGui.QCheckBox(self.groupBox)
        self.chkLoadVisit.setObjectName(_fromUtf8("chkLoadVisit"))
        self.gridLayout_2.addWidget(self.chkLoadVisit, 3, 0, 1, 1)
        self.chkLoadMes = QtGui.QCheckBox(self.groupBox)
        self.chkLoadMes.setObjectName(_fromUtf8("chkLoadMes"))
        self.gridLayout_2.addWidget(self.chkLoadMes, 5, 0, 1, 1)
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)
        self.chkLoadMature = QtGui.QCheckBox(self.groupBox)
        self.chkLoadMature.setChecked(True)
        self.chkLoadMature.setObjectName(_fromUtf8("chkLoadMature"))
        self.gridLayout_2.addWidget(self.chkLoadMature, 0, 0, 1, 1)
        self.chkLoadChildren = QtGui.QCheckBox(self.groupBox)
        self.chkLoadChildren.setChecked(True)
        self.chkLoadChildren.setObjectName(_fromUtf8("chkLoadChildren"))
        self.gridLayout_2.addWidget(self.chkLoadChildren, 1, 0, 1, 1)
        self.chkLoadChildren.raise_()
        self.line.raise_()
        self.chkLoadMes.raise_()
        self.chkLoadMature.raise_()
        self.chkLoadVisit.raise_()
        self.chkLoadService.raise_()
        self.horizontalLayout.addWidget(self.groupBox)
        self.gbPeriod = QtGui.QGroupBox(self.frmOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.gbPeriod.sizePolicy().hasHeightForWidth())
        self.gbPeriod.setSizePolicy(sizePolicy)
        self.gbPeriod.setObjectName(_fromUtf8("gbPeriod"))
        self.gridLayout_4 = QtGui.QGridLayout(self.gbPeriod)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblEndDate = QtGui.QLabel(self.gbPeriod)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout_4.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(self.gbPeriod)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout_4.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(self.gbPeriod)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout_4.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.edtBegDate = CDateEdit(self.gbPeriod)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout_4.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.gbPeriod)
        self.gbDublicates = QtGui.QGroupBox(self.frmOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbDublicates.sizePolicy().hasHeightForWidth())
        self.gbDublicates.setSizePolicy(sizePolicy)
        self.gbDublicates.setObjectName(_fromUtf8("gbDublicates"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbDublicates)
        self.verticalLayout_4.setMargin(4)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.chkUpdate = QtGui.QRadioButton(self.gbDublicates)
        self.chkUpdate.setChecked(True)
        self.chkUpdate.setObjectName(_fromUtf8("chkUpdate"))
        self.verticalLayout_4.addWidget(self.chkUpdate)
        self.chkSkip = QtGui.QRadioButton(self.gbDublicates)
        self.chkSkip.setObjectName(_fromUtf8("chkSkip"))
        self.verticalLayout_4.addWidget(self.chkSkip)
        self.chkAskUser = QtGui.QRadioButton(self.gbDublicates)
        self.chkAskUser.setObjectName(_fromUtf8("chkAskUser"))
        self.verticalLayout_4.addWidget(self.chkAskUser)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.gbDublicates)
        self.gridLayout_3.addWidget(self.frmOptions, 3, 0, 2, 6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtFileName, self.btnSelectFile)
        Dialog.setTabOrder(self.btnSelectFile, self.btnView)
        Dialog.setTabOrder(self.btnView, self.edtRbProfileFileName)
        Dialog.setTabOrder(self.edtRbProfileFileName, self.btnSelectFileRbProfile)
        Dialog.setTabOrder(self.btnSelectFileRbProfile, self.btnLoadRbProfile)
        Dialog.setTabOrder(self.btnLoadRbProfile, self.btnViewRbProfile)
        Dialog.setTabOrder(self.btnViewRbProfile, self.chkLoadMature)
        Dialog.setTabOrder(self.chkLoadMature, self.chkLoadChildren)
        Dialog.setTabOrder(self.chkLoadChildren, self.chkLoadVisit)
        Dialog.setTabOrder(self.chkLoadVisit, self.chkLoadService)
        Dialog.setTabOrder(self.chkLoadService, self.chkLoadMes)
        Dialog.setTabOrder(self.chkLoadMes, self.edtBegDate)
        Dialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        Dialog.setTabOrder(self.edtEndDate, self.chkUpdate)
        Dialog.setTabOrder(self.chkUpdate, self.chkSkip)
        Dialog.setTabOrder(self.chkSkip, self.chkAskUser)
        Dialog.setTabOrder(self.chkAskUser, self.log)
        Dialog.setTabOrder(self.log, self.btnImport)
        Dialog.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка тарифов из ИНФИС", None))
        self.btnView.setText(_translate("Dialog", "Просмотр", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.gbRefBooks.setTitle(_translate("Dialog", "Справочники для определения типа тарификации", None))
        self.lblRbProfile.setText(_translate("Dialog", "Справочник профилей", None))
        self.btnViewRbProfile.setText(_translate("Dialog", "Просмотр", None))
        self.btnLoadRbProfile.setText(_translate("Dialog", "Загрузить", None))
        self.btnSelectFileRbProfile.setText(_translate("Dialog", "...", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))
        self.groupBox.setTitle(_translate("Dialog", "Загружать", None))
        self.chkLoadService.setText(_translate("Dialog", "Услуги", None))
        self.chkLoadVisit.setText(_translate("Dialog", "Посещения", None))
        self.chkLoadMes.setText(_translate("Dialog", "МЭС", None))
        self.chkLoadMature.setText(_translate("Dialog", "Взрослые", None))
        self.chkLoadChildren.setText(_translate("Dialog", "Детские", None))
        self.gbPeriod.setTitle(_translate("Dialog", "Период", None))
        self.lblEndDate.setText(_translate("Dialog", "по", None))
        self.lblBegDate.setText(_translate("Dialog", "с", None))
        self.gbDublicates.setTitle(_translate("Dialog", "Совпадающие записи", None))
        self.chkUpdate.setText(_translate("Dialog", "Обновить", None))
        self.chkSkip.setText(_translate("Dialog", "Пропустить", None))
        self.chkAskUser.setText(_translate("Dialog", "Спросить у пользователя", None))

from library.DateEdit import CDateEdit
