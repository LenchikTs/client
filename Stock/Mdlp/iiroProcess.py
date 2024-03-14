# -*- coding: utf-8 -*-
# iiro: Incoming Invoice - Reverse Order
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# У нас обратный порядок, и мы должны передать
#   416-receive_order
#   912-unit_unpack (возможно, что после подтв.416)

import datetime # переделать на QDateTime!
import json
import uuid

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDateTime

import isodate
import pyxb


from Exchange.MDLP.documents.v136 import Documents, ReceiveOrder, UnitUnpack


#from library.DialogBase import CDialogBase
from library.Utils import withWaitCursor

#from connection import CMdlpConnection
from Stage import CMdlpStage
from ExchangePurpose import CMdplExchangePurpose
from Utils import ( getMotionStage,
                    getMotionStageFromExchanges,
                    setMotionStage,
                    storeMdlpExchange,
                    execMdlpExchange
                  )


# последействия для обратного порядка приёма
# нам нужно:
# - если есть принятые sscc или sgtin, то сформиривать и передать 416-receive_order
# - если есть sscc, то передать 912-unit_unpack (возможно, что после подтв.416)
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


# IIDRO: incoming invoice - reverse order


@withWaitCursor
def iiroProcess(logger,
                motionId,
                connection,
                supplierId,
                receiverId,
                docNum,
                docDate,
                confirmedSsccsWithSumAndVat,
                confirmedSgtinsWithSumAndVat
               ):
    # всякие хлопоты после приёма накладной по обратному порядку
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.ready:
        receiveOrderId, wanId, unitUnpackId = prepareIiroProcess(logger,
                                                                 motionId,
                                                                 connection,
                                                                 supplierId,
                                                                 receiverId,
                                                                 docNum,
                                                                 docDate,
                                                                 confirmedSsccsWithSumAndVat,
                                                                 confirmedSgtinsWithSumAndVat
                                                                )
        motionStage = CMdlpStage.inProgress
    elif motionStage == CMdlpStage.inProgress:
        receiveOrderId, wanId, unitUnpackId = getIiroExchanges(logger, motionId)

    if motionStage == CMdlpStage.inProgress:
        exchangeStages = []
        for exchangeId in [receiveOrderId, wanId, unitUnpackId]:
            if exchangeId:
                exchangeStage = execMdlpExchange(logger, exchangeId, connection)
                exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage


def prepareIiroProcess(logger,
                       motionId,
                       connection,
                       supplierId,
                       receiverId,
                       docNum,
                       docDate,
                       confirmedSsccsWithSumAndVat,
                       confirmedSgtinsWithSumAndVat
                      ):
    sessionUuid = str(uuid.uuid4())
    QtGui.qApp.db.transaction()
    try:
        # показать: формирую документы

        receiveOrderId = wanId = unitUnpackId = None

        if confirmedSsccsWithSumAndVat or confirmedSgtinsWithSumAndVat:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iiroReceiveOrder))
            receiveOrderId = buildAndStoreIiroReceiveOrder(motionId,
                                                           sessionUuid,
                                                           supplierId,
                                                           receiverId,
                                                           docNum,
                                                           docDate,
                                                           confirmedSsccsWithSumAndVat,
                                                           confirmedSgtinsWithSumAndVat
                                                          )

            logger.append(u'формирование записи ожидания документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iiroWaitAcceptNotification))
            wanId = buildAndStoreIiroWaitAcceptNotification(motionId,
                                                            receiveOrderId,
                                                            supplierId,
                                                            confirmedSsccsWithSumAndVat,
                                                            confirmedSgtinsWithSumAndVat
                                                           )



        if confirmedSsccsWithSumAndVat:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iiroUnitUnpack))
            unitUnpackId = buildAndStoreIiroUnitUnpack(motionId,
                                                       wanId,
                                                       sessionUuid,
                                                       receiverId,
                                                       confirmedSsccsWithSumAndVat
                                                      )
        setMotionStage(motionId, CMdlpStage.inProgress)
        QtGui.qApp.db.commit()
        return (receiveOrderId, wanId, unitUnpackId)
    except Exception as e:
        QtGui.qApp.db.rollback()
        raise e


