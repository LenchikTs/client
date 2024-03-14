# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\ImageProcDialog.ui'
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

class Ui_ImageProcDialog(object):
    def setupUi(self, ImageProcDialog):
        ImageProcDialog.setObjectName(_fromUtf8("ImageProcDialog"))
        ImageProcDialog.resize(400, 300)
        ImageProcDialog.setSizeGripEnabled(True)
        ImageProcDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ImageProcDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grpView = QtGui.QGraphicsView(ImageProcDialog)
        self.grpView.setObjectName(_fromUtf8("grpView"))
        self.gridLayout.addWidget(self.grpView, 0, 0, 1, 1)
        self.scrSize = QtGui.QSlider(ImageProcDialog)
        self.scrSize.setMinimum(-10)
        self.scrSize.setMaximum(10)
        self.scrSize.setProperty("value", 0)
        self.scrSize.setOrientation(QtCore.Qt.Vertical)
        self.scrSize.setInvertedAppearance(False)
        self.scrSize.setTickPosition(QtGui.QSlider.TicksBelow)
        self.scrSize.setTickInterval(2)
        self.scrSize.setObjectName(_fromUtf8("scrSize"))
        self.gridLayout.addWidget(self.scrSize, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ImageProcDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(ImageProcDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ImageProcDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ImageProcDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImageProcDialog)
        ImageProcDialog.setTabOrder(self.grpView, self.scrSize)
        ImageProcDialog.setTabOrder(self.scrSize, self.buttonBox)

    def retranslateUi(self, ImageProcDialog):
        ImageProcDialog.setWindowTitle(_translate("ImageProcDialog", "Dialog", None))

