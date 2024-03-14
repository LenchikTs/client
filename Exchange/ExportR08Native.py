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

u"""Экспорт реестра  в формате XML. Республика Калмыкия"""

from PyQt4.QtCore import Qt

from library.Utils import forceString
#from Exchange.Export import CAbstractExportWizard
from Exchange.ExportR47D1 import (CExportWizard, XmlStreamWriter,
    PersonalDataWriter)

def exportR08Native(widget, accountId, accountItemIdList, _):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CR08ExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CR08ExportWizard(CExportWizard):
    u"""Мастер экспорта для Калмыкии"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг для Калмыкии'
        CExportWizard.__init__(self, parent)
        self.prefix = 'R08D1'
        self.setWindowTitle(title)
        self.page1.setXmlWriter((R08XmlStreamWriter(self.page1),
            PersonalDataWriter(self.page1)))


# ******************************************************************************

class R08XmlStreamWriter(XmlStreamWriter):
    u"""Осуществляет запись данных экспорта в XML"""

    def __init__(self, parent):
        XmlStreamWriter.__init__(self, parent)

    def writeHeader(self, params):
        u"""Запись заголовка xml файла"""
        settleDate = params['settleDate']
        date = params['accDate']
        self.writeStartElement('ZL_LIST')

        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1')
        self.writeTextElement('DATA', date.toString(Qt.ISODate))
        self.writeTextElement('FILENAME', params['shortFileName'][:-4])
        self.writeTextElement('SD_Z', self._parent.getEventCount())
        self.writeEndElement() # ZGLV

        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', '%d' % params['accId'])
        self.writeTextElement('CODE_MO', params['lpuCode'])
        self.writeTextElement('YEAR', forceString(settleDate.year()))
        self.writeTextElement('MONTH', forceString(settleDate.month()))
        self.writeTextElement('NSCHET', params['accNumber'])
        self.writeTextElement('DSCHET',
                params['accDate'].toString(Qt.ISODate))
        self.writeTextElement('PLAT', params['payerCode'])
        self.writeTextElement('SUMMAV', forceString(params['accSum']))
        self.writeEndElement() # SCHET