def buildAndStoreIiroReceiveOrder(motionId,
                                  sessionUuid,
                                  supplierId,
                                  receiverId,
                                  docNum,
                                  docDate,
                                  confirmedSsccsWithSumAndVat,
                                  confirmedSgtinsWithSumAndVat
                           ):
    receiveOrder = ReceiveOrder(subject_id     = receiverId,  # Идентификатор поликлиники
                                shipper_id     = supplierId,  # Идентификатор грузоотправителя
                                operation_date = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL), # Дата приемки
                                doc_num        = docNum,                        # Номер документа
                                doc_date       = docDate.toString('dd.MM.yyyy'),# Дата документа
                                receive_type   = 1,                             # Вид операции приемки, «1» - поступление
                                source         = 1,                             # Источник финансирования «1» собственные средства
                                contract_type  = 1,                             # Тип договора «1» - купля-продажа
                                order_details  = pyxb.BIND(union=[pyxb.BIND()])
                               )

    utionType = type(receiveOrder.order_details.union[0])
    unions = []
    for (sscc, sum, vat) in confirmedSsccsWithSumAndVat:
        unions.append(utionType(sscc_detail = pyxb.BIND(sscc=sscc),
                                cost      ='%.02f'  % sum,
                                vat_value = '%.02f' % vat
                               )
                     )
    for (sgtin, sum, vat) in confirmedSgtinsWithSumAndVat:
        unions.append(utionType(sgtin     = sgtin,
                                cost      ='%.02f'  % sum,
                                vat_value = '%.02f' % vat
                               )
                     )
    receiveOrder.order_details.union = unions
    outDoc = Documents(session_ui    = sessionUuid,
                       receive_order = receiveOrder
                      )
    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iiroReceiveOrder,
                             stage       = CMdlpStage.ready,
                             docType     = int(receiveOrder.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def buildAndStoreIiroWaitAcceptNotification(motionId,
                                            receiveOrderId,
                                            supplierId,
                                            confirmedSsccsWithSumAndVat,
                                            confirmedSgtinsWithSumAndVat
                                           ):
    now = QDateTime.currentDateTime()
    filterAsString   = json.dumps({'docType'  : 607,
                                   'senderId' : supplierId,
                                   'begDate'  : unicode(now.toString(Qt.ISODate)),
                                   'endDate'  : unicode(now.addDays(21).toString(Qt.ISODate)),
                                  }
                                 )
    requiredSsccs  = sorted([x[0] for x in confirmedSsccsWithSumAndVat])
    requiredSgtins = sorted([x[0] for x in confirmedSgtinsWithSumAndVat])
    progressAsString = json.dumps({ 'required': { 'ssccs' : requiredSsccs,
                                                  'sgtins': requiredSgtins
                                                },
                                    'received': { 'ssccs' : [],
                                                  'sgtins': []
                                                }
                                  }
                                 )
    return storeMdlpExchange(motionId,
                             runAfterId  = receiveOrderId,
                             purpose     = CMdplExchangePurpose.iiroWaitAcceptNotification,
                             stage       = CMdlpStage.ready,
                             docType     = 607,
                             filter      = filterAsString,
                             progress    = progressAsString
                            )


def buildAndStoreIiroUnitUnpack(motionId,
                                waitAcceptNotificationId,
                                sessionUuid,
                                receiverId,
                                confirmedSsccsWithSumAndVat
                               ):
    unitUnpack = UnitUnpack(subject_id      = receiverId,
                            operation_date  = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL),
                            sscc            = [sscc
                                               for (sscc, sum, vat) in confirmedSsccsWithSumAndVat
                                              ],
                            is_recursive    = True
                           )

    outDoc = Documents(session_ui  = sessionUuid,
                       unit_unpack = unitUnpack
                      )

    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             runAfterId  = waitAcceptNotificationId,
                             purpose     = CMdplExchangePurpose.iiroUnitUnpack,
                             stage       = CMdlpStage.ready,
                             docType     = int(unitUnpack.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def getIiroExchanges(logger, motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    for purpose in (CMdplExchangePurpose.iiroReceiveOrder,
                    CMdplExchangePurpose.iiroWaitAcceptNotification,
                    CMdplExchangePurpose.iiroUnitUnpack):
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
#            logger.append()
    return result


