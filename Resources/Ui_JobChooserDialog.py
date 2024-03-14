# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\py\s11-svn\Resources\ResourceChooserDialog.ui'
#
# Created: Tue Nov 03 15:45:31 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ResourceChooserDialog(object):
    def setupUi(self, ResourceChooserDialog):
        ResourceChooserDialog.setObjectName("ResourceChooserDialog")
        ResourceChooserDialog.resize(606, 198)
        ResourceChooserDialog.setSizeGripEnabled(True)
        ResourceChooserDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ResourceChooserDialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(ResourceChooserDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.treeResourceTypes = QtGui.QTreeView(self.splitter)
        self.treeResourceTypes.setObjectName("treeResourceTypes")
        self.clnCalendar = CCalendarWidget(self.splitter)
        self.clnCalendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.clnCalendar.setGridVisible(False)
        self.clnCalendar.setVerticalHeaderFormat(QtGui.QCalendarWidget.ISOWeekNumbers)
        self.clnCalendar.setObjectName("clnCalendar")
        self.tblResources = CTableView(self.splitter)
        self.tblResources.setObjectName("tblResources")
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(ResourceChooserDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ResourceChooserDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ResourceChooserDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ResourceChooserDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ResourceChooserDialog)
        ResourceChooserDialog.setTabOrder(self.treeResourceTypes, self.clnCalendar)
        ResourceChooserDialog.setTabOrder(self.clnCalendar, self.tblResources)
        ResourceChooserDialog.setTabOrder(self.tblResources, self.buttonBox)

    def retranslateUi(self, ResourceChooserDialog):
        ResourceChooserDialog.setWindowTitle(QtGui.QApplication.translate("ResourceChooserDialog", "Выберите ресурс-дату-место", None, QtGui.QApplication.UnicodeUTF8))

from library.TableView import CTableView
from library.Calendar import CCalendarWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ResourceChooserDialog = QtGui.QDialog()
    ui = Ui_ResourceChooserDialog()
    ui.setupUi(ResourceChooserDialog)
    ResourceChooserDialog.show()
    sys.exit(app.exec_())

