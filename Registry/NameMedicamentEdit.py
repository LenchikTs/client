# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

from library.Completer          import CStaticCompleterModel, CCompleter
from library.InDocTable         import CInDocTableCol


class CNameMedicamentEdit(QtGui.QLineEdit):
    seriesList = None

    def getSeriesList(self):
        if CNameMedicamentEdit.seriesList is None:
            db = QtGui.qApp.db
            result = []
            try:
                query = db.query('SELECT DISTINCT rbNomenclature.name FROM rbNomenclature ORDER BY rbNomenclature.name')
                while query.next():
                    result.append(query.value(0))
            except:
                pass
            CNameMedicamentEdit.seriesList = result
        return CNameMedicamentEdit.seriesList


    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.__completerModel = CStaticCompleterModel(self, self.getSeriesList())
        self.__completer = CCompleter(self, self.__completerModel)
        self.setCompleter(self.__completer)
#        self.connect(self.__completer, QtCore.SIGNAL('highlighted(QString)'), self.onCompleterHighlighted)


#    def focusOutEvent(self, event):
#        currentCompletion = self.__completer.currentCompletion()
#        if QString.compare(self.text(), currentCompletion, Qt.CaseInsensitive) == 0:
#                self.setText(currentCompletion)
##                self.setInsurerFilter(currentCompletion)
#        QtGui.QLineEdit.focusOutEvent(self, event)
#
#
#    def onCompleterHighlighted(self, text):
#        self.emit(QtCore.SIGNAL('textEdited(QString)'), text)

class CMedicamentInDocTableCol(CInDocTableCol):
    def createEditor(self, parent):
        editor = CNameMedicamentEdit(parent)
        return editor
