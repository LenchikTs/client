# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Registry/ProphylaxisPlanningMarksDialog.ui'
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

class Ui_ProphylaxisPlanningMarksDialog(object):
    def setupUi(self, ProphylaxisPlanningMarksDialog):
        ProphylaxisPlanningMarksDialog.setObjectName(_fromUtf8("ProphylaxisPlanningMarksDialog"))
        ProphylaxisPlanningMarksDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ProphylaxisPlanningMarksDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkProcessed = QtGui.QCheckBox(ProphylaxisPlanningMarksDialog)
        self.chkProcessed.setText(_fromUtf8(""))
        self.chkProcessed.setObjectName(_fromUtf8("chkProcessed"))
        self.gridLayout.addWidget(self.chkProcessed, 0, 1, 1, 1)
        self.cmbNotified = QtGui.QComboBox(ProphylaxisPlanningMarksDialog)
        self.cmbNotified.setObjectName(_fromUtf8("cmbNotified"))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbNotified, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProphylaxisPlanningMarksDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.edtNote = QtGui.QPlainTextEdit(ProphylaxisPlanningMarksDialog)
        self.edtNote.setTabChangesFocus(True)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 2, 1, 3, 2)
        self.label = QtGui.QLabel(ProphylaxisPlanningMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lblProcessed = QtGui.QLabel(ProphylaxisPlanningMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProcessed.sizePolicy().hasHeightForWidth())
        self.lblProcessed.setSizePolicy(sizePolicy)
        self.lblProcessed.setObjectName(_fromUtf8("lblProcessed"))
        self.gridLayout.addWidget(self.lblProcessed, 0, 0, 1, 1)
        self.lblNote = QtGui.QLabel(ProphylaxisPlanningMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblNote.sizePolicy().hasHeightForWidth())
        self.lblNote.setSizePolicy(sizePolicy)
        self.lblNote.setMinimumSize(QtCore.QSize(0, 25))
        self.lblNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.label.setBuddy(self.cmbNotified)
        self.lblProcessed.setBuddy(self.chkProcessed)
        self.lblNote.setBuddy(self.edtNote)

        self.retranslateUi(ProphylaxisPlanningMarksDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProphylaxisPlanningMarksDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProphylaxisPlanningMarksDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProphylaxisPlanningMarksDialog)
        ProphylaxisPlanningMarksDialog.setTabOrder(self.chkProcessed, self.cmbNotified)
        ProphylaxisPlanningMarksDialog.setTabOrder(self.cmbNotified, self.edtNote)
        ProphylaxisPlanningMarksDialog.setTabOrder(self.edtNote, self.buttonBox)

    def retranslateUi(self, ProphylaxisPlanningMarksDialog):
        ProphylaxisPlanningMarksDialog.setWindowTitle(_translate("ProphylaxisPlanningMarksDialog", "Dialog", None))
        self.cmbNotified.setItemText(0, _translate("ProphylaxisPlanningMarksDialog", "Нет", None))
        self.cmbNotified.setItemText(1, _translate("ProphylaxisPlanningMarksDialog", "По телефону", None))
        self.cmbNotified.setItemText(2, _translate("ProphylaxisPlanningMarksDialog", "СМС", None))
        self.cmbNotified.setItemText(3, _translate("ProphylaxisPlanningMarksDialog", "Эл.почтой", None))
        self.label.setText(_translate("ProphylaxisPlanningMarksDialog", "&Извещён", None))
        self.lblProcessed.setText(_translate("ProphylaxisPlanningMarksDialog", "&Отработан", None))
        self.lblNote.setText(_translate("ProphylaxisPlanningMarksDialog", "&Примечание", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProphylaxisPlanningMarksDialog = QtGui.QDialog()
    ui = Ui_ProphylaxisPlanningMarksDialog()
    ui.setupUi(ProphylaxisPlanningMarksDialog)
    ProphylaxisPlanningMarksDialog.show()
    sys.exit(app.exec_())

