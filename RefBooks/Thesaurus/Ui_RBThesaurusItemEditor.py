# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBThesaurusItemEditor.ui'
#
# Created: Wed Feb 19 22:52:40 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ThesaurusItemEditorDialog(object):
    def setupUi(self, ThesaurusItemEditorDialog):
        ThesaurusItemEditorDialog.setObjectName(_fromUtf8("ThesaurusItemEditorDialog"))
        ThesaurusItemEditorDialog.resize(320, 119)
        ThesaurusItemEditorDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ThesaurusItemEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(ThesaurusItemEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblTemplate = QtGui.QLabel(ThesaurusItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTemplate.sizePolicy().hasHeightForWidth())
        self.lblTemplate.setSizePolicy(sizePolicy)
        self.lblTemplate.setObjectName(_fromUtf8("lblTemplate"))
        self.gridlayout.addWidget(self.lblTemplate, 2, 0, 1, 1)
        self.lblCode = QtGui.QLabel(ThesaurusItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtTemplate = QtGui.QLineEdit(ThesaurusItemEditorDialog)
        self.edtTemplate.setMinimumSize(QtCore.QSize(200, 0))
        self.edtTemplate.setObjectName(_fromUtf8("edtTemplate"))
        self.gridlayout.addWidget(self.edtTemplate, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(73, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblName = QtGui.QLabel(ThesaurusItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(ThesaurusItemEditorDialog)
        self.edtName.setMinimumSize(QtCore.QSize(200, 0))
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ThesaurusItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblTemplate.setBuddy(self.edtTemplate)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(ThesaurusItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ThesaurusItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ThesaurusItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ThesaurusItemEditorDialog)
        ThesaurusItemEditorDialog.setTabOrder(self.edtCode, self.edtName)
        ThesaurusItemEditorDialog.setTabOrder(self.edtName, self.edtTemplate)

    def retranslateUi(self, ThesaurusItemEditorDialog):
        ThesaurusItemEditorDialog.setWindowTitle(QtGui.QApplication.translate("ThesaurusItemEditorDialog", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTemplate.setText(QtGui.QApplication.translate("ThesaurusItemEditorDialog", "&Шаблон", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("ThesaurusItemEditorDialog", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("ThesaurusItemEditorDialog", "На&именование", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ThesaurusItemEditorDialog = QtGui.QDialog()
    ui = Ui_ThesaurusItemEditorDialog()
    ui.setupUi(ThesaurusItemEditorDialog)
    ThesaurusItemEditorDialog.show()
    sys.exit(app.exec_())

