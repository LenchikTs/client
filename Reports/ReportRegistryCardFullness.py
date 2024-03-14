# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.Utils       import forceInt, forceBool, forceString, formatName
from library.DialogBase  import CDialogBase
from Reports.Report      import CReport
from Reports.ReportBase  import CReportBase, createTable

from Reports.ReportAcuteInfections import addAttachCond


def getAddressCond(isLocAddress):
    db = QtGui.qApp.db
    tableClientAddress = db.table('ClientAddress')
    subcond = [tableClientAddress['client_id'].eqEx('`Client`.`id`'),
               tableClientAddress['id'].eqEx(u'getClientLocAddressId(Client.id)' if isLocAddress else u'getClientRegAddressId(Client.id)'),
               tableClientAddress['address_id'].isNull(),
              ]
    subcondNoCAId = u'(SELECT %s IS NULL)'%(u'getClientLocAddressId(Client.id)' if isLocAddress else u'getClientRegAddressId(Client.id)')
    return db.joinOr([db.existsStmt(tableClientAddress, subcond), subcondNoCAId])


def selectData(params):
    if not any(params.values()):  # ничего не выбрано
        return None

    db = QtGui.qApp.db
    tableClient = db.table('Client')
    cond = []
    cols = [ tableClient['id'].alias('clientId'),
             tableClient['firstName'],
             tableClient['lastName'],
             tableClient['patrName'],
           ]

    if params.get('noFIO'):
        subcond = db.joinOr([
            tableClient['firstName'].eq(''),
            tableClient['lastName'].eq(''),
            tableClient['patrName'].eq(''),
        ])
        cond.append(subcond)
    if params.get('noBirthDate'):
        subcond = db.joinOr(["(DATE(Client.birthDate) = DATE('0000-00-00'))",
                             tableClient['birthDate'].isNull()])
        cols.append('(%s) AS noBirthDate' % subcond)
        cond.append(subcond)
    if params.get('noRegAddress'):
        subcond = getAddressCond(isLocAddress=False)
        cols.append('(%s) AS noRegAddress' % subcond)
        cond.append(subcond)
    if params.get('noLocAddress'):
        subcond = getAddressCond(isLocAddress=True)
        cols.append('(%s) AS noLocAddress' % subcond)
        cond.append(subcond)
    if params.get('noSNILS'):
        subcond = tableClient['SNILS'].eq('')
        cols.append('(%s) AS noSNILS' % subcond)
        cond.append(subcond)
    if params.get('noDocuments'):
        stmt = u"""NOT EXISTS(SELECT 1
                FROM ClientDocument
                JOIN rbDocumentType ON ClientDocument.documentType_id = rbDocumentType.id
                JOIN rbDocumentTypeGroup ON rbDocumentType.group_id = rbDocumentTypeGroup.id
                WHERE ClientDocument.deleted = 0 AND ClientDocument.client_id = Client.id
                    AND rbDocumentTypeGroup.code = '1')"""
        cols.append('(%s) AS noDocuments'  % stmt)
        cond.append(stmt)
    if params.get('noAttachTFOMS'):
        record = db.getRecordEx('rbAttachType', 'id', u"name LIKE '%тфомс%'")
        if not record:
            return None
        attachType = forceInt(record.value('id'))
        stmt = []
        addAttachCond(stmt, None, 0, attachType, QDate(), QDate())
        cols.append('(%s) AS noAttachTFOMS' % stmt[0])
        cond.append(stmt[0])
    if params.get('noAttachLPU'):
        stmt = []
        addAttachCond(stmt, 'LPU_id!=%d'%QtGui.qApp.currentOrgId(), 0, None, QDate(), QDate())
        cols.append('(%s) AS noAttachLPU' % stmt[0])
        cond.append(stmt[0])

    cond = [ tableClient['deleted'].eq(0), db.joinOr(cond) ]
    stmt = db.selectStmt(tableClient, cols, cond)
    return db.query(stmt)



