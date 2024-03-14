# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Ещё один вариант соединения прогресс-бара и журнала,
## с надеждой на лучшую реализацию.
##
#############################################################################

#from PyQt4 import QtGui
from PyQt4.QtCore import QDateTime

from library.SimpleProgressDialog import CSimpleProgressDialog
from Ui_ProgressWithLog import Ui_ProgressWithLogDialog


class CProgressWithLogDialog(Ui_ProgressWithLogDialog, CSimpleProgressDialog):
    titleLen = 16

    def __init__(self, parent):
        CSimpleProgressDialog.__init__(self, parent)
        fm = self.txtLogView.fontMetrics()
        self.txtLogView.setTabStopWidth( fm.boundingRect('0'*(self.titleLen+1)).width() )


    def log(self, title, message):
        now = QDateTime.currentDateTime()
        self.txtLogView.appendPlainText(u'%s\t%s\t%s' % ( unicode(now.toString('dd.MM.yyyy hh:mm')),
                                                          title,
                                                          '\n\t\t'.join( message.split('\n') )
                                                        )
                                       )
#        QtGui.qApp.log(title, message)
