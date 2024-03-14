# -*- coding: utf-8 -*-
# iido: Incoming Invoice - Direct Order
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# На предыдущем шаге мы получили документ типа 601-move_order_notification
# и теперь должны передать:
#   701-accept,
#   606-refusal_receiver_notification,
#   912-unit_unpack

import datetime
import uuid

import isodate
import pyxb

from PyQt4 import QtGui

from Exchange.MDLP.documents.v136 import createFromXml, Documents, Accept, RefusalReceiver, UnitUnpack


#from library.DialogBase import CDialogBase
from library.Utils import withWaitCursor

#from connection import CMdlpConnection
from Stage import CMdlpStage
from ExchangePurpose import CMdplExchangePurpose
from Utils import ( getMotionStage,
                    getMotionStageFromExchanges,
                    setMotionStage,
                    storeMdlpExchange,
                    execMdlpExchange,
                  )


# последействия для прямого порядка приёма
# нам нужно:
# - если есть принятые sscc или sgtin, то сформиривать и передать 701-accept
# - если есть непринятые sscc или sgtin, то сформиривать и передать 606-refusal_receiver_notification
# - если есть sscc, то передать 912-unit_unpack
# каждый перечисленный выше документ проходит стадии обработки:
# - принимается решение необходимости формирования документа или отказ от необходимости передавать
# - документ формируется (как xml), генерируется request_id, всё сохраняется в БД
# - точка повтора №1 (критерий: есть request_id, нет document_id)
# - документ передаётся в MDLP и document_id дополняет данные в БД
# - точка повтора №2 (критерий: есть request_id, есть document_id, нет состояния)
# - анализируется состояние документа,
#   doc_status дополняет данные в БД.
#   если doc_status in ('PROCESSED_DOCUMENT', 'FAILED_RESULT_READY')
#   система МДЛП закончила работу над документом
#   вероятно, можно сохранить в БД квитанцию этого документа.
#   что делать, если doc_status == 'FAILED_RESULT_READY' я пока не знаю.
#   информировать?


@withWaitCursor
def iidoProcess(logger, #!logger
                motionId,
                connection,
                incomingDocumentId,
                confirmedSsccs,
                confirmedSgtins,
                refusedSsccs,
                refusedSgtins
               ):
    # всякие хлопоты после приёма накладной по прямому порядку
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.ready:
        acceptId, refusalReceiverId, unitUnpackId = prepareIidoProcess(logger,
                                                                       motionId,
                                                                       connection,
                                                                       incomingDocumentId,
                                                                       confirmedSsccs,
                                                                       confirmedSgtins,
                                                                       refusedSsccs,
                                                                       refusedSgtins
                                                                      )
        motionStage = CMdlpStage.inProgress
    elif motionStage == CMdlpStage.inProgress:
        acceptId, refusalReceiverId, unitUnpackId = getIidoExchanges(logger, motionId)

    if motionStage == CMdlpStage.inProgress:
        exchangeStages = []
        for exchangeId in [acceptId, refusalReceiverId, unitUnpackId]:
            if exchangeId:
                exchangeStage = execMdlpExchange(logger, exchangeId, connection)
                exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage


def prepareIidoProcess(logger,
                       motionId,
                       connection,
                       incomingDocumentId,
                       confirmedSsccs,
                       confirmedSgtins,
                       refusedSsccs,
                       refusedSgtins
                      ):
    sessionUuid = str(uuid.uuid4())

    # показать: запрашиваю документ
    logger.append(u'запрос документа %s' % incomingDocumentId)
    rawOuterDoc = connection.getRawDocument(incomingDocumentId)
    QtGui.qApp.db.transaction()
    try:
        storeMdlpExchange(motionId,
                          purpose=CMdplExchangePurpose.iidoMoveOrderNotification,
                          stage=CMdlpStage.unnecessary,
                          docType=601,
                          documentId=incomingDocumentId,
                          xmlDocument=rawOuterDoc
                         )

        outerDoc = createFromXml(rawOuterDoc)
        originalSessionUuid = outerDoc.session_ui
        incomingDoc = outerDoc.move_order_notification
        supplierId = incomingDoc.subject_id
        receiverId = incomingDoc.receiver_id

        # показать: формирую документы

        acceptId          = None
        refusalReceiverId = None
        unitUnpackId      = None

        if confirmedSsccs or confirmedSgtins:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iidoAccept))
            acceptId = buildAndStoreIidoAccept( motionId,
                                                sessionUuid,
                                                originalSessionUuid,
                                                supplierId,
                                                receiverId,
                                                confirmedSsccs,
                                                confirmedSgtins,
                                              )

        if refusedSsccs or refusedSgtins:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iidoRefusalReceiver))
            refusalReceiverId = buildAndStoreIidoRefusalReceiver(motionId,
                                                                 sessionUuid,
                                                                 originalSessionUuid,
                                                                 supplierId,
                                                                 receiverId,
                                                                 refusedSsccs,
                                                                 refusedSgtins
                                                                )

        if confirmedSsccs:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iidoUnitUnpack))
            unitUnpackId = buildAndStoreIidoUnitUnpack(motionId,
                                                       sessionUuid,
                                                       receiverId,
                                                       confirmedSsccs
                                                      )
        setMotionStage(motionId, CMdlpStage.inProgress)
        QtGui.qApp.db.commit()
        return (acceptId, refusalReceiverId, unitUnpackId)
    except Exception as e:
        QtGui.qApp.db.rollback()
        raise e


