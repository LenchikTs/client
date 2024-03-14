# -*- coding: utf-8 -*-
# iiwd: Internal Invoice - Withdrawal By Document
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# Выбытие по документу, и мы должны передать
# 531-health_care

import datetime # переделать на QDateTime!
#import json
import uuid

from PyQt4 import QtGui
# from PyQt4.QtCore import Qt, QDateTime

import isodate
import pyxb


from Exchange.MDLP.documents.v136 import Documents, HealthCare


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


# iiwd: Internal Invoice - Withdrawal By Document

@withWaitCursor
def iiwdProcess(logger,
                motionId,
                connection,
                supplierId,
                docNum,
                docDate,
                sgtins,
               ):
    motionStage = getMotionStage(motionId)
    if motionStage == CMdlpStage.ready:
        (healthCareId,) = prepareIiwdProcess(logger,
                                             motionId,
                                             connection,
                                             supplierId,
                                             docNum,
                                             docDate,
                                             sgtins
                                            )
        motionStage = CMdlpStage.inProgress
    elif motionStage == CMdlpStage.inProgress:
        (healthCareId,) = getIiwdExchanges(logger, motionId)

    if motionStage == CMdlpStage.inProgress:
        exchangeStages = []
        for exchangeId in [healthCareId]:
            if exchangeId:
                exchangeStage = execMdlpExchange(logger, exchangeId, connection)
                exchangeStages.append(exchangeStage)
        if exchangeStages:
            motionStage = max(motionStage, min(exchangeStages))
        else:
            motionStage = getMotionStageFromExchanges(motionId)
        setMotionStage(motionId, motionStage)
    return motionStage


def prepareIiwdProcess(logger,
                       motionId,
                       connection,
                       supplierId,
                       docNum,
                       docDate,
                       sgtins
                      ):
    sessionUuid = str(uuid.uuid4())
    QtGui.qApp.db.transaction()
    try:
        # показать: формирую документы
        healthCareId = None

        if sgtins:
            logger.append(u'формирование документа %s' % CMdplExchangePurpose.docType(CMdplExchangePurpose.iiwdHealthCare))
            healthCareId = buildAndStoreIiwdHealthCare(motionId,
                                                       sessionUuid,
                                                       supplierId,
                                                       docNum,
                                                       docDate,
                                                       sgtins,
                                                      )

        setMotionStage(motionId, CMdlpStage.inProgress)
        QtGui.qApp.db.commit()
        return (healthCareId,)
    except Exception as e:
        QtGui.qApp.db.rollback()
        raise e


def buildAndStoreIiwdHealthCare(motionId,
                                sessionUuid,
                                supplierId,
                                docNum,
                                docDate,
                                sgtins
                               ):
    healthCare = HealthCare(subject_id     = supplierId,                      # Идентификатор организации-отправителя
                            operation_date = datetime.datetime.now().replace(tzinfo=isodate.tzinfo.LOCAL), # Дата приемки
                            doc_date       = docDate.toString('dd.MM.yyyy'),  # Реквизиты документа, на основании которого осуществлена выдача - дата
                            doc_num        = docNum,                          # Реквизиты документа, на основании которого осуществлена выдача - номер
                            order_details  = pyxb.BIND(union=[pyxb.BIND()])
                           )

    utionType = type(healthCare.order_details.union[0])
    unions = []
    for sgtin in sgtins:
        unions.append(utionType(sgtin     = sgtin,
                               )
                     )
    healthCare.order_details.union = unions
    outDoc = Documents(session_ui  = sessionUuid,
                       health_care = healthCare
                      )
    rawOutDoc = outDoc.toxml('UTF-8').decode('utf8')
    return storeMdlpExchange(motionId,
                             purpose     = CMdplExchangePurpose.iiwdHealthCare,
                             stage       = CMdlpStage.ready,
                             docType     = int(healthCare.action_id),
                             requestId   = str(uuid.uuid4()),
                             xmlDocument = rawOutDoc
                            )


def getIiwdExchanges(logger, motionId):
    db = QtGui.qApp.db
    table = db.table('StockMotion_MdlpExchange')
    result = []
    for purpose in (CMdplExchangePurpose.iiwdHealthCare,
                   ):
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
#            logger.append('?')
    return result


