# -*- coding: utf-8 -*-
# iinm: Incoming Invoice - Notification Mode
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# У нас обратный порядок в уведомительном режиме, и мы должны передать
#    702-posting
#   912-unit_unpack (возможно, что после подтверждения 627-posting_notification)

import datetime # переделать на QDateTime!
#import json
import uuid

from PyQt4 import QtGui
#from PyQt4.QtCore import Qt, QDateTime

import isodate
import pyxb


from Exchange.MDLP.documents.v136 import Documents, Posting, UnitUnpack


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
def iinmProcess(logger,
                motionId,
                connection,
                supplierId,
                supplierInn,
                supplierKpp,
                receiverId,
                docNum,
                docDate,
                confirmedSsccsWithSumAndVat,
                confirmedSgtinsWithSumAndVat
               ):
    # всякие хлопоты после приёма накладной при работе в режиме уведомления
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.ready:
        postingId, unitUnpackId = prepareIinmProcess(logger,
                                                     motionId,
                                                     connection,
                                                     supplierId,
                                                     supplierInn,
                                                     supplierKpp,
                                                     receiverId,
                                                     docNum,
                                                     docDate,
                                                     confirmedSsccsWithSumAndVat,
                                                     confirmedSgtinsWithSumAndVat
                                                    )
        motionStage = CMdlpStage.inProgress
    elif motionStage == CMdlpStage.inProgress:
        postingId, unitUnpackId = getIinmExchanges(logger, motionId)

    if motionStage == CMdlpStage.inProgress:
        exchangeStages = []
        for exchangeId in [postingId, unitUnpackId]:
            if exchangeId:
                exchangeStage = execMdlpExchange(logger, exchangeId, connection)
                exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage


def prepareIinmProcess(logger,
                       motionId,
                       connection,
                       supplierId,
                       supplierInn,
                       supplierKpp,
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
        postingId = unitUnpackId = None
        if confirmedSsccsWithSumAndVat or confirmedSgtinsWithSumAndVat:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iinmPosting))
            postingId = buildAndStoreIinmPosting(motionId,
                                                 sessionUuid,
                                                 supplierInn,
                                                 supplierKpp,
                                                 receiverId,
                                                 docNum,
                                                 docDate,
                                                 confirmedSsccsWithSumAndVat,
                                                 confirmedSgtinsWithSumAndVat
                                                )

        if confirmedSsccsWithSumAndVat:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iinmUnitUnpack))
            unitUnpackId = buildAndStoreIinmUnitUnpack(motionId,
                                                       postingId,
                                                       sessionUuid,
                                                       receiverId,
                                                       confirmedSsccsWithSumAndVat
                                                      )
        setMotionStage(motionId, CMdlpStage.inProgress)
        QtGui.qApp.db.commit()
        return (postingId, unitUnpackId)
    except Exception as e:
        QtGui.qApp.db.rollback()
        raise e


def buildAndStoreIinmPosting(motionId,
                             sessionUuid,
                             supplierInn,
                             supplierKpp,
                             receiverId,
                             docNum,
                             docDate,
                             confirmedSsccsWithSumAndVat,
                             confirmedSgtinsWithSumAndVat
                            ):
    posting = Posting(subject_id     = receiverId,  # Идентификатор поликлиники
                      shipper_info   = pyxb.BIND(inn=supplierInn),
                      operation_date = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL), # Дата приемки
                      doc_num        = docNum,                        # Номер документа
                      doc_date       = docDate.toString('dd.MM.yyyy'),# Дата документа
                      contract_type  = 1,                             # Тип договора «1» - купля-продажа
                      source         = 1,                             # Источник финансирования «1» собственные средства
                      order_details  = pyxb.BIND(union=[pyxb.BIND()])
                     )
    if supplierKpp:
        posting.shipper_info.kpp = supplierKpp
    utionType = type(posting.order_details.union[0])
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
    posting.order_details.union = unions
    outDoc = Documents(session_ui = sessionUuid,
                       posting    = posting
                      )
    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iinmPosting,
                             stage       = CMdlpStage.ready,
                             docType     = int(posting.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def buildAndStoreIinmUnitUnpack(motionId,
                                postingId,
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
                             runAfterId  = postingId,
                             purpose     = CMdplExchangePurpose.iinmUnitUnpack,
                             stage       = CMdlpStage.ready,
                             docType     = int(unitUnpack.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def getIinmExchanges(logger, motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    for purpose in (CMdplExchangePurpose.iinmPosting,
                    CMdplExchangePurpose.iinmUnitUnpack):
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


