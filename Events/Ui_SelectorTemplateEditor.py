# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Events/SelectorTemplateEditor.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_SelectorTemplateEditor(object):
    def setupUi(self, SelectorTemplateEditor):
        SelectorTemplateEditor.setObjectName(_fromUtf8("SelectorTemplateEditor"))
        SelectorTemplateEditor.resize(460, 122)
        self.gridLayout = QtGui.QGridLayout(SelectorTemplateEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.cmbAvailability = QtGui.QComboBox(SelectorTemplateEditor)
        self.cmbAvailability.setObjectName(_fromUtf8("cmbAvailability"))
        self.cmbAvailability.addItem(_fromUtf8(""))
        self.cmbAvailability.addItem(_fromUtf8(""))
        self.cmbAvailability.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAvailability, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SelectorTemplateEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblName = QtGui.QLabel(SelectorTemplateEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(SelectorTemplateEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(SelectorTemplateEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(SelectorTemplateEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblAvailability = QtGui.QLabel(SelectorTemplateEditor)
        self.lblAvailability.setObjectName(_fromUtf8("lblAvailability"))
        self.gridLayout.addWidget(self.lblAvailability, 2, 0, 1, 1)
        self.chkOffset = QtGui.QCheckBox(SelectorTemplateEditor)
        self.chkOffset.setObjectName(_fromUtf8("chkOffset"))
        self.gridLayout.addWidget(self.chkOffset, 3, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(SelectorTemplateEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectorTemplateEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectorTemplateEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectorTemplateEditor)
        SelectorTemplateEditor.setTabOrder(self.edtCode, self.edtName)
        SelectorTemplateEditor.setTabOrder(self.edtName, self.cmbAvailability)
        SelectorTemplateEditor.setTabOrder(self.cmbAvailability, self.chkOffset)
        SelectorTemplateEditor.setTabOrder(self.chkOffset, self.buttonBox)

    def retranslateUi(self, SelectorTemplateEditor):
        SelectorTemplateEditor.setWindowTitle(_translate("SelectorTemplateEditor", "Dialog", None))
        self.cmbAvailability.setItemText(0, _translate("SelectorTemplateEditor", "Всем", None))
        self.cmbAvailability.setItemText(1, _translate("SelectorTemplateEditor", "По специальности", None))
        self.cmbAvailability.setItemText(2, _translate("SelectorTemplateEditor", "Владельцу", None))
        self.lblName.setText(_translate("SelectorTemplateEditor", "&Наименование", None))
        self.lblCode.setText(_translate("SelectorTemplateEditor", "&Код", None))
        self.lblAvailability.setText(_translate("SelectorTemplateEditor", "Доступность", None))
        self.chkOffset.setText(_translate("SelectorTemplateEditor", "Учитывать хронологию", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SelectorTemplateEditor = QtGui.QDialog()
    ui = Ui_SelectorTemplateEditor()
    ui.setupUi(SelectorTemplateEditor)
    SelectorTemplateEditor.show()
    sys.exit(app.exec_())

