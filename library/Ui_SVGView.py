# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\SVGView.ui'
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

class Ui_SVGViewDialog(object):
    def setupUi(self, SVGViewDialog):
        SVGViewDialog.setObjectName(_fromUtf8("SVGViewDialog"))
        SVGViewDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SVGViewDialog.resize(640, 605)
        SVGViewDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(SVGViewDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView = QtGui.QGraphicsView(SVGViewDialog)
        self.graphicsView.setRenderHints(QtGui.QPainter.TextAntialiasing)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 2, 3)
        self.grpPager = QtGui.QWidget(SVGViewDialog)
        self.grpPager.setEnabled(False)
        self.grpPager.setObjectName(_fromUtf8("grpPager"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.grpPager)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnFirstPage = QtGui.QToolButton(self.grpPager)
        self.btnFirstPage.setText(_fromUtf8(""))
        self.btnFirstPage.setObjectName(_fromUtf8("btnFirstPage"))
        self.horizontalLayout.addWidget(self.btnFirstPage)
        self.edtPageNum = QtGui.QSpinBox(self.grpPager)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPageNum.sizePolicy().hasHeightForWidth())
        self.edtPageNum.setSizePolicy(sizePolicy)
        self.edtPageNum.setObjectName(_fromUtf8("edtPageNum"))
        self.horizontalLayout.addWidget(self.edtPageNum)
        self.btnLastPage = QtGui.QToolButton(self.grpPager)
        self.btnLastPage.setText(_fromUtf8(""))
        self.btnLastPage.setObjectName(_fromUtf8("btnLastPage"))
        self.horizontalLayout.addWidget(self.btnLastPage)
        self.gridLayout.addWidget(self.grpPager, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SVGViewDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        self.label = QtGui.QLabel(SVGViewDialog)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.retranslateUi(SVGViewDialog)
        QtCore.QMetaObject.connectSlotsByName(SVGViewDialog)
        SVGViewDialog.setTabOrder(self.graphicsView, self.btnFirstPage)
        SVGViewDialog.setTabOrder(self.btnFirstPage, self.edtPageNum)
        SVGViewDialog.setTabOrder(self.edtPageNum, self.btnLastPage)
        SVGViewDialog.setTabOrder(self.btnLastPage, self.buttonBox)

    def retranslateUi(self, SVGViewDialog):
        SVGViewDialog.setWindowTitle(_translate("SVGViewDialog", "просмотр отчёта", None))
        self.label.setToolTip(_translate("SVGViewDialog", "Для сдвига текста используйте клавиши wasd", None))

