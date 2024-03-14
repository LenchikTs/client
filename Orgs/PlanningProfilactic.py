# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, SIGNAL

from library.Utils import forceInt

from Ui_PlanningProfilactic import Ui_PlanningProfilactic


class CPlanningProfilactic(QtGui.QDialog, Ui_PlanningProfilactic):
    def __init__(self,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.chkAddDisp, SIGNAL("stateChanged(int)"), self.chooseSomething)
        self.connect(self.chkAddDispExempts, SIGNAL("stateChanged(int)"), self.chooseSomething)
        self.connect(self.chkAddProf, SIGNAL("stateChanged(int)"), self.chooseSomething)
       
    def start(self):
        try:
            QtGui.qApp.setWaitCursor()
            db = QtGui.qApp.db
            year = self.sbYear.value()

            chkAddDisp = self.chkAddDisp.isChecked()
            chkAddDispExempts = self.chkAddDispExempts.isChecked()
            chkAddProf = self.chkAddProf.isChecked()
            stmt = 'call planningProfilactic(%d, %d, %d, %d, @count);'%(year, chkAddDisp, chkAddDispExempts, chkAddProf)
            query = db.query(stmt)
            stmt = 'select @count as cnt;'
            query = db.query(stmt)
            cnt = 0
            QtGui.qApp.restoreOverrideCursor()
            if query.first():
                record = query.record()
                cnt = forceInt(record.value('cnt'))
            QtGui.QMessageBox.information(self,
                                        u'Планирование завершено',
                                        u'Добавлено %d записей' % cnt,
                                        QtGui.QMessageBox.Ok)
        finally:
            QtGui.qApp.restoreOverrideCursor()
        

    @pyqtSignature('')
    def on_btnStart_clicked(self):
        self.start()
        
    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()
        
    def chooseSomething(self):
            self.btnStart.setEnabled(self.chkAddDisp.isChecked() or self.chkAddDispExempts.isChecked() or self.chkAddProf.isChecked())
