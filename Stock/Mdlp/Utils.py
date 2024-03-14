# -*- coding: utf-8 -*-
# iiro: Incoming Invoice - Reverse Order
# Заголовок будет потом,
# сейчас это "превью"

import datetime
import isodate
import json

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDateTime

from Exchange.MDLP.documents.v136 import createFromXml


#from library.DialogBase import CDialogBase
from library.Utils import forceInt, forceRef, forceString

#from connection import CMdlpConnection
from ExchangePurpose import CMdplExchangePurpose
from Stage import CMdlpStage


__all__ = [ 'getMotionStage',
            'getMotionStageFromExchanges',
            'setMotionStage',
            'getMotionExchanges',
            'processMotion',
            'storeMdlpExchange',
            'updateMdlpExchange',
            'execMdlpExchange',
            'explainWait',
          ]


def getMotionStage(motionId):
    db = QtGui.qApp.db
    return forceInt(db.translate('StockMotion', 'id', motionId, 'mdlpStage'))


def getMotionStageFromExchanges(motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    stage = db.getMin(table,
                      'stage',
                      [ table['master_id'].eq(motionId),
                        table['purpose'].like('%.out.%'),
                        table['stage'].ge(CMdlpStage.ready),
                      ]
                     )
    if stage is None:
        return CMdlpStage.unnecessary
    else:
        return forceInt(stage)


def setMotionStage(motionId, mdlpStage):
    db = QtGui.qApp.db
    table = db.table('StockMotion')
    record = table.newRecord(['id', 'mdlpStage'])
    record.setValue('id', motionId)
    record.setValue('mdlpStage', mdlpStage)
    db.updateRecord(table, record)


def getMotionExchanges(motionId, purposes=None):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    if purposes:
        for purpose in purposes:
            ids = db.getIdList(table,
                               'id',
                               db.joinAnd([ table['master_id'].eq(motionId),
                                            table['purpose'].eq(purpose),
                                            table['stage'].inlist((CMdlpStage.ready, CMdlpStage.inProgress))
                                          ]
                                         ),
                               limit=1
                              )
            result.append(ids[0] if ids else None)
    else:
        result = db.getIdList(table,
                               'id',
                               db.joinAnd([ table['master_id'].eq(motionId),
                                            db.joinOr([ table['purpose'].like('%.out.%'),
                                                        table['purpose'].like('%.wait.%'),
                                                      ]
                                                     ),

                                            table['stage'].inlist((CMdlpStage.ready, CMdlpStage.inProgress))
                                          ]
                                         ),
                              )

    return result


def processMotion(logger,
                  motionId,
                  connection
                 ):
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.inProgress:
        exchangeIds = getMotionExchanges(motionId)
        exchangeStages = []
        for exchangeId in exchangeIds:
            exchangeStage = execMdlpExchange(logger, exchangeId, connection)
            exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage




def storeMdlpExchange(motionId,
                      runAfterId  = None,
                      purpose     = '',
                      stage       = 0,
                      docType     = 0,
                      requestId   = '',
                      filter      = '',
                      progress    = '',
                      documentId  = '',
                      xmlDocument = ''
                     ):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    record = table.newRecord()
    record.setValue('createDatetime', QDateTime.currentDateTime())
    record.setValue('master_id',   motionId)
    record.setValue('runAfter_id', runAfterId)
    record.setValue('purpose',     purpose)
    record.setValue('stage',       stage)
    record.setValue('docType',     docType)
    record.setValue('requestId',   requestId)
    record.setValue('filter',      filter)
    record.setValue('progress',    progress)
    record.setValue('documentId',  documentId)
    record.setValue('xmlDocument', xmlDocument)
    return db.insertRecord(table, record)

# нужно? ненужно?
def updateMdlpExchange(exchangeId,
                       **kwargs
                      ):
    kwargs['id'] = exchangeId
    kwargs['modifyDatetime'] = QDateTime.currentDateTime()

    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    record = table.newRecord(kwargs.keys())
    for k, v in kwargs.iteritems():
        record.setValue(k, v)
#    record.setValue('id', exchangeId)
    db.updateRecord(table, record)
    return exchangeId


def execMdlpExchange(logger, exchangeId, connection):
    # выполняем шаг обмена для выгрузки или загрузки документа
    # Предыдущего обмена не должно быть или он должен быть
    # в стадиях "обмен не нужен" или "обмен завершён успешно"
    # тогда можно предпринять попытку выполнить этот шаг обмена,
    # иначе
    db = QtGui.qApp.db
    tableExchange = db.table('StockMotion_MdlpExchange')
    tablePrevExchange = db.table('StockMotion_MdlpExchange').alias('prev')
    table = tableExchange.leftJoin(tablePrevExchange,
                                   tablePrevExchange['id'].eq(tableExchange['runAfter_id'])
                                  )
    record = db.getRecordEx(table,
                            [ tablePrevExchange['stage'].alias('prevStage'),
                              tableExchange['stage'].alias('stage'),
                              tableExchange['purpose'],
                            ],
                            tableExchange['id'].eq(exchangeId)
                           )
    stage = forceInt(record.value('stage'))
    prevStage = forceRef(record.value('prevStage')) # forceRef - for None on NULL
    if prevStage not in (None, CMdlpStage.unnecessary, CMdlpStage.success):
        return stage

    purpose = forceString(record.value('purpose'))
    if '.out.' in purpose:
        logger.append(CMdplExchangePurpose.text(purpose))
        return _execOutMdlpExchange(logger, exchangeId, stage, connection)
    elif '.wait.' in purpose:
        logger.append(CMdplExchangePurpose.text(purpose))
        return _execWaitMdlpExchange(logger, exchangeId, stage, connection)
    else:
        assert False, 'unknown exchange purpose'
        return stage


def _execOutMdlpExchange(logger, exchangeId, stage, connection):
    # выполняем шаг обмена для выгрузки документа.
    # если единица обмена помечена как подготовленная ( stage == 1 == CMdlpStage.ready )
    # - то нужно поискать свои докумены по requestId
    #   - если найдётся, то это признак что произошло прерывание
    #        и нужно сохранить documentId и перевести в stage == 2 == CMdlpStage.inProgress )
    #   - если не найдётся, то нужно выгружить,
    #        иногда перед выгрузкой нужно поправить дату операции :(
    #        сохранить documentId и перевести в stage == 2 == CMdlpStage.inProgress )
    #        если выгрузка не произойдёт, то остаётся в тек. stage
    # если единица обмена помечена как в "процессе" ( stage == 2 == CMdlpStage.inProgress )
    # - то нужно поискать документ (по
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    docStatus  = None
    documentId = None
    if stage == CMdlpStage.ready:
        requestId = forceString(db.translate(table, 'id', exchangeId, 'requestId'))
        docType   = forceInt(db.translate(table, 'id', exchangeId, 'docType'))
        logger.append(u'запрос в МДЛП документа типа %d по request_id %s' % (docType, requestId))
        mdlpMetaDocs = connection.getOutcomingDocuments(count=1,
                                                        requestId=requestId,
                                                        docType=docType,
                                                        docStatus=None
                                                       )
        if mdlpMetaDocs:
            mdlpMetaDoc = mdlpMetaDocs[0]
            documentId = mdlpMetaDoc.documentId
            docStatus  = mdlpMetaDoc.docStatus
            stage      = CMdlpStage.inProgress
            updateMdlpExchange(exchangeId,
                               stage      = stage,
                               documentId = documentId,
                               docStatus  = docStatus
                              )
        else:
            optionalFields = {}
            xml = forceString(db.translate(table, 'id', exchangeId, 'xmlDocument'))
            if docType == 912:
                xml = _fixOperationDate(xml)
                optionalFields['xmlDocument'] = xml
            stage      = CMdlpStage.inProgress
            logger.append(u'документ не найден. отправка в МДЛП докумета типа %d с request_id %s' % (docType, requestId))
            documentId = connection.postRawDocument(xml, requestId=requestId)
            updateMdlpExchange(exchangeId,
                               stage      = stage,
                               documentId = documentId,
                               **optionalFields
                              )
    if stage == CMdlpStage.inProgress:
        if documentId is None:
            documentId = forceString(db.translate(table, 'id', exchangeId, 'documentId'))
        if docStatus is None:
            logger.append(u'запрос в МДЛП документа с id %s' % documentId)
            mdlpMetaDocs = connection.getOutcomingDocuments(count=1,
                                                            documentId=documentId,
                                                            docStatus=None
                                                           )
            if mdlpMetaDocs:
                mdlpMetaDoc = mdlpMetaDocs[0]
                docStatus = mdlpMetaDoc.docStatus
        if docStatus in ('PROCESSED_DOCUMENT', 'FAILED_RESULT_READY'):
            stage = CMdlpStage.success if docStatus == 'PROCESSED_DOCUMENT' else CMdlpStage.failed
            xml = connection.getDocumentRawReceipt(documentId)
            updateMdlpExchange(exchangeId,
                               stage      = stage,
                               documentId = documentId,
                               docStatus  = docStatus,
                               xmlReceipt = xml
                              )
        else:
            updateMdlpExchange(exchangeId,
                               docStatus  = docStatus,
                              )
    return stage


def _execWaitMdlpExchange(logger, exchangeId, stage, connection):
    # выполняем шаг обмена по ожиданию входящего документа.
    # у нас в exchange есть filter, который представляет собою json словаря
    # с параметрами для запроса входящих документов
    # (docType, senderId, begDate, endDate)
    # и progress - словарь с целевыми и достигнутыми sscc и sgtin)
    if stage in (CMdlpStage.ready, CMdlpStage.inProgress):
        db = QtGui.qApp.db
        table = db.table('StockMotion_MdlpExchange')
        record = db.getRecord(table,
                              ['master_id', 'purpose', 'filter', 'progress'],
                              exchangeId
                             )
        motionId = forceRef(record.value('master_id'))
        purpose  = forceString(record.value('purpose'))
        filterAsString   = forceString(record.value('filter'))
        progressAsString = forceString(record.value('progress'))
        try:
            filter = json.loads(filterAsString)
            assert isinstance(filter, dict)
            progress = json.loads(progressAsString)
            assert isinstance(progress, dict)
            required = progress.get('required', {})
            requiredSsccs  = set(required.get('ssccs', []))
            requiredSgtins = set(required.get('sgtins', []))
            received = progress.get('received', {})
            receivedSsccs  = set(received.get('ssccs', []))
            receivedSgtins = set(received.get('sgtins', []))
        except:
            updateMdlpExchange(exchangeId, stage = CMdlpStage.failed)
            logger.append(u'прерывание обработки из-за ошибки в данных')
            return CMdlpStage.failed
        if (     requiredSsccs.issubset(receivedSsccs)
             and requiredSgtins.issubset(receivedSgtins)
           ):
            updateMdlpExchange(exchangeId, stage = CMdlpStage.success)
            return CMdlpStage.success
        incomingPurpose = purpose.replace('.wait.', '.in.')
        seenDocuments   = getMdlpDocumentIdsSet(motionId, incomingPurpose)
        docType  = filter.get('docType')
        senderId = filter.get('senderId')
        begDate  = filter.get('begDate')
        if begDate:
            begDate = QDateTime.fromString(begDate, Qt.ISODate)
        endDate  = filter.get('endDate')
        if endDate:
            endDate = QDateTime.fromString(endDate, Qt.ISODate)

        logger.append(u'поиск в МДЛП документов типа %d от %s' % (docType, senderId))
        docs = connection.getIncomingDocuments(count     = 1000,
                                               docType   = docType,
                                               docStatus = 'PROCESSED_DOCUMENT',
                                               senderId  = senderId,
                                               begDate   = begDate,
                                               endDate   = endDate,
                                              )
        for metaDoc in docs:
            documentId = metaDoc.documentId
            if documentId not in seenDocuments:
                logger.append(u'загрузка из МДЛП документа с id %s' % documentId)
                rawOuterDoc = connection.getRawDocument(documentId)
                outerDoc = createFromXml(rawOuterDoc)
                if docType == 607:
                    ssccs  = set([unicode(s)
                                    for s in outerDoc.accept_notification.order_details.sscc
                                    ]
                                )
                    sgtins = set([unicode(s)
                                    for s in outerDoc.accept_notification.order_details.sgtin
                                    ]
                                )
                else:
                    ssccs = sgtins = set()

                receivedSsccs  |= ssccs
                receivedSgtins |= sgtins
                received = { 'ssccs' : sorted(receivedSsccs),
                             'sgtins': sorted(receivedSgtins),
                           }
                progress['received'] = received
                progressAsString = json.dumps(progress)
                allDone = (     requiredSsccs.issubset(receivedSsccs)
                            and requiredSgtins.issubset(receivedSgtins)
                            )

                db.transaction()
                try:
                    storeMdlpExchange(motionId,
                                        purpose=incomingPurpose,
                                        stage=CMdlpStage.unnecessary,
                                        docType=docType,
                                        documentId=documentId,
                                        xmlDocument=rawOuterDoc
                                        )
                    stage=CMdlpStage.success if allDone else CMdlpStage.inProgress
                    updateMdlpExchange(exchangeId,
                                        process=progressAsString,
                                        stage=stage
                                        )
                    db.commit()
                except Exception as e:
                    db.rollback()
                    raise e
                if allDone:
                    return stage
    return stage


def getMdlpDocumentIdsSet(motionId, purpose):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    records = db.getRecordList(table,
                               'documentId',
                               [ table['master_id'].eq(motionId),
                                 table['purpose'].eq(purpose),
                               ]
                              )
    return set([ forceString(record.value('documentId'))
                 for record in records
               ]
              )


def explainWait(progressAsString):
    progress = json.loads(progressAsString)
    try:
        required = progress.get('required', {})
        requiredSsccs  = required.get('ssccs', [])
        requiredSgtins = required.get('sgtins', [])
        return ', '.join(requiredSsccs+requiredSgtins)
    except:
        return u'ошибка в «progress»'


def _fixOperationDate(xml):
    outerDoc = createFromXml(xml)
    if outerDoc.unit_unpack:
        outerDoc.unit_unpack.operation_date=datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL)
        xml = outerDoc.toxml('UTF-8').decode('utf-8')
    return xml

