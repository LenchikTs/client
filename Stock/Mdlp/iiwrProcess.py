# -*- coding: utf-8 -*-
# iiwr: Internal Invoice - Withdrawal By Registrar
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# Выбытие по регистратору,
# мы просто сохраняем себе для памяти 10531-skzkm_health_care.xsd

#import datetime
#import uuid

#import isodate
#import pyxb

from PyQt4 import QtGui

#from Exchange.MDLP.documents.v136 import createFromXml, Documents, Accept, RefusalReceiver, UnitUnpack


#from library.DialogBase import CDialogBase
from library.Utils import withWaitCursor

#from connection import CMdlpConnection
from Stage import CMdlpStage
from ExchangePurpose import CMdplExchangePurpose
from Utils import ( # getMotionStage,
                    # getMotionStageFromExchanges,
                    setMotionStage,
                    storeMdlpExchange,
                    # execMdlpExchange,
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
def iiwrProcess(logger,
                motionId,
                connection,
                documentIds,
               ):
    # всякие хлопоты после приёма накладной по прямому порядку
    if documentIds:
        rawOuterDocs = []
        for documentId in documentIds:
           logger.append('загрузка из МДЛП документа c id %s' % documentId)
           rawOuterDocs.append((documentId, connection.getRawDocument(documentId)))
        QtGui.qApp.db.transaction()
        try:
            for (documentId, rawOuterDoc) in rawOuterDocs:
                storeMdlpExchange(motionId,
                                  purpose=CMdplExchangePurpose.iiwrKzkmHealthCare,
                                  stage=CMdlpStage.unnecessary,
                                  docType=10531,
                                  documentId=documentId,
                                  xmlDocument=rawOuterDoc
                                 )

            setMotionStage(motionId, CMdlpStage.unnecessary)
            QtGui.qApp.db.commit()
        except Exception as e:
            QtGui.qApp.db.rollback()
            raise e
    else:
        setMotionStage(motionId, CMdlpStage.unnecessary)
    return CMdlpStage.unnecessary
