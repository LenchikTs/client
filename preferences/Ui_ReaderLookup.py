# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/preferences/ReaderLookup.ui'
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

class Ui_readerLookup(object):
    def setupUi(self, readerLookup):
        readerLookup.setObjectName(_fromUtf8("readerLookup"))
        readerLookup.resize(326, 97)
        self.gridLayout = QtGui.QGridLayout(readerLookup)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pnlAtr = QtGui.QLabel(readerLookup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlAtr.sizePolicy().hasHeightForWidth())
        self.pnlAtr.setSizePolicy(sizePolicy)
        self.pnlAtr.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlAtr.setFrameShadow(QtGui.QFrame.Sunken)
        self.pnlAtr.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.pnlAtr.setObjectName(_fromUtf8("pnlAtr"))
        self.gridLayout.addWidget(self.pnlAtr, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblReader = QtGui.QLabel(readerLookup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReader.sizePolicy().hasHeightForWidth())
        self.lblReader.setSizePolicy(sizePolicy)
        self.lblReader.setObjectName(_fromUtf8("lblReader"))
        self.gridLayout.addWidget(self.lblReader, 1, 0, 1, 1)
        self.pnlReader = QtGui.QLabel(readerLookup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlReader.sizePolicy().hasHeightForWidth())
        self.pnlReader.setSizePolicy(sizePolicy)
        self.pnlReader.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlReader.setFrameShadow(QtGui.QFrame.Sunken)
        self.pnlReader.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.pnlReader.setObjectName(_fromUtf8("pnlReader"))
        self.gridLayout.addWidget(self.pnlReader, 1, 1, 1, 1)
        self.lblAtr = QtGui.QLabel(readerLookup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAtr.sizePolicy().hasHeightForWidth())
        self.lblAtr.setSizePolicy(sizePolicy)
        self.lblAtr.setObjectName(_fromUtf8("lblAtr"))
        self.gridLayout.addWidget(self.lblAtr, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(readerLookup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblInstruction = QtGui.QLabel(readerLookup)
        self.lblInstruction.setText(_fromUtf8(""))
        self.lblInstruction.setObjectName(_fromUtf8("lblInstruction"))
        self.gridLayout.addWidget(self.lblInstruction, 0, 0, 1, 2)

        self.retranslateUi(readerLookup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), readerLookup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), readerLookup.reject)
        QtCore.QMetaObject.connectSlotsByName(readerLookup)

    def retranslateUi(self, readerLookup):
        readerLookup.setWindowTitle(_translate("readerLookup", "Определение считывателя смарт-карты", None))
        self.pnlAtr.setText(_translate("readerLookup", "-", None))
        self.lblReader.setText(_translate("readerLookup", "Считыватель", None))
        self.pnlReader.setText(_translate("readerLookup", "-", None))
        self.lblAtr.setText(_translate("readerLookup", "ATR карты", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    readerLookup = QtGui.QDialog()
    ui = Ui_readerLookup()
    ui.setupUi(readerLookup)
    readerLookup.show()
    sys.exit(app.exec_())

