# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ImportTariffsR67.ui'
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
        Dialog.resize(500, 421)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setText(_fromUtf8(""))
        self.edtFileName.setReadOnly(True)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.gridLayout_2.addWidget(self.edtFileName, 0, 1, 1, 1)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.gridLayout_2.addWidget(self.btnSelectFile, 0, 2, 1, 1)
        self.btnView = QtGui.QPushButton(Dialog)
        self.btnView.setObjectName(_fromUtf8("btnView"))
        self.gridLayout_2.addWidget(self.btnView, 0, 3, 1, 1)
        self.frmOptions = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmOptions.sizePolicy().hasHeightForWidth())
        self.frmOptions.setSizePolicy(sizePolicy)
        self.frmOptions.setObjectName(_fromUtf8("frmOptions"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frmOptions)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.grpOptions = QtGui.QGroupBox(self.frmOptions)
        self.grpOptions.setObjectName(_fromUtf8("grpOptions"))
        self.gridLayout = QtGui.QGridLayout(self.grpOptions)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtUetValue = QtGui.QDoubleSpinBox(self.grpOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtUetValue.sizePolicy().hasHeightForWidth())
        self.edtUetValue.setSizePolicy(sizePolicy)
        self.edtUetValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edtUetValue.setMinimum(0.01)
        self.edtUetValue.setMaximum(99999999.99)
        self.edtUetValue.setObjectName(_fromUtf8("edtUetValue"))
        self.gridLayout.addWidget(self.edtUetValue, 1, 2, 2, 1)
        self.lblUetValue = QtGui.QLabel(self.grpOptions)
        self.lblUetValue.setObjectName(_fromUtf8("lblUetValue"))
        self.gridLayout.addWidget(self.lblUetValue, 1, 0, 2, 2)
        self.chkOnlyForCurrentOrg = QtGui.QCheckBox(self.grpOptions)
        self.chkOnlyForCurrentOrg.setObjectName(_fromUtf8("chkOnlyForCurrentOrg"))
        self.gridLayout.addWidget(self.chkOnlyForCurrentOrg, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.grpOptions)
        self.gbDublicates = QtGui.QGroupBox(self.frmOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbDublicates.sizePolicy().hasHeightForWidth())
        self.gbDublicates.setSizePolicy(sizePolicy)
        self.gbDublicates.setObjectName(_fromUtf8("gbDublicates"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbDublicates)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkUpdate = QtGui.QRadioButton(self.gbDublicates)
        self.chkUpdate.setChecked(True)
        self.chkUpdate.setObjectName(_fromUtf8("chkUpdate"))
        self.verticalLayout.addWidget(self.chkUpdate)
        self.chkAppend = QtGui.QRadioButton(self.gbDublicates)
        self.chkAppend.setObjectName(_fromUtf8("chkAppend"))
        self.verticalLayout.addWidget(self.chkAppend)
        self.chkSkip = QtGui.QRadioButton(self.gbDublicates)
        self.chkSkip.setObjectName(_fromUtf8("chkSkip"))
        self.verticalLayout.addWidget(self.chkSkip)
        self.chkAskUser = QtGui.QRadioButton(self.gbDublicates)
        self.chkAskUser.setObjectName(_fromUtf8("chkAskUser"))
        self.verticalLayout.addWidget(self.chkAskUser)
        self.horizontalLayout_2.addWidget(self.gbDublicates)
        self.gridLayout_2.addWidget(self.frmOptions, 1, 0, 1, 4)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 4)
        self.statusLabel = QtGui.QLabel(Dialog)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout_2.addWidget(self.statusLabel, 3, 0, 1, 4)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout_2.addWidget(self.log, 4, 0, 1, 4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.horizontalLayout.addWidget(self.btnImport)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName(_fromUtf8("labelNum"))
        self.horizontalLayout.addWidget(self.labelNum)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout.addWidget(self.btnClose)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtFileName, self.btnSelectFile)
        Dialog.setTabOrder(self.btnSelectFile, self.btnView)
        Dialog.setTabOrder(self.btnView, self.chkOnlyForCurrentOrg)
        Dialog.setTabOrder(self.chkOnlyForCurrentOrg, self.edtUetValue)
        Dialog.setTabOrder(self.edtUetValue, self.chkUpdate)
        Dialog.setTabOrder(self.chkUpdate, self.chkAppend)
        Dialog.setTabOrder(self.chkAppend, self.chkSkip)
        Dialog.setTabOrder(self.chkSkip, self.chkAskUser)
        Dialog.setTabOrder(self.chkAskUser, self.log)
        Dialog.setTabOrder(self.log, self.btnImport)
        Dialog.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка тарифов для Смоленской области", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.btnView.setText(_translate("Dialog", "Просмотр", None))
        self.grpOptions.setTitle(_translate("Dialog", "Опции", None))
        self.lblUetValue.setToolTip(_translate("Dialog", "только для стоматологии", None))
        self.lblUetValue.setText(_translate("Dialog", "Стоимость одного УЕТ", None))
        self.chkOnlyForCurrentOrg.setToolTip(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Импортируются только те тарифы, для которых код в поле <span style=\" font-weight:600;\">MCOD </span>источника совпадает с кодом <span style=\" font-weight:600;\">ИНФИС </span>текущей организации.</p></body></html>", None))
        self.chkOnlyForCurrentOrg.setText(_translate("Dialog", "только для текущего ЛПУ", None))
        self.gbDublicates.setTitle(_translate("Dialog", "Совпадающие записи", None))
        self.chkUpdate.setText(_translate("Dialog", "Обновить", None))
        self.chkAppend.setToolTip(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Добавляется </span><span style=\" font-size:8pt; font-weight:600;\">новый</span><span style=\" font-size:8pt;\"> тариф, действующий с</span><span style=\" font-size:8pt; font-weight:600;\"> текущей</span><span style=\" font-size:8pt;\"> даты, а существующий тариф закрывается с днём ранее </span><span style=\" font-size:8pt; font-weight:600;\">текущей</span><span style=\" font-size:8pt;\"> даты.</span></p></body></html>", None))
        self.chkAppend.setText(_translate("Dialog", "Дополнить", None))
        self.chkSkip.setText(_translate("Dialog", "Пропустить", None))
        self.chkAskUser.setText(_translate("Dialog", "Спросить у пользователя", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))

