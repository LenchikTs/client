# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Samson\Exchange\ImportOrgsINFIS.ui'
#
# Created: Sun Jun 13 20:50:13 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(479, 500)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self._2 = QtGui.QHBoxLayout()
        self._2.setObjectName("_2")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self._2.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setText("")
        self.edtFileName.setReadOnly(True)
        self.edtFileName.setObjectName("edtFileName")
        self._2.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName("btnSelectFile")
        self._2.addWidget(self.btnSelectFile)
        self.btnView = QtGui.QPushButton(Dialog)
        self.btnView.setObjectName("btnView")
        self._2.addWidget(self.btnView)
        self.verticalLayout_5.addLayout(self._2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gbDublicates = QtGui.QGroupBox(Dialog)
        self.gbDublicates.setObjectName("gbDublicates")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbDublicates)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.chkUpdate = QtGui.QRadioButton(self.gbDublicates)
        self.chkUpdate.setChecked(False)
        self.chkUpdate.setObjectName("chkUpdate")
        self.verticalLayout_4.addWidget(self.chkUpdate)
        self.chkSkip = QtGui.QRadioButton(self.gbDublicates)
        self.chkSkip.setChecked(True)
        self.chkSkip.setObjectName("chkSkip")
        self.verticalLayout_4.addWidget(self.chkSkip)
        self.chkAskUser = QtGui.QRadioButton(self.gbDublicates)
        self.chkAskUser.setObjectName("chkAskUser")
        self.verticalLayout_4.addWidget(self.chkAskUser)
        self.verticalLayout_2.addWidget(self.gbDublicates)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_5.addWidget(self.progressBar)
        self.statusLabel = QtGui.QLabel(Dialog)
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout_5.addWidget(self.statusLabel)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName("log")
        self.verticalLayout_5.addWidget(self.log)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName("btnImport")
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName("labelNum")
        self.hboxlayout.addWidget(self.labelNum)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName("btnClose")
        self.hboxlayout.addWidget(self.btnClose)
        self.verticalLayout_5.addLayout(self.hboxlayout)
        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtFileName, self.btnSelectFile)
        Dialog.setTabOrder(self.btnSelectFile, self.btnView)
        Dialog.setTabOrder(self.btnView, self.chkUpdate)
        Dialog.setTabOrder(self.chkUpdate, self.chkSkip)
        Dialog.setTabOrder(self.chkSkip, self.chkAskUser)
        Dialog.setTabOrder(self.chkAskUser, self.log)
        Dialog.setTabOrder(self.log, self.btnImport)
        Dialog.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Импорт данных об ЛПУ из справочника ИНФИС", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "импортировать из", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectFile.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnView.setText(QtGui.QApplication.translate("Dialog", "Просмотр", None, QtGui.QApplication.UnicodeUTF8))
        self.gbDublicates.setTitle(QtGui.QApplication.translate("Dialog", "Совпадающие записи", None, QtGui.QApplication.UnicodeUTF8))
        self.chkUpdate.setText(QtGui.QApplication.translate("Dialog", "Обновить", None, QtGui.QApplication.UnicodeUTF8))
        self.chkSkip.setText(QtGui.QApplication.translate("Dialog", "Пропустить", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAskUser.setText(QtGui.QApplication.translate("Dialog", "Спросить у пользователя", None, QtGui.QApplication.UnicodeUTF8))
        self.btnImport.setText(QtGui.QApplication.translate("Dialog", "начать импортирование", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNum.setText(QtGui.QApplication.translate("Dialog", "всего записей в источнике:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "закрыть", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
