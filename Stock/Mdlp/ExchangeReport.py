# -*- coding: utf-8 -*-
# iiro: Incoming Invoice - Reverse Order
# Заголовок будет потом,
# сейчас это "превью"

#import datetime
#import isodate
#import json

from PyQt4 import QtGui
#from PyQt4.QtCore import Qt, QDateTime

from library.Utils import forceDateTime, forceInt, forceString, forceRef

from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog, CPageFormat

from .ExchangePurpose import CMdplExchangePurpose
from .Stage import CMdlpStage
from .Utils import explainWait


def showMdlpExchangeReport(widget, motionId):
#    db = QtGui.qApp.db
#    motionRecord = db.getRecord('StockMotion', ['type', 'mdlpStage'])

    records = selectData(motionId)
    mapIdToNum = {}
    for i, record in enumerate(records):
        id = forceRef(record.value('id'))
        mapIdToNum[id] = str(i+1)

    doc = QtGui.QTextDocument()
    cursor = QtGui.QTextCursor(doc)
    cursor.setCharFormat(CReportBase.ReportTitle)
    cursor.insertText(u'Обмен с ДМЛП')
    cursor.insertBlock()
    cursor.setCharFormat(CReportBase.ReportBody)

    tableColumns = [ ( '3%', u'№',               CReportBase.AlignRight),
                     ( '6%', u'Создано',         CReportBase.AlignCenter),
                     ( '6%', u'Изменено',        CReportBase.AlignCenter),
                     ( '3%', u'Выполнять после', CReportBase.AlignRight),
                     ('16%', u'Назначение',      CReportBase.AlignLeft),
                     ('16%', u'Стадия',          CReportBase.AlignLeft),
                     ('16%', u'requestId',       CReportBase.AlignLeft),
                     ('16%', u'documentId',      CReportBase.AlignLeft),
                     ('16%', u'Состояние в МДЛП',CReportBase.AlignLeft),
                   ]

    table = createTable(cursor, tableColumns)
    for record in records:
        id = forceRef(record.value('id'))
        createDatetime = forceDateTime(record.value('createDatetime'))
        modifyDatetime = forceDateTime(record.value('modifyDatetime'))
        runAfterId = forceRef(record.value('runAfter_id'))
        purpose = forceString(record.value('purpose'))
        progress = forceString(record.value('progress'))
        stage = forceInt(record.value('stage'))
        requestId = forceString(record.value('requestId'))
        documentId = forceString(record.value('documentId'))
        docStatus  = forceString(record.value('docStatus'))

        iTableRow = table.addRow()
        table.setText(iTableRow, 0, mapIdToNum.get(id, u'-'))
        table.setText(iTableRow, 1, forceString(createDatetime))
        table.setText(iTableRow, 2, forceString(modifyDatetime))
        table.setText(iTableRow, 3, mapIdToNum.get(runAfterId, u'-'))
        table.setText(iTableRow, 4, formatPurposeAndProgres(purpose, progress))
        table.setText(iTableRow, 5, CMdlpStage.text(stage))
        table.setText(iTableRow, 6, requestId or '-')
        table.setText(iTableRow, 7, documentId or '-')
        table.setText(iTableRow, 8, docStatus or '-')
        docStatus
    view = CReportViewDialog(widget)
    view.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape)
    view.setText(doc)
    view.exec_()


def selectData(motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    records = db.getRecordList(table,
                               ['id',
                                'createDatetime',  'modifyDatetime',
                                'runAfter_id',
                                'purpose',
                                'progress',
                                'stage',
                                'requestId', 'documentId',
                                'docStatus',
#                                'xmlDocument', 'xmlReceipt'
                               ],
                               [ table['master_id'].eq(motionId),
                               ],
                               'id'
                              )
    return records


def formatPurposeAndProgres(purpose, progress):
    result = CMdplExchangePurpose.text(purpose)
    if CMdplExchangePurpose.isWait(purpose) and progress:
        result += '(%s)' % explainWait(progress)
    return result
