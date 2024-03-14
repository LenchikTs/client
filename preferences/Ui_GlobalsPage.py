# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/preferences/GlobalsPage.ui'
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

class Ui_globalsPage(object):
    def setupUi(self, globalsPage):
        globalsPage.setObjectName(_fromUtf8("globalsPage"))
        globalsPage.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(globalsPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblGlobal = CTableView(globalsPage)
        self.tblGlobal.setObjectName(_fromUtf8("tblGlobal"))
        self.gridLayout.addWidget(self.tblGlobal, 0, 0, 1, 1)

        self.retranslateUi(globalsPage)
        QtCore.QMetaObject.connectSlotsByName(globalsPage)

    def retranslateUi(self, globalsPage):
        globalsPage.setWindowTitle(_translate("globalsPage", "Глобальные настройки", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    globalsPage = QtGui.QWidget()
    ui = Ui_globalsPage()
    ui.setupUi(globalsPage)
    globalsPage.show()
    sys.exit(app.exec_())

