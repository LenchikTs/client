# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\Nomenclature\NomenclatureFillMNNDialog.ui'
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

class Ui_NomenclatureFillMNNDialog(object):
    def setupUi(self, NomenclatureFillMNNDialog):
        NomenclatureFillMNNDialog.setObjectName(_fromUtf8("NomenclatureFillMNNDialog"))
        NomenclatureFillMNNDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(NomenclatureFillMNNDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblSelectedValueMNN = CTableView(NomenclatureFillMNNDialog)
        self.tblSelectedValueMNN.setObjectName(_fromUtf8("tblSelectedValueMNN"))
        self.gridLayout.addWidget(self.tblSelectedValueMNN, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NomenclatureFillMNNDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NomenclatureFillMNNDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NomenclatureFillMNNDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NomenclatureFillMNNDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NomenclatureFillMNNDialog)

    def retranslateUi(self, NomenclatureFillMNNDialog):
        NomenclatureFillMNNDialog.setWindowTitle(_translate("NomenclatureFillMNNDialog", "Выберите значение МНН", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NomenclatureFillMNNDialog = QtGui.QDialog()
    ui = Ui_NomenclatureFillMNNDialog()
    ui.setupUi(NomenclatureFillMNNDialog)
    NomenclatureFillMNNDialog.show()
    sys.exit(app.exec_())

