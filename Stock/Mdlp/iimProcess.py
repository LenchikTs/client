# -*- coding: utf-8 -*-
# iimProcess: internal Invoice - Move
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# Для перемещения мы должны передать
#   431-move_place

import datetime # переделать на QDateTime!
# import json
import uuid

from PyQt4 import QtGui
# from PyQt4.QtCore import Qt, QDateTime

import isodate
import pyxb


from Exchange.MDLP.documents.v136 import Documents, MovePlace


from library.Utils import withWaitCursor

from Stage import CMdlpStage
from ExchangePurpose import CMdplExchangePurpose
from Utils import ( getMotionStage,
                    getMotionStageFromExchanges,
                    setMotionStage,
                    storeMdlpExchange,
                    execMdlpExchange
                  )


# последействие для перемещения sgtins

# ????: internal invoice - move


@withWaitCursor
def iimProcess(logger,
               motionId,
               connection,
               supplierId,
               receiverId,
               docNum,
               docDate,
               sgtins
              ):
    # 431-move_place
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.ready:
        moveId = prepareIimProcess(logger,
                                   motionId,
                                   connection,
                                   supplierId,
                                   receiverId,
                                   docNum,
                                   docDate,
                                   sgtins
                                  )
        motionStage = CMdlpStage.inProgress
    elif motionStage == CMdlpStage.inProgress:
        (moveId,) = getIimExchanges(logger, motionId)

    if motionStage == CMdlpStage.inProgress:
        exchangeStages = []
        for exchangeId in [moveId]:
            if exchangeId:
                exchangeStage = execMdlpExchange(logger, exchangeId, connection)
                exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage


def prepareIimProcess(logger,
                      motionId,
                      connection,
                      supplierId,
                      receiverId,
                      docNum,
                      docDate,
                      sgtins
                     ):
    sessionUuid = str(uuid.uuid4())
    QtGui.qApp.db.transaction()
    try:
        # показать: формирую документы

        moveId = None

        if sgtins:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iimMovePlace))
            moveId = buildAndStoreIimMovePlace(motionId,
                                               sessionUuid,
                                               supplierId,
                                               receiverId,
                                               docNum,
                                               docDate,
                                               sgtins
                                              )

        setMotionStage(motionId, CMdlpStage.inProgress)
        QtGui.qApp.db.commit()
        return moveId
    except Exception as e:
        QtGui.qApp.db.rollback()
        raise e


def buildAndStoreIimMovePlace(motionId,
                              sessionUuid,
                              supplierId,
                              receiverId,
                              docNum,
                              docDate,
                              sgtins
                             ):
    movePlace = MovePlace(subject_id     = supplierId,  # Идентификатор организации-отправителя
                          receiver_id    = receiverId,  # Идентификатор организации-получателя
                          operation_date = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL), # Дата совершения операции
                          doc_num        = docNum,      # Реквизиты документа перемещения: номер документа
                          doc_date       = docDate.toString('dd.MM.yyyy'),# Реквизиты документа перемещения: дата документа
                          order_details  = pyxb.BIND()
                         )

    movePlace.order_details.sgtin = sgtins
    outDoc = Documents(session_ui    = sessionUuid,
                       move_place    = movePlace
                      )
    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iimMovePlace,
                             stage       = CMdlpStage.ready,
                             docType     = int(movePlace.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def getIimExchanges(logger, motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    for purpose in (CMdplExchangePurpose.iimMovePlace,):
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
#            logger.append('???')
    return result


