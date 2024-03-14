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

from PyQt4          import QtGui
from PyQt4.QtCore   import Qt, pyqtSignature

from Registry.Utils import formatClientContingentType
from library.Utils  import forceRef, forceString, forceBool

from Registry.Ui_ShowContingentsClientDialog import Ui_ShowContingentsClientDialog


class CShowContingentsClientDialog(QtGui.QDialog, Ui_ShowContingentsClientDialog):
    def __init__(self,  parent, clientId):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.clientId = clientId
        self.loadData()


    def loadData(self):
        bannerHTML=u''
        if self.clientId:
            db = QtGui.qApp.db
            table = db.table('rbContingentType')
            records = db.getRecordList(table, u'*', order='rbContingentType.priority DESC, rbContingentType.id ASC')
            for record in records:
                contingentTypeId = forceRef(record.value('id'))
#                contingentTypeCode = forceString(record.value('code'))
                contingentTypeName = forceString(record.value('name'))
#                priority = forceInt(record.value('priority'))
                isContingent = False
                stmt = u'SELECT checkClientContingentTypeFind(%s, %s) AS isContingent'%(self.clientId, contingentTypeId)
                query = QtGui.qApp.db.query(stmt)
                while query.next():
                    record   = query.record()
                    isContingent = forceBool(record.value('isContingent'))
                if contingentTypeId and isContingent:
                    clientContingentTypeCode, clientContingentTypeColor = formatClientContingentType(self.clientId, contingentTypeId)
                    bannerHTML+= u' <B><font color="%s">[%s]</font></B><br>' % (clientContingentTypeColor, clientContingentTypeCode + u' - ' + contingentTypeName)
        clientBanner = u'<HTML><BODY>%s</BODY></HTML>' % bannerHTML
        self.txtClientContingentBrowser.setHtml(clientBanner)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Close:
            self.close()
