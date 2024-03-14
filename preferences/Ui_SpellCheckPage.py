# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/preferences/SpellCheckPage.ui'
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

class Ui_spellCheckPage(object):
    def setupUi(self, spellCheckPage):
        spellCheckPage.setObjectName(_fromUtf8("spellCheckPage"))
        spellCheckPage.setEnabled(True)
        spellCheckPage.resize(740, 430)
        spellCheckPage.setMouseTracking(False)
        self.gridLayout = QtGui.QGridLayout(spellCheckPage)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnSelectPathToPersonalDict = QtGui.QToolButton(spellCheckPage)
        self.btnSelectPathToPersonalDict.setObjectName(_fromUtf8("btnSelectPathToPersonalDict"))
        self.gridLayout.addWidget(self.btnSelectPathToPersonalDict, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 337, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.edtPathToPersonalDict = QtGui.QLineEdit(spellCheckPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPathToPersonalDict.sizePolicy().hasHeightForWidth())
        self.edtPathToPersonalDict.setSizePolicy(sizePolicy)
        self.edtPathToPersonalDict.setObjectName(_fromUtf8("edtPathToPersonalDict"))
        self.gridLayout.addWidget(self.edtPathToPersonalDict, 1, 1, 1, 1)
        self.chkSpellCheckHighlight = QtGui.QCheckBox(spellCheckPage)
        self.chkSpellCheckHighlight.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSpellCheckHighlight.sizePolicy().hasHeightForWidth())
        self.chkSpellCheckHighlight.setSizePolicy(sizePolicy)
        self.chkSpellCheckHighlight.setMouseTracking(True)
        self.chkSpellCheckHighlight.setText(_fromUtf8(""))
        self.chkSpellCheckHighlight.setObjectName(_fromUtf8("chkSpellCheckHighlight"))
        self.gridLayout.addWidget(self.chkSpellCheckHighlight, 0, 1, 1, 1)
        self.lblPathToPersonalDict = QtGui.QLabel(spellCheckPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPathToPersonalDict.sizePolicy().hasHeightForWidth())
        self.lblPathToPersonalDict.setSizePolicy(sizePolicy)
        self.lblPathToPersonalDict.setObjectName(_fromUtf8("lblPathToPersonalDict"))
        self.gridLayout.addWidget(self.lblPathToPersonalDict, 1, 0, 1, 1)
        self.lblPathToPersonalDict_2 = QtGui.QLabel(spellCheckPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPathToPersonalDict_2.sizePolicy().hasHeightForWidth())
        self.lblPathToPersonalDict_2.setSizePolicy(sizePolicy)
        self.lblPathToPersonalDict_2.setObjectName(_fromUtf8("lblPathToPersonalDict_2"))
        self.gridLayout.addWidget(self.lblPathToPersonalDict_2, 0, 0, 1, 1)
        self.btnEditPersonalDict = QtGui.QPushButton(spellCheckPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEditPersonalDict.sizePolicy().hasHeightForWidth())
        self.btnEditPersonalDict.setSizePolicy(sizePolicy)
        self.btnEditPersonalDict.setObjectName(_fromUtf8("btnEditPersonalDict"))
        self.gridLayout.addWidget(self.btnEditPersonalDict, 2, 1, 1, 1)

        self.retranslateUi(spellCheckPage)
        QtCore.QMetaObject.connectSlotsByName(spellCheckPage)

    def retranslateUi(self, spellCheckPage):
        spellCheckPage.setWindowTitle(_translate("spellCheckPage", "Проверка правописания", None))
        self.btnSelectPathToPersonalDict.setText(_translate("spellCheckPage", "...", None))
        self.lblPathToPersonalDict.setText(_translate("spellCheckPage", "Выбрать пользовательский словарь", None))
        self.lblPathToPersonalDict_2.setText(_translate("spellCheckPage", "Разрешить проверку правописания", None))
        self.btnEditPersonalDict.setText(_translate("spellCheckPage", "Редактировать пользовательский словарь", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    spellCheckPage = QtGui.QWidget()
    ui = Ui_spellCheckPage()
    ui.setupUi(spellCheckPage)
    spellCheckPage.show()
    sys.exit(app.exec_())