class CReportRegistryCardFullness(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о заполненности регистрационных карт')


    def getSetupDialog(self, parent):
        result = CReportRegistryCardFullnessSetup(parent)
        result.setWindowTitle(self.title())
        return result


    def build(self, params):
        checkFIO = params.get('noFIO')

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('33%', [u'Код карты'], CReportBase.AlignCenter),
            ('33%', [u'ФИО пациента'], CReportBase.AlignCenter),
            ('34%', [u'Отсутствующие данные'], CReportBase.AlignLeft),
        ]
        table = createTable(cursor, tableColumns)
        query = selectData(params)
        if not query:
            return doc
        while query.next():
            record = query.record()
            clientId = forceInt(record.value('clientId'))
            firstName = forceString(record.value('firstName'))
            lastName = forceString(record.value('lastName'))
            patrName = forceString(record.value('patrName'))
            noBirthDate = forceBool(record.value('noBirthDate'))
            noRegAddress = forceBool(record.value('noRegAddress'))
            noLocAddress = forceBool(record.value('noLocAddress'))
            noSNILS = forceBool(record.value('noSNILS'))
            noDocuments = forceBool(record.value('noDocuments'))
            noAttachTFOMS = forceBool(record.value('noAttachTFOMS'))
            noAttachLPU = forceBool(record.value('noAttachLPU'))

            notFilled = []
            if checkFIO and not firstName or firstName.isspace():
                notFilled.append(u'имя')
            if checkFIO and not lastName or lastName.isspace():
                notFilled.append(u'фамилия')
            if checkFIO and not patrName or patrName.isspace():
                notFilled.append(u'отчество')
            if noBirthDate:
                notFilled.append(u'дата рождения')
            if noRegAddress:
                notFilled.append(u'адрес регистрации')
            if noLocAddress:
                notFilled.append(u'адрес проживания')
            if noSNILS:
                notFilled.append(u'СНИЛС')
            if noDocuments:
                notFilled.append(u'документ, удостоверяющий личность')
            if noAttachTFOMS:
                notFilled.append(u'прикрепление к ТФОМС')
            if noAttachLPU:
                notFilled.append(u'прикрепление к ЛПУ')

            row = table.addRow()
            table.setText(row, 0, clientId)
            table.setText(row, 1, formatName(lastName, firstName, patrName))
            table.setText(row, 2, u', '.join(notFilled).capitalize())

        return doc



class CReportRegistryCardFullnessSetup(CDialogBase):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.chkFIO = QtGui.QCheckBox(u'Неполное ФИО')
        self.chkBirthDate = QtGui.QCheckBox(u'Не заполнена дата рождения')
        self.chkRegAddress = QtGui.QCheckBox(u'Не заполнен адрес регистрации')
        self.chkLocAddress = QtGui.QCheckBox(u'Не заполнен адрес проживания')
        self.chkSNILS = QtGui.QCheckBox(u'Не заполнен СНИЛС')
        self.chkDocuments = QtGui.QCheckBox(u'Не заполнены данные документа, удостоверяющего личность')
        self.chkAttachTFOMS = QtGui.QCheckBox(u'Отсутствие прикрепления к ТФОМС')
        self.chkAttachLPU = QtGui.QCheckBox(u'Отсутствие прикрепления к ЛПУ')
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.chkFIO)
        layout.addWidget(self.chkBirthDate)
        layout.addWidget(self.chkRegAddress)
        layout.addWidget(self.chkLocAddress)
        layout.addWidget(self.chkSNILS)
        layout.addWidget(self.chkDocuments)
        layout.addWidget(self.chkAttachTFOMS)
        layout.addWidget(self.chkAttachLPU)
        layout.addStretch()
        layout.addWidget(buttonBox)


    def params(self):
        result = {}
        result['noFIO'] = self.chkFIO.isChecked()
        result['noBirthDate'] = self.chkBirthDate.isChecked()
        result['noRegAddress'] = self.chkRegAddress.isChecked()
        result['noLocAddress'] = self.chkLocAddress.isChecked()
        result['noSNILS'] = self.chkSNILS.isChecked()
        result['noDocuments'] = self.chkDocuments.isChecked()
        result['noAttachTFOMS'] = self.chkAttachTFOMS.isChecked()
        result['noAttachLPU'] = self.chkAttachLPU.isChecked()
        return result


    def setParams(self, params):
        self.chkFIO.setChecked(params.get('noFIO', False))
        self.chkBirthDate.setChecked(params.get('noBirthDate', False))
        self.chkRegAddress.setChecked(params.get('noRegAddress', False))
        self.chkLocAddress.setChecked(params.get('noLocAddress', False))
        self.chkSNILS.setChecked(params.get('noSNILS', False))
        self.chkDocuments.setChecked(params.get('noDocuments', False))
        self.chkAttachTFOMS.setChecked(params.get('noAttachTFOMS', False))
        self.chkAttachLPU.setChecked(params.get('noAttachLPU', False))
