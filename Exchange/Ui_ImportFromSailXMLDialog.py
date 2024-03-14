# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SAMSON\2.5\s11-svn\Exchange\ImportFromSailXMLDialog.ui'
#
# Created: Sat Apr 13 16:35:51 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_ImportFromSailXMLDialog(object):
    def setupUi(self, ImportFromSailXMLDialog):
        ImportFromSailXMLDialog.setObjectName(_fromUtf8("ImportFromSailXMLDialog"))
        ImportFromSailXMLDialog.resize(498, 380)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImportFromSailXMLDialog.sizePolicy().hasHeightForWidth())
        ImportFromSailXMLDialog.setSizePolicy(sizePolicy)
        self.log = QtGui.QTextBrowser(ImportFromSailXMLDialog)
        self.log.setGeometry(QtCore.QRect(10, 140, 481, 181))
        self.log.setObjectName(_fromUtf8("log"))
        self.layoutWidget = QtGui.QWidget(ImportFromSailXMLDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 350, 481, 27))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(self.layoutWidget)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(self.layoutWidget)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.stat = QtGui.QLabel(ImportFromSailXMLDialog)
        self.stat.setGeometry(QtCore.QRect(10, 330, 481, 20))
        self.stat.setText(_fromUtf8(""))
        self.stat.setObjectName(_fromUtf8("stat"))
        self.prbImport = QtGui.QProgressBar(ImportFromSailXMLDialog)
        self.prbImport.setGeometry(QtCore.QRect(10, 110, 481, 21))
        self.prbImport.setProperty("value", 24)
        self.prbImport.setOrientation(QtCore.Qt.Horizontal)
        self.prbImport.setObjectName(_fromUtf8("prbImport"))
        self.wControl = QtGui.QWidget(ImportFromSailXMLDialog)
        self.wControl.setGeometry(QtCore.QRect(0, 0, 501, 101))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wControl.sizePolicy().hasHeightForWidth())
        self.wControl.setSizePolicy(sizePolicy)
        self.wControl.setObjectName(_fromUtf8("wControl"))
        self.cbNet = QtGui.QComboBox(self.wControl)
        self.cbNet.setGeometry(QtCore.QRect(250, 70, 241, 22))
        self.cbNet.setObjectName(_fromUtf8("cbNet"))
        self.btnSelectFileXML = QtGui.QToolButton(self.wControl)
        self.btnSelectFileXML.setGeometry(QtCore.QRect(470, 10, 25, 19))
        self.btnSelectFileXML.setObjectName(_fromUtf8("btnSelectFileXML"))
        self.cbType = QtGui.QComboBox(self.wControl)
        self.cbType.setGeometry(QtCore.QRect(10, 70, 221, 22))
        self.cbType.setObjectName(_fromUtf8("cbType"))
        self.cbType.addItem(_fromUtf8(""))
        self.cbType.addItem(_fromUtf8(""))
        self.cbType.addItem(_fromUtf8(""))
        self.cbType.addItem(_fromUtf8(""))
        self.cbType.addItem(_fromUtf8(""))
        self.cbType.addItem(_fromUtf8(""))
        self.lbNet = QtGui.QLabel(self.wControl)
        self.lbNet.setGeometry(QtCore.QRect(250, 50, 221, 16))
        self.lbNet.setObjectName(_fromUtf8("lbNet"))
        self.lbType = QtGui.QLabel(self.wControl)
        self.lbType.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.lbType.setObjectName(_fromUtf8("lbType"))
        self.chkPersonImport = QtGui.QCheckBox(self.wControl)
        self.chkPersonImport.setGeometry(QtCore.QRect(10, 30, 181, 18))
        self.chkPersonImport.setChecked(True)
        self.chkPersonImport.setObjectName(_fromUtf8("chkPersonImport"))
        self.edtFileNameXML = QtGui.QLineEdit(self.wControl)
        self.edtFileNameXML.setGeometry(QtCore.QRect(10, 10, 451, 20))
        self.edtFileNameXML.setReadOnly(True)
        self.edtFileNameXML.setObjectName(_fromUtf8("edtFileNameXML"))

        self.retranslateUi(ImportFromSailXMLDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportFromSailXMLDialog)

    def retranslateUi(self, ImportFromSailXMLDialog):
        ImportFromSailXMLDialog.setWindowTitle(_translate("ImportFromSailXMLDialog", "Импорт из ИС \"Парус. Прогресс\"", None))
        self.btnImport.setText(_translate("ImportFromSailXMLDialog", "начать импортирование", None))
        self.btnClose.setText(_translate("ImportFromSailXMLDialog", "закрыть", None))
        self.btnSelectFileXML.setText(_translate("ImportFromSailXMLDialog", "...", None))
        self.cbType.setItemText(0, _translate("ImportFromSailXMLDialog", "Не задана", None))
        self.cbType.setItemText(1, _translate("ImportFromSailXMLDialog", "Амбулатория", None))
        self.cbType.setItemText(2, _translate("ImportFromSailXMLDialog", "Стационар", None))
        self.cbType.setItemText(3, _translate("ImportFromSailXMLDialog", "Скорая помощь", None))
        self.cbType.setItemText(4, _translate("ImportFromSailXMLDialog", "Мобильная станция", None))
        self.cbType.setItemText(5, _translate("ImportFromSailXMLDialog", "Приемное отделение стационара", None))
        self.lbNet.setText(_translate("ImportFromSailXMLDialog", "Сеть по умолчанию:", None))
        self.lbType.setText(_translate("ImportFromSailXMLDialog", "Тип по умолчанию:", None))
        self.chkPersonImport.setText(_translate("ImportFromSailXMLDialog", "Импортировать персонал", None))

