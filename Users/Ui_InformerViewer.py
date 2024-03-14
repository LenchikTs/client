# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Users\InformerViewer.ui'
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

class Ui_InformerPage(object):
    def setupUi(self, InformerPage):
        InformerPage.setObjectName(_fromUtf8("InformerPage"))
        InformerPage.resize(630, 371)
        InformerPage.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(InformerPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabInformer = QtGui.QTabWidget(InformerPage)
        self.tabInformer.setObjectName(_fromUtf8("tabInformer"))
        self.tabSystem = QtGui.QWidget()
        self.tabSystem.setObjectName(_fromUtf8("tabSystem"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabSystem)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblSystemCreatePerson = QtGui.QLabel(self.tabSystem)
        self.lblSystemCreatePerson.setObjectName(_fromUtf8("lblSystemCreatePerson"))
        self.gridLayout_2.addWidget(self.lblSystemCreatePerson, 0, 0, 1, 1)
        self.lblSystemCreatePersonValue = QtGui.QLabel(self.tabSystem)
        self.lblSystemCreatePersonValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblSystemCreatePersonValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblSystemCreatePersonValue.setText(_fromUtf8(""))
        self.lblSystemCreatePersonValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblSystemCreatePersonValue.setObjectName(_fromUtf8("lblSystemCreatePersonValue"))
        self.gridLayout_2.addWidget(self.lblSystemCreatePersonValue, 0, 1, 1, 2)
        self.lblSystemCreateDatetime = QtGui.QLabel(self.tabSystem)
        self.lblSystemCreateDatetime.setObjectName(_fromUtf8("lblSystemCreateDatetime"))
        self.gridLayout_2.addWidget(self.lblSystemCreateDatetime, 1, 0, 1, 1)
        self.lblSystemCreateDatetimeValue = QtGui.QLabel(self.tabSystem)
        self.lblSystemCreateDatetimeValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblSystemCreateDatetimeValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblSystemCreateDatetimeValue.setText(_fromUtf8(""))
        self.lblSystemCreateDatetimeValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblSystemCreateDatetimeValue.setObjectName(_fromUtf8("lblSystemCreateDatetimeValue"))
        self.gridLayout_2.addWidget(self.lblSystemCreateDatetimeValue, 1, 1, 1, 2)
        self.lblSystemSubject = QtGui.QLabel(self.tabSystem)
        self.lblSystemSubject.setObjectName(_fromUtf8("lblSystemSubject"))
        self.gridLayout_2.addWidget(self.lblSystemSubject, 2, 0, 1, 1)
        self.edtSystemText = QtGui.QTextBrowser(self.tabSystem)
        self.edtSystemText.setOpenExternalLinks(True)
        self.edtSystemText.setObjectName(_fromUtf8("edtSystemText"))
        self.gridLayout_2.addWidget(self.edtSystemText, 3, 1, 1, 2)
        self.systemButtonBox = QtGui.QDialogButtonBox(self.tabSystem)
        self.systemButtonBox.setStandardButtons(QtGui.QDialogButtonBox.NoButton)
        self.systemButtonBox.setObjectName(_fromUtf8("systemButtonBox"))
        self.gridLayout_2.addWidget(self.systemButtonBox, 4, 2, 1, 1)
        self.lblSystemText = QtGui.QLabel(self.tabSystem)
        self.lblSystemText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblSystemText.setObjectName(_fromUtf8("lblSystemText"))
        self.gridLayout_2.addWidget(self.lblSystemText, 3, 0, 1, 1)
        self.lblSystemSubjectValue = QtGui.QLabel(self.tabSystem)
        self.lblSystemSubjectValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblSystemSubjectValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblSystemSubjectValue.setText(_fromUtf8(""))
        self.lblSystemSubjectValue.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblSystemSubjectValue.setObjectName(_fromUtf8("lblSystemSubjectValue"))
        self.gridLayout_2.addWidget(self.lblSystemSubjectValue, 2, 1, 1, 2)
        self.chkSystemMarkViewed = QtGui.QCheckBox(self.tabSystem)
        self.chkSystemMarkViewed.setObjectName(_fromUtf8("chkSystemMarkViewed"))
        self.gridLayout_2.addWidget(self.chkSystemMarkViewed, 4, 1, 1, 1)
        self.tabInformer.addTab(self.tabSystem, _fromUtf8(""))
        self.tabExternal = QtGui.QWidget()
        self.tabExternal.setObjectName(_fromUtf8("tabExternal"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabExternal)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblExternalEvent = CTableView(self.tabExternal)
        self.tblExternalEvent.setObjectName(_fromUtf8("tblExternalEvent"))
        self.gridLayout_3.addWidget(self.tblExternalEvent, 0, 0, 1, 2)
        self.chkExternalMarkViewed = QtGui.QCheckBox(self.tabExternal)
        self.chkExternalMarkViewed.setObjectName(_fromUtf8("chkExternalMarkViewed"))
        self.gridLayout_3.addWidget(self.chkExternalMarkViewed, 1, 0, 1, 1)
        self.chkExternalShowEventsClosed = QtGui.QCheckBox(self.tabExternal)
        self.chkExternalShowEventsClosed.setObjectName(_fromUtf8("chkExternalShowEventsClosed"))
        self.gridLayout_3.addWidget(self.chkExternalShowEventsClosed, 1, 1, 1, 1)
        self.tabInformer.addTab(self.tabExternal, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabInformer, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InformerPage)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(InformerPage)
        self.tabInformer.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(InformerPage)
        InformerPage.setTabOrder(self.tabInformer, self.buttonBox)
        InformerPage.setTabOrder(self.buttonBox, self.edtSystemText)
        InformerPage.setTabOrder(self.edtSystemText, self.chkSystemMarkViewed)
        InformerPage.setTabOrder(self.chkSystemMarkViewed, self.systemButtonBox)
        InformerPage.setTabOrder(self.systemButtonBox, self.tblExternalEvent)
        InformerPage.setTabOrder(self.tblExternalEvent, self.chkExternalMarkViewed)
        InformerPage.setTabOrder(self.chkExternalMarkViewed, self.chkExternalShowEventsClosed)

    def retranslateUi(self, InformerPage):
        InformerPage.setWindowTitle(_translate("InformerPage", "ChangeMe!", None))
        self.lblSystemCreatePerson.setText(_translate("InformerPage", "Автор", None))
        self.lblSystemCreateDatetime.setText(_translate("InformerPage", "Дата", None))
        self.lblSystemSubject.setText(_translate("InformerPage", "Тема", None))
        self.lblSystemText.setText(_translate("InformerPage", "Текст", None))
        self.chkSystemMarkViewed.setText(_translate("InformerPage", "я ознакомлен(а)", None))
        self.tabInformer.setTabText(self.tabInformer.indexOf(self.tabSystem), _translate("InformerPage", "Системные", None))
        self.chkExternalMarkViewed.setText(_translate("InformerPage", "закрыть уведомления", None))
        self.chkExternalShowEventsClosed.setText(_translate("InformerPage", "показать закрытые уведомления", None))
        self.tabInformer.setTabText(self.tabInformer.indexOf(self.tabExternal), _translate("InformerPage", "Внешние", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InformerPage = QtGui.QDialog()
    ui = Ui_InformerPage()
    ui.setupUi(InformerPage)
    InformerPage.show()
    sys.exit(app.exec_())

