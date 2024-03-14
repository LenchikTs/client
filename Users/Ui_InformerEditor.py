# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\py\s11-svn\Users\InformerEditor.ui'
#
# Created: Mon Apr 27 18:55:48 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_InformerMessageEditorDialog(object):
    def setupUi(self, InformerMessageEditorDialog):
        InformerMessageEditorDialog.setObjectName("InformerMessageEditorDialog")
        InformerMessageEditorDialog.resize(514, 356)
        InformerMessageEditorDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(InformerMessageEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.lblSubject = QtGui.QLabel(InformerMessageEditorDialog)
        self.lblSubject.setObjectName("lblSubject")
        self.gridLayout.addWidget(self.lblSubject, 0, 0, 1, 1)
        self.edtSubject = QtGui.QLineEdit(InformerMessageEditorDialog)
        self.edtSubject.setObjectName("edtSubject")
        self.gridLayout.addWidget(self.edtSubject, 0, 1, 1, 1)
        self.lblText = QtGui.QLabel(InformerMessageEditorDialog)
        self.lblText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblText.setObjectName("lblText")
        self.gridLayout.addWidget(self.lblText, 1, 0, 1, 1)
        self.edtText = QtGui.QTextEdit(InformerMessageEditorDialog)
        self.edtText.setObjectName("edtText")
        self.gridLayout.addWidget(self.edtText, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InformerMessageEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.lblSubject.setBuddy(self.edtSubject)
        self.lblText.setBuddy(self.edtText)

        self.retranslateUi(InformerMessageEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), InformerMessageEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), InformerMessageEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InformerMessageEditorDialog)
        InformerMessageEditorDialog.setTabOrder(self.edtSubject, self.edtText)
        InformerMessageEditorDialog.setTabOrder(self.edtText, self.buttonBox)

    def retranslateUi(self, InformerMessageEditorDialog):
        InformerMessageEditorDialog.setWindowTitle(QtGui.QApplication.translate("InformerMessageEditorDialog", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSubject.setText(QtGui.QApplication.translate("InformerMessageEditorDialog", "&Тема", None, QtGui.QApplication.UnicodeUTF8))
        self.lblText.setText(QtGui.QApplication.translate("InformerMessageEditorDialog", "&Сообщение", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InformerMessageEditorDialog = QtGui.QDialog()
    ui = Ui_InformerMessageEditorDialog()
    ui.setupUi(InformerMessageEditorDialog)
    InformerMessageEditorDialog.show()
    sys.exit(app.exec_())