def buildAndStoreIidoAccept(motionId,
                            sessionUuid,
                            originalSessionUuid,
                            supplierId,
                            receiverId,
                            confirmedSsccs,
                            confirmedSgtins
                           ):
    accept = Accept(subject_id      = receiverId,
                    counterparty_id = supplierId,
                    operation_date  = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL),
                    order_details   = pyxb.BIND() # магия, иначе нужно использовать синтетическое имя, и при изменении в схеме это имя изменится
                   )
    if confirmedSsccs:
        accept.order_details.sscc  = confirmedSsccs
    if confirmedSgtins:
        accept.order_details.sgtin = confirmedSgtins

    outDoc = Documents(original_id = originalSessionUuid, # session_ui из входящего документа
                       session_ui  = sessionUuid,
                       accept      = accept
                      )
    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iidoAccept,
                             stage       = CMdlpStage.ready,
                             docType     = int(accept.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def buildAndStoreIidoRefusalReceiver(motionId,
                                     sessionUuid,
                                     originalSessionUuid,
                                     supplierId,
                                     receiverId,
                                     refusedSsccs,
                                     refusedSgtins
                                    ):
    refusalReceiver = RefusalReceiver(subject_id = receiverId,
                                      shipper_id = supplierId,
                                      operation_date  = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL),
                                      reason = u'Несоответствие документа и факта',
                                      order_details=pyxb.BIND()
                                     )
    if refusedSsccs:
        refusalReceiver.order_details.sscc = refusedSsccs
    if refusedSgtins:
        refusalReceiver.order_details.sgtin = refusedSgtins

    outDoc = Documents(original_id = originalSessionUuid, # session_ui из входящего документа
                       session_ui  = sessionUuid,
                       refusal_receiver = refusalReceiver
                      )

    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iidoRefusalReceiver,
                             stage       = CMdlpStage.ready,
                             docType     = int(refusalReceiver.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def buildAndStoreIidoUnitUnpack(motionId,
                                sessionUuid,
                                receiverId,
                                confirmedSsccs
                               ):
    unitUnpack = UnitUnpack(subject_id      = receiverId,
                            operation_date  = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL),
                            sscc            = confirmedSsccs,
                            is_recursive    = True
                           )

    outDoc = Documents(session_ui  = sessionUuid,
                       unit_unpack = unitUnpack
                      )

    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iidoUnitUnpack,
                             stage       = CMdlpStage.ready,
                             docType     = int(unitUnpack.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def getIidoExchanges(logger, motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    for purpose in (CMdplExchangePurpose.iidoAccept,
                    CMdplExchangePurpose.iidoRefusalReceiver,
                    CMdplExchangePurpose.iidoUnitUnpack):
        ids = db.getIdList(table,
                           'id',
                           db.joinAnd([ table['master_id'].eq(motionId),
                                        table['purpose'].eq(purpose),
                                        table['stage'].inlist((CMdlpStage.ready, CMdlpStage.inProgress))
                                      ]
                                     ),
                           limit=1
                          )
        if ids:
            result.append(ids[0])
#            logger.append('чтение из базы данных %s', CMdplExchangePurpose.docType(purpose))
    return result




