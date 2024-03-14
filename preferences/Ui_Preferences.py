# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/preferences/Preferences.ui'
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

class Ui_preferencesDialog(object):
    def setupUi(self, preferencesDialog):
        preferencesDialog.setObjectName(_fromUtf8("preferencesDialog"))
        preferencesDialog.resize(461, 278)
        self.verticalLayout = QtGui.QVBoxLayout(preferencesDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(preferencesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pagesList = QtGui.QListWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pagesList.sizePolicy().hasHeightForWidth())
        self.pagesList.setSizePolicy(sizePolicy)
        self.pagesList.setResizeMode(QtGui.QListView.Adjust)
        self.pagesList.setViewMode(QtGui.QListView.ListMode)
        self.pagesList.setSelectionRectVisible(False)
        self.pagesList.setObjectName(_fromUtf8("pagesList"))
        self.pagesHolder = QtGui.QStackedWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pagesHolder.sizePolicy().hasHeightForWidth())
        self.pagesHolder.setSizePolicy(sizePolicy)
        self.pagesHolder.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pagesHolder.setFrameShadow(QtGui.QFrame.Sunken)
        self.pagesHolder.setLineWidth(1)
        self.pagesHolder.setObjectName(_fromUtf8("pagesHolder"))
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(preferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(preferencesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), preferencesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), preferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(preferencesDialog)

    def retranslateUi(self, preferencesDialog):
        preferencesDialog.setWindowTitle(_translate("preferencesDialog", "Предпочтения", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    preferencesDialog = QtGui.QDialog()
    ui = Ui_preferencesDialog()
    ui.setupUi(preferencesDialog)
    preferencesDialog.show()
    sys.exit(app.exec_())

