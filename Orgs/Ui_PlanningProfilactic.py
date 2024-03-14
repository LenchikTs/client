# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\PlanningProfilactic.ui'
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

class Ui_PlanningProfilactic(object):
    def setupUi(self, PlanningProfilactic):
        PlanningProfilactic.setObjectName(_fromUtf8("PlanningProfilactic"))
        PlanningProfilactic.resize(368, 154)
        self.gridLayout = QtGui.QGridLayout(PlanningProfilactic)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 5, 1, 1)
        self.btnClose = QtGui.QPushButton(PlanningProfilactic)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 6, 4, 1, 1)
        self.btnStart = QtGui.QPushButton(PlanningProfilactic)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 6, 0, 1, 3)
        self.lblOrgStructure = QtGui.QLabel(PlanningProfilactic)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 0, 0, 1, 1)
        self.chkAddDispExempts = QtGui.QCheckBox(PlanningProfilactic)
        self.chkAddDispExempts.setObjectName(_fromUtf8("chkAddDispExempts"))
        self.gridLayout.addWidget(self.chkAddDispExempts, 3, 0, 1, 5)
        self.sbYear = QtGui.QSpinBox(PlanningProfilactic)
        self.sbYear.setMinimum(2017)
        self.sbYear.setMaximum(2099)
        self.sbYear.setObjectName(_fromUtf8("sbYear"))
        self.gridLayout.addWidget(self.sbYear, 0, 1, 1, 2)
        self.chkAddDisp = QtGui.QCheckBox(PlanningProfilactic)
        self.chkAddDisp.setChecked(True)
        self.chkAddDisp.setObjectName(_fromUtf8("chkAddDisp"))
        self.gridLayout.addWidget(self.chkAddDisp, 1, 0, 1, 5)
        self.chkAddProf = QtGui.QCheckBox(PlanningProfilactic)
        self.chkAddProf.setChecked(True)
        self.chkAddProf.setObjectName(_fromUtf8("chkAddProf"))
        self.gridLayout.addWidget(self.chkAddProf, 4, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)

        self.retranslateUi(PlanningProfilactic)
        QtCore.QMetaObject.connectSlotsByName(PlanningProfilactic)

    def retranslateUi(self, PlanningProfilactic):
        PlanningProfilactic.setWindowTitle(_translate("PlanningProfilactic", "Планирование профилактических мероприятий", None))
        self.btnClose.setText(_translate("PlanningProfilactic", "Закрыть", None))
        self.btnStart.setText(_translate("PlanningProfilactic", "Начать", None))
        self.lblOrgStructure.setText(_translate("PlanningProfilactic", "год", None))
        self.chkAddDispExempts.setText(_translate("PlanningProfilactic", "Включать диспан. фед. льготников", None))
        self.chkAddDisp.setText(_translate("PlanningProfilactic", "Включать диспан. по возрастам", None))
        self.chkAddProf.setText(_translate("PlanningProfilactic", "Включать профилактич. осмотры", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlanningProfilactic = QtGui.QDialog()
    ui = Ui_PlanningProfilactic()
    ui.setupUi(PlanningProfilactic)
    PlanningProfilactic.show()
    sys.exit(app.exec_())

