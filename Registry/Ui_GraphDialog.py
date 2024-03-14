# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Registry/GraphDialog.ui'
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

class Ui_GraphDialog(object):
    def setupUi(self, GraphDialog):
        GraphDialog.setObjectName(_fromUtf8("GraphDialog"))
        GraphDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        GraphDialog.resize(652, 566)
        GraphDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(GraphDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grpPager = QtGui.QWidget(GraphDialog)
        self.grpPager.setEnabled(False)
        self.grpPager.setObjectName(_fromUtf8("grpPager"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.grpPager)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnFirstPage = QtGui.QToolButton(self.grpPager)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnFirstPage.setFont(font)
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
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnLastPage.setFont(font)
        self.btnLastPage.setObjectName(_fromUtf8("btnLastPage"))
        self.horizontalLayout.addWidget(self.btnLastPage)
        self.gridLayout.addWidget(self.grpPager, 2, 0, 1, 1)
        self.chkMonth = QtGui.QCheckBox(GraphDialog)
        self.chkMonth.setObjectName(_fromUtf8("chkMonth"))
        self.gridLayout.addWidget(self.chkMonth, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.label = QtGui.QLabel(GraphDialog)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.graphicsView = CGraphView(GraphDialog)
        self.graphicsView.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 6)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblProperty = QtGui.QLabel(GraphDialog)
        self.lblProperty.setObjectName(_fromUtf8("lblProperty"))
        self.horizontalLayout_2.addWidget(self.lblProperty)
        self.cmbPropertyType = CPropertyComboBox(GraphDialog)
        self.cmbPropertyType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.cmbPropertyType.setObjectName(_fromUtf8("cmbPropertyType"))
        self.horizontalLayout_2.addWidget(self.cmbPropertyType)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(GraphDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Retry|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 4)
        self.lblCurrentYear = QtGui.QLabel(GraphDialog)
        self.lblCurrentYear.setText(_fromUtf8(""))
        self.lblCurrentYear.setObjectName(_fromUtf8("lblCurrentYear"))
        self.gridLayout.addWidget(self.lblCurrentYear, 0, 4, 1, 1)

        self.retranslateUi(GraphDialog)
        QtCore.QMetaObject.connectSlotsByName(GraphDialog)
        GraphDialog.setTabOrder(self.cmbPropertyType, self.chkMonth)
        GraphDialog.setTabOrder(self.chkMonth, self.graphicsView)
        GraphDialog.setTabOrder(self.graphicsView, self.btnFirstPage)
        GraphDialog.setTabOrder(self.btnFirstPage, self.edtPageNum)
        GraphDialog.setTabOrder(self.edtPageNum, self.btnLastPage)

    def retranslateUi(self, GraphDialog):
        GraphDialog.setWindowTitle(_translate("GraphDialog", "График", None))
        self.btnFirstPage.setText(_translate("GraphDialog", "<<", None))
        self.btnLastPage.setText(_translate("GraphDialog", ">>", None))
        self.chkMonth.setText(_translate("GraphDialog", "По месяцам", None))
        self.label.setToolTip(_translate("GraphDialog", "Для сдвига текста используйте клавиши wasd", None))
        self.lblProperty.setText(_translate("GraphDialog", "Свойство", None))

from Events.PropertyComboBox import CPropertyComboBox
from Registry.GraphView import CGraphView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GraphDialog = QtGui.QDialog()
    ui = Ui_GraphDialog()
    ui.setupUi(GraphDialog)
    GraphDialog.show()
    sys.exit(app.exec_())

