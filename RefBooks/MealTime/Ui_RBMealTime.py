# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBMealTime.ui'
#
# Created: Wed Feb 19 22:52:50 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBMealTime(object):
    def setupUi(self, RBMealTime):
        RBMealTime.setObjectName(_fromUtf8("RBMealTime"))
        RBMealTime.resize(320, 119)
        RBMealTime.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(RBMealTime)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(RBMealTime)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(RBMealTime)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblTime = QtGui.QLabel(RBMealTime)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTime.sizePolicy().hasHeightForWidth())
        self.lblTime.setSizePolicy(sizePolicy)
        self.lblTime.setObjectName(_fromUtf8("lblTime"))
        self.gridlayout.addWidget(self.lblTime, 2, 0, 1, 1)
        self.edtRangeTime = CTimeRangeEdit(RBMealTime)
        self.edtRangeTime.setObjectName(_fromUtf8("edtRangeTime"))
        self.gridlayout.addWidget(self.edtRangeTime, 2, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBMealTime)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(RBMealTime)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBMealTime)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblTime.setBuddy(self.edtRangeTime)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBMealTime)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBMealTime.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBMealTime.reject)
        QtCore.QMetaObject.connectSlotsByName(RBMealTime)
        RBMealTime.setTabOrder(self.edtCode, self.edtName)
        RBMealTime.setTabOrder(self.edtName, self.edtRangeTime)

    def retranslateUi(self, RBMealTime):
        RBMealTime.setWindowTitle(QtGui.QApplication.translate("RBMealTime", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTime.setText(QtGui.QApplication.translate("RBMealTime", "с / по", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBMealTime", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBMealTime", "&Код", None, QtGui.QApplication.UnicodeUTF8))

from library.TimeEdit import CTimeRangeEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBMealTime = QtGui.QDialog()
    ui = Ui_RBMealTime()
    ui.setupUi(RBMealTime)
    RBMealTime.show()
    sys.exit(app.exec_())

