# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\angel.ui'
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

class Ui_AngelDialog(object):
    def setupUi(self, AngelDialog):
        AngelDialog.setObjectName(_fromUtf8("AngelDialog"))
        AngelDialog.resize(735, 626)
        self.gridLayout = QtGui.QGridLayout(AngelDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnRect = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRect.sizePolicy().hasHeightForWidth())
        self.btnRect.setSizePolicy(sizePolicy)
        self.btnRect.setCheckable(True)
        self.btnRect.setChecked(True)
        self.btnRect.setAutoExclusive(False)
        self.btnRect.setObjectName(_fromUtf8("btnRect"))
        self.verticalLayout.addWidget(self.btnRect)
        self.btnEllipse = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEllipse.sizePolicy().hasHeightForWidth())
        self.btnEllipse.setSizePolicy(sizePolicy)
        self.btnEllipse.setCheckable(True)
        self.btnEllipse.setAutoExclusive(False)
        self.btnEllipse.setObjectName(_fromUtf8("btnEllipse"))
        self.verticalLayout.addWidget(self.btnEllipse)
        self.btnText = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnText.sizePolicy().hasHeightForWidth())
        self.btnText.setSizePolicy(sizePolicy)
        self.btnText.setCheckable(True)
        self.btnText.setAutoExclusive(False)
        self.btnText.setObjectName(_fromUtf8("btnText"))
        self.verticalLayout.addWidget(self.btnText)
        self.btnCross = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCross.sizePolicy().hasHeightForWidth())
        self.btnCross.setSizePolicy(sizePolicy)
        self.btnCross.setCheckable(True)
        self.btnCross.setAutoExclusive(False)
        self.btnCross.setAutoRaise(False)
        self.btnCross.setObjectName(_fromUtf8("btnCross"))
        self.verticalLayout.addWidget(self.btnCross)
        self.btnSave = QtGui.QPushButton(AngelDialog)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.verticalLayout.addWidget(self.btnSave)
        self.btnLoad = QtGui.QPushButton(AngelDialog)
        self.btnLoad.setObjectName(_fromUtf8("btnLoad"))
        self.verticalLayout.addWidget(self.btnLoad)
        self.btnHelp = QtGui.QPushButton(AngelDialog)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.verticalLayout.addWidget(self.btnHelp)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lblItemInfo = QtGui.QLabel(AngelDialog)
        self.lblItemInfo.setObjectName(_fromUtf8("lblItemInfo"))
        self.verticalLayout.addWidget(self.lblItemInfo)
        self.lblColour = QtGui.QLabel(AngelDialog)
        self.lblColour.setText(_fromUtf8(""))
        self.lblColour.setObjectName(_fromUtf8("lblColour"))
        self.verticalLayout.addWidget(self.lblColour)
        spacerItem1 = QtGui.QSpacerItem(20, 148, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.btnBlack = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBlack.sizePolicy().hasHeightForWidth())
        self.btnBlack.setSizePolicy(sizePolicy)
        self.btnBlack.setCheckable(True)
        self.btnBlack.setChecked(True)
        self.btnBlack.setObjectName(_fromUtf8("btnBlack"))
        self.verticalLayout.addWidget(self.btnBlack)
        self.btnYellow = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnYellow.sizePolicy().hasHeightForWidth())
        self.btnYellow.setSizePolicy(sizePolicy)
        self.btnYellow.setCheckable(True)
        self.btnYellow.setObjectName(_fromUtf8("btnYellow"))
        self.verticalLayout.addWidget(self.btnYellow)
        self.btnRed = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRed.sizePolicy().hasHeightForWidth())
        self.btnRed.setSizePolicy(sizePolicy)
        self.btnRed.setCheckable(True)
        self.btnRed.setObjectName(_fromUtf8("btnRed"))
        self.verticalLayout.addWidget(self.btnRed)
        self.btnBlue = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBlue.sizePolicy().hasHeightForWidth())
        self.btnBlue.setSizePolicy(sizePolicy)
        self.btnBlue.setCheckable(True)
        self.btnBlue.setObjectName(_fromUtf8("btnBlue"))
        self.verticalLayout.addWidget(self.btnBlue)
        self.btnGreen = QtGui.QToolButton(AngelDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGreen.sizePolicy().hasHeightForWidth())
        self.btnGreen.setSizePolicy(sizePolicy)
        self.btnGreen.setCheckable(True)
        self.btnGreen.setObjectName(_fromUtf8("btnGreen"))
        self.verticalLayout.addWidget(self.btnGreen)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsView = QtGui.QGraphicsView(AngelDialog)
        self.graphicsView.setFrameShape(QtGui.QFrame.StyledPanel)
        self.graphicsView.setInteractive(True)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnPrint = QtGui.QPushButton(AngelDialog)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.horizontalLayout.addWidget(self.btnPrint)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(AngelDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.retranslateUi(AngelDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AngelDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AngelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AngelDialog)

    def retranslateUi(self, AngelDialog):
        AngelDialog.setWindowTitle(_translate("AngelDialog", "Dialog", None))
        self.btnRect.setText(_translate("AngelDialog", "[]", None))
        self.btnEllipse.setText(_translate("AngelDialog", "O", None))
        self.btnText.setText(_translate("AngelDialog", "Текст", None))
        self.btnCross.setText(_translate("AngelDialog", "x", None))
        self.btnSave.setText(_translate("AngelDialog", "Сохранить", None))
        self.btnLoad.setText(_translate("AngelDialog", "Загрузить", None))
        self.btnHelp.setText(_translate("AngelDialog", "Помощь", None))
        self.lblItemInfo.setText(_translate("AngelDialog", "Черный\n"
"Квадрат", None))
        self.btnBlack.setText(_translate("AngelDialog", "Черный", None))
        self.btnYellow.setText(_translate("AngelDialog", "Желтый", None))
        self.btnRed.setText(_translate("AngelDialog", "Красный", None))
        self.btnBlue.setText(_translate("AngelDialog", "Голубой", None))
        self.btnGreen.setText(_translate("AngelDialog", "Зеленый", None))
        self.btnPrint.setText(_translate("AngelDialog", "Печать", None))
