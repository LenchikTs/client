# -*- coding: utf-8 -*-

from PyQt4              import QtGui
from Ui_SMPAddEventDialog  import Ui_Dialog

class CSMPAddEventDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def exec_(self):
        self.edtNote.clear()
        return QtGui.QDialog.exec_(self)

    def eventTypeId(self):
        return self.cmbEventType.itemData(self.cmbEventType.currentIndex()).toInt()[0]
        
    def note(self):
        return unicode(self.edtNote.text())
