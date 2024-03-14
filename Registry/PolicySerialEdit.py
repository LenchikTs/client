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
from PyQt4.QtCore import SIGNAL

from library.Completer import CStaticCompleterModel, CCompleter


class CPolicySerialEdit(QtGui.QLineEdit):
    seriesList = None

    def getSeriesList(self):
        if CPolicySerialEdit.seriesList is None:
            db = QtGui.qApp.db
            result = []
            try:
                query = db.query('SELECT DISTINCT serial FROM Organisation_PolicySerial WHERE serial != \'\' ORDER BY serial')
                while query.next():
                    result.append(query.value(0))
            except:
                pass
            CPolicySerialEdit.seriesList = result
        return CPolicySerialEdit.seriesList


    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.__completerModel = CStaticCompleterModel(self, self.getSeriesList())
        self.__completer = CCompleter(self, self.__completerModel)
        self.setCompleter(self.__completer)
        self.connect(self.__completer, SIGNAL('highlighted(QString)'), self.onCompleterHighlighted)


    def focusOutEvent(self, event):
        currentCompletion = self.__completer.currentCompletion()
        if unicode(self.text()).lower() == unicode(currentCompletion).lower():
            self.setText(currentCompletion)
#            self.setInsurerFilter(currentCompletion)
        QtGui.QLineEdit.focusOutEvent(self, event)

#    def setInsurerFilter(self, text):
#        pass

    def onCompleterHighlighted(self, text):
        self.emit(SIGNAL('textEdited(QString)'), text)
