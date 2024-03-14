#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Интерфейсный объект для свсзи с МДЛП
##
#############################################################################

import base64
import json
import time
import logging
import urllib
import uuid
from datetime import date, datetime, timedelta

import isodate
import requests

from documents.v136 import createFromXml
from UrlComporents import CUrlComporents
from library.Utils import anyToUnicode


class CMdlp(object):
    contentTypeJson = 'application/json;charset=UTF-8'

    defaultBaseUrl = 'https://api.sb.mdlp.crpt.ru//api/v1/'

    dirAuth                    = 'auth'                               # 6.2.1. Метод для получения кода аутентификации
    dirToken                   = 'token'                              # 6.2.2. Метод для получения ключа сессии
    dirLogout                  = 'auth/logout'                        # 6.2.3. Метод для выхода из системыEndpoint: GET <endpoint>/<version>/auth/logout

    dirDocumentsSend           = 'documents/send'                     # 5.1. Отправка документа
    dirDocumentsOutcome             = 'documents/outcome'             # 5.11. Получение списка исходящих документов
    dirDocumentsOutcomeFromShowcase = 'documents/showcase/outcome'    # 5.12. Получение списка исходящих документов из витрины документов
    dirDocumentsIncome              = 'documents/income'              # 5.13. Получение списка входящих документов
    dirDocumentsIncomeFromShowcase  = 'documents/showcase/income'     # 5.14. Получение списка входящих документов из витрины документов

    dirDocumentDownload        = 'documents/download/%s'
    dirDocumentReceiptDownload = 'documents/%s/ticket'                # 5.19. Получение квитанции по номеру исходящего документа

    # удалено, так как ищет только среди своих подразделений.
    #    dirBranches                = 'reestr/branches/filter'             # 8.1.2. Метод для поиска информации о местах осуществления деятельности по фильтру
    dirBranchInfo              = 'reestr/branches/%s'                 # 8.1.4. Получение информации о конкретном месте осуществления деятельности
    #    dirWarehouses              = 'reestr/warehouses/filter'           # 8.2.2. Метод для поиска информации о местах ответственного хранения по фильтру
    #    dirWarehouseInfo           = 'reestr/warehouses/%s'               # 8.2.3. Получение информации о конкретном месте ответственного хранения

    dirSgtins                  = 'reestr/sgtin/filter'                # 8.3.1. Метод для поиска по реестру КИЗ
    dirSgtinsByList            = 'reestr/sgtin/sgtins-by-list'        # 8.3.2. Метод поиска по реестру КИЗ по списку значений
    dirPublicSgtinsByList      = 'reestr/sgtin/public/sgtins-by-list' # 8.3.3. Метод поиска по общедоступному реестру КИЗ по списку значений
    dirSgtinInfo               = 'reestr/sgtin/%s'                    # 8.3.5. Метод для получения детальной информации о КИЗ и связанным с ним ЛП

    dirSsccHierarchy           = 'reestr/sscc/%s/hierarchy'           # 8.4.1. Метод для получения информации об иерархии вложенности третичной упаковки
    dirSsccSgtins              = 'reestr/sscc/%s/sgtins'              # 8.4.2. Метод для получения информации о КИЗ, вложенных в третичную упаковку
    dirSsccFullHierarchy       = 'reestr/sscc/%s/full-hierarchy'      # 8.4.3. Метод для получения информации о полной иерархии вложенности третичной упаковки
    dirSsccFullHierarchyByList = 'reestr/sscc/full-hierarchy'         # 8.4.4. Метод для получения информации о полной иерархии вложенности третичной упаковки для нескольких SSCC

    dirPublicProducts          = 'reestr/med_products/public/filter'  # 8.5.3. Метод для поиска публичной информации в реестре производимых ЛП
    dirPartners                = 'reestr_partners/filter'             # 8.8.1. Получение информации о субъектах обращения (участниках ИС "Маркировка")


    mapActionToInterval        = { # dirAuth                     :  1.0,
                                   # dirToken                    :  1.0,
                                   # dirLogout                   :  1.0,
                                   'postDocument'                    :  0.5,
                                   'getOutcomingDocuments'            :  1.0,
                                   'getOutcomingDocumentsFromShowcase':  1.0,
                                   'getIncomingDocuments'             :  1.0,
                                   'getIncomingDocumentsFromShowcase' :  1.0,
                                   'getBranchInfo'                    :  0.5,
                                   'getDocumentReceiptUrl'            :  0.5,
                                   'getSgtinsByList'                  : 10.0,
                                   'getSgtinInfo'                     :  0.5,
                                   'getSsccHierarchy'                 : 20.0,
                                   'getSsccSgtins'                    :  5.0,
                                   'getSsccFullHierarchy'             : 30.0,
                                   'getSsccFullHierarchyByList'       : 30.0,
                                   'getPublicProducts'                :  5.0,
                                   'getPartners'                      :  1.0
                                 }


    def __init__(self, api, baseUrl=None):
        self._api           = api
        self.setBaseUrl(baseUrl)
        self._clientId      = None
        self._clientSecret  = None
        self._certHash      = None
        self._cert          = None
        self._certProvider  = None
        self._token         = None
        self._tokenExpired  = None
        self._mapActionToInterval = dict(self.mapActionToInterval)
        self._mapActionToLastCall = {}
        self._cleanUrlMorphRules()


    #################################################
    #
    # Интерфейсные методы

    def getBaseUrl(self):
        return self._baseUrl or self.defaultBaseUrl


    def setBaseUrl(self, baseUrl):
        if baseUrl and not baseUrl.endswith('/'):
            baseUrl += '/'
        self._baseUrl = baseUrl


    baseUrl = property(getBaseUrl, setBaseUrl)


    def setStunnel(self, target, subst):
        # я не вижу как настроить stunnel из Крипто-Про как proxy,
        # только как SSL/TLS тунель :(
        # поэтому делаем так:
        # target: куда я хочу попасть, важно схема + host + port + path, например 'https://api.sb.mdlp.crpt.ru'
        # subst:  на что заменять, важно  схема + host + port, например 'http://localhost'
        # предполагается, что в случае совпадения url target.схема, target.host, target.port и начала path c target.path
        # нужно заменить на subst.схема, subst.host и subst.port;
        # сейчас мне достаточно одного правила.
        self._cleanUrlMorphRules()
        self._addUrlMorphRules(target, subst)


    def setAuth(self, clientId, clientSecret, certHash):
        self._clientId     = clientId
        self._clientSecret = clientSecret
        self._certHash     = certHash
        self._certProvider = None
        self._cert         = None
        self._tokenExpired = datetime.now() + timedelta(seconds=-5)
        self._token        = False


    def auth(self, clientId, clientSecret, certHash):
        self.setAuth(clientId, clientSecret, certHash)
        self._auth()


    def close(self):
        self._close()


    def getDocument(self, documentId):
        xml = self.getRawDocument(documentId)
        return createFromXml(xml)


    def getRawDocument(self, documentId):
        documentUrl = self._getDocumentUrl(documentId)
        return self._downloadDocument(documentUrl)


    def getDocumentReceipt(self, documentId):
        xml = self.getDocumentRawReceipt(documentId)
        if xml:
           return createFromXml(xml)
        return None


    def getDocumentRawReceipt(self, documentId):
        receiptUrl = self._getDocumentReceiptUrl(documentId)
        if receiptUrl:
            return self._downloadDocument(receiptUrl)
        return None


    def getRequestId(self):
        return str(uuid.uuid4())


    def postDocument(self, document, requestId=None):
        xml = document.toxml('UTF-8')
        return self.postRawDocument(xml, requestId)


    def postRawDocument(self, xml, requestId=None):
        if isinstance(xml, unicode):
            xml = xml.encode('utf-8')
        signature = self._getCert().createDetachedSignature(xml)

        query = {'document'  : base64.b64encode(xml),
                 'sign'      : base64.b64encode(signature),
                 'request_id': requestId or self.getRequestId(),
                }
        response = self._post('postDocument', self.dirDocumentsSend, query)
        if response.status_code == 200:
            return response.json()['document_id']
        self._raiseExceptionFromResponse('postDocument', response)


    def getOutcomingDocumentsByPages(self,
                                     count              = 100,
                                     begDate            = None,                # Дата начала периода фильтрации
                                     endDate            = None,                # Дата окончания  периода фильтрации
                                     documentId         = None,                # Уникальный  идентификатор документа
                                     requestId          = None,                # Уникальный  идентификатор запроса
                                     docType            = None,                # Тип документа
#                                     docStatus          = 'PROCESSED_DOCUMENT',# Статус документа
                                     docStatus          = None,                # Статус документа
                                     fileUploadType     = None,                # Тип загрузки в систему
                                     begProcessedDate   = None,                # Дата обработки документа: начало периода
                                     endProcessedDate   = None,                # Дата обработки документа: окончание периода
                                     senderId           = None,                # Уникальный идентификатор отправителя, sysId или branchId - смотря по документку
                                     receiverId         = None                 # Уникальный идентификатор получателя, sysId или branchId - смотря по документку
                                    ):
        # 5.11. Получение списка исходящих документов
        query = {'count'  : count,
                 'filter' : self._prepareFilter( locals(),
                                                 ( ('begDate',          'start_date',          self._dateToStr),
                                                   ('endDate',          'end_date',            self._dateToStrUp),
                                                   ('documentId',       'document_id',         None),
                                                   ('requestId',        'request_id',          None),
                                                   ('docType',          'doc_type',            None),
                                                   ('docStatus',        'doc_status',          None),
                                                   ('fileUploadType',   'file_uploadtype',     None),
                                                   ('begProcessedDate', 'processed_date_from', self._dateToStr),
                                                   ('endProcessedDate', 'processed_date_to',   self._dateToStrUp),
                                                   ('senderId',         'sender_id',           None),
                                                   ('receiverId',       'receiver_id',         None)
                                                  )
                                               ),
                }
        start = 0
        prevTotal = 0
        documents = []
        while True:
            query['start_from'] = start
            response = self._post('getOutcomingDocuments', self.dirDocumentsOutcome, query)
            if response.status_code != 200:
                self._raiseExceptionFromResponse('getOutcomingDocuments', response)
            data = response.json()
            total = data['total']
            if start == 0:
                prevTotal = total
            elif prevTotal != total:
                start = 0
                documents = []
                continue
            documents.extend(data['documents'])
            start += len(data['documents'])
            if (    len(data['documents']) == 0 # ничего не вернулось
                 or len(documents) >= count     # получено сколько просили
                 or len(documents) >= total     # получено сколько есть
               ):
                break
        return [ COutcomingDocument(self, doc) for doc in documents[:count] ]


    def getOutcomingDocumentsFromShowcase(self,
                                          count              = 100,
                                          begDate            = None,                # Дата начала периода фильтрации
                                          endDate            = None,                # Дата окончания  периода фильтрации
                                          documentId         = None,                # Уникальный  идентификатор документа
                                          requestId          = None,                # Уникальный  идентификатор запроса
                                          docType            = None,                # Тип документа
#                                          docStatus          = 'PROCESSED_DOCUMENT',# Статус документа
                                          docStatus          = None,                # Статус документа
                                          fileUploadType     = None,                # Тип загрузки в систему
                                          begProcessedDate   = None,                # Дата обработки документа: начало периода
                                          endProcessedDate   = None,                # Дата обработки документа: окончание периода
                                          senderId           = None,                # Уникальный идентификатор отправителя, sysId или branchId - смотря по документку
                                          receiverId         = None                 # Уникальный идентификатор получателя, sysId или branchId - смотря по документку
                                         ):
        # 5.12. Получение списка исходящих документов из витрины документов
        query = {'count'  : count,
                 'filter' : self._prepareFilter( locals(),
                                                 ( ('begDate',          'start_date',          self._dateToStr),
                                                   ('endDate',          'end_date',            self._dateToStrUp),
                                                   ('documentId',       'document_id',         None),
                                                   ('requestId',        'request_id',          None),
                                                   ('docType',          'doc_type',            None),
                                                   ('docStatus',        'doc_status',          None),
                                                   ('fileUploadType',   'file_uploadtype',     None),
                                                   ('begProcessedDate', 'processed_date_from', self._dateToStr),
                                                   ('endProcessedDate', 'processed_date_to',   self._dateToStrUp),
                                                   ('senderId',         'sender_id',           None),
                                                   ('receiverId',       'receiver_id',         None)
                                                  )
                                               ),
                }
        documents = []
        while True:
            response = self._post('getOutcomingDocumentsFromShowcase', self.dirDocumentsOutcomeFromShowcase, query)
            if response.status_code != 200:
                self._raiseExceptionFromResponse('getOutcomingDocumentsFromShowcase', response)
            data = response.json()
            documents.extend(data['documents'])
            npk = data.get('next_page_key')
            if (    npk is None                     # как я понял, это признак того что всё возвращено и больше ничего не будет
                 or len(documents) >= count         # получено сколько просили
                 or len(documents) >= data['total'] # получено сколько есть
               ):
                break
            query['next_page_key'] = npk
        return [ COutcomingDocument(self, doc) for doc in documents[:count] ]

    getOutcomingDocuments = getOutcomingDocumentsFromShowcase


    def getIncomingDocumentsByPages(self,
                                    count            = 100,
                                    begDate          = None,                # Дата начала периода фильтрации
                                    endDate          = None,                # Дата окончания  периода фильтрации
                                    documentId       = None,                # Уникальный  идентификатор документа
                                    requestId        = None,                # Уникальный  идентификатор запроса
                                    docType          = None,                # Тип документа
                                    docStatus        = 'PROCESSED_DOCUMENT',# Статус документа
                                    fileUploadType   = None,                # Тип загрузки в систему
                                    begProcessedDate = None,                # Дата обработки документа: начало периода
                                    endProcessedDate = None,                # Дата обработки документа: окончание периода
                                    senderId         = None,                # Уникальный идентификатор отправителя, sysId или branchId - смотря по документку
                                    receiverId       = None,                # Уникальный идентификатор получателя, sysId или branchId - смотря по документку
                                    onlyNew          = None,                # Признак, регулирующий возможность получать только новые (непрочитанные) документы
                                   ):
        # 5.13. Получение списка входящих документов
        query = {'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('begDate',          'start_date',          self._dateToStr),
                                                      ('endDate',          'end_date',            self._dateToStrUp),
                                                      ('documentId',       'document_id',         None),
                                                      ('requestId',        'request_id',          None),
                                                      ('docType',          'doc_type',            None),
                                                      ('docStatus',        'doc_status',          None),
                                                      ('fileUploadType',   'file_uploadtype',     None),
                                                      ('begProcessedDate', 'processed_date_from', self._dateToStr),
                                                      ('endProcessedDate', 'processed_date_to',   self._dateToStrUp),
                                                      ('senderId',         'sender_id',           None),
                                                      ('receiverId',       'receiver_id',         None),
                                                      ('onlyNew',          'only_new',            None),
                                                    )
                                                  ),
                }

        start = 0
        prevTotal = 0
        documents = []
        while True:
            query['start_from'] = start
            response = self._post('getIncomingDocuments', self.dirDocumentsIncome, query)
            if response.status_code != 200:
                self._raiseExceptionFromResponse('getIncomingDocuments', response)
            data = response.json()
            total = data['total']
            if start == 0:
                prevTotal = total
            elif prevTotal != total:
                start = 0
                documents = []
                continue
            documents.extend(data['documents'])
            start += len(data['documents'])
            if (    len(data['documents']) == 0 # ничего не вернулось
                 or len(documents) >= count     # получено сколько просили
                 or len(documents) >= total     # получено сколько есть
               ):
                break
        return [ CIncomingDocument(self, doc) for doc in documents[:count] ]



    def getIncomingDocumentsFromShowcase(self,
                              count            = 100,
                              begDate          = None,                # Дата начала периода фильтрации
                              endDate          = None,                # Дата окончания  периода фильтрации
                              documentId       = None,                # Уникальный  идентификатор документа
                              requestId        = None,                # Уникальный  идентификатор запроса
                              docType          = None,                # Тип документа
                              docStatus        = 'PROCESSED_DOCUMENT',# Статус документа
                              fileUploadType   = None,                # Тип загрузки в систему
                              begProcessedDate = None,                # Дата обработки документа: начало периода
                              endProcessedDate = None,                # Дата обработки документа: окончание периода
                              senderId         = None,                # Уникальный идентификатор отправителя, sysId или branchId - смотря по документку
                              receiverId       = None,                # Уникальный идентификатор получателя, sysId или branchId - смотря по документку
                              onlyNew          = None,                # Признак, регулирующий возможность получать только новые (непрочитанные) документы
                             ):
        # 5.14. Получение списка входящих документов из витрины документов
        query = {'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('begDate',          'start_date',          self._dateToStr),
                                                      ('endDate',          'end_date',            self._dateToStrUp),
                                                      ('documentId',       'document_id',         None),
                                                      ('requestId',        'request_id',          None),
                                                      ('docType',          'doc_type',            None),
                                                      ('docStatus',        'doc_status',          None),
                                                      ('fileUploadType',   'file_uploadtype',     None),
                                                      ('begProcessedDate', 'processed_date_from', self._dateToStr),
                                                      ('endProcessedDate', 'processed_date_to',   self._dateToStrUp),
                                                      ('senderId',         'sender_id',           None),
                                                      ('receiverId',       'receiver_id',         None),
                                                      ('onlyNew',          'only_new',            None),
                                                    )
                                                  ),
                }
        documents = []
        while True:
            response = self._post('getIncomingDocumentsFromShowcase', self.dirDocumentsIncomeFromShowcase, query)
            if response.status_code != 200:
                self._raiseExceptionFromResponse('getIncomingDocumentsFromShowcase', response)
            data = response.json()
            documents.extend(data['documents'])
            npk = data.get('next_page_key')
            if (    npk is None                     # как я понял, это признак того что всё возвращено
                 or len(documents) >= count         # получено сколько просили
                 or len(documents) >= data['total'] # получено сколько есть
               ):
                break
            query['next_page_key'] = npk
        return [ CIncomingDocument(self, doc) for doc in documents[:count] ]

    getIncomingDocuments = getIncomingDocumentsFromShowcase


    def getBranch(self, branchId):
        # 8.1.3. Получение информации о конкретном месте осуществления деятельности
        response = self._get('getBranchInfo', self.dirBranchInfo % urllib.quote_plus(branchId))
        if response.status_code == 200:
            # return response.json()
            return CBranchInformation(self, response.json())
        self._raiseExceptionFromResponse('getBranchInfo', response)


    def getSgtins(self,
                  start   = 0,
                  count   = 100,
                  status  = None,
                  gtin    = None,
                  sgtin   = None,
                  ownerId = None, # sysId или branchId
                 ):
        # 8.3.1. Метод для поиска по реестру КИЗ
        query = {'start_from': start,
                 'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('status',  'status', None),
                                                      ('gtin',    'gtin',   None),
                                                      ('sgtin',   'sgtin',  None),
                                                      ('ownerId', 'sys_id', None),
                                                    )
                                                  ),
                }
        response = self._post('getSgtins', self.dirSgtins, query)
        if response.status_code == 200:
            data = response.json()
            return [ CSgtinInformation(self, entry)
                     for entry in data.get('entries', [])
                   ]
        self._raiseExceptionFromResponse('getSgtins', response)


    def getSgtinsByList(self, sgtins):
        # 8.3.2. Метод поиска по реестру КИЗ по списку значений
        # * — Максимальное количество элементов в списке запрашиваемых КИЗ: 500
        MAXCNT = 500

        succeedSgtins = []
        failedSgtins  = []

        for i in xrange(0, len(sgtins), MAXCNT):
            query = {'filter':{ 'sgtins': sgtins[i:i+MAXCNT]}}
            response = self._post('getSgtinsByList', self.dirSgtinsByList, query)

            if response.status_code == 200:
                data = response.json()
                for entry in data.get('entries', []):
                    succeedSgtins.append( CSgtinInformation(self, entry) )
                for entry in data.get('failed_entries', []):
                    failedSgtins.append( CFailedSgtinInformation(self, entry) )
            else:
                self._raiseExceptionFromResponse('getSgtinsByList', response)
        return (succeedSgtins, failedSgtins)


    def getPublicSgtinsByList(self, sgtins):
        # 8.3.3. Метод поиска по общедоступному реестру КИЗ по списку значений
        # * — Максимальное количество элементов в списке запрашиваемых КИЗ: 500
        query = {'filter' : { 'sgtins': sgtins },
                }
        response = self._post('getPublicSgtinsByList', self.dirPublicSgtinsByList, query)
        if response.status_code == 200:
            data = response.json()
            return ( [ CPublicSgtinInformation(self, entry)
                       for entry in data.get('entries', [])
                     ],
                     [ CFailedSgtinInformation(self, entry)
                       for entry in data.get('failed_entries', [])
                     ]
                   )
        self._raiseExceptionFromResponse('getPublicSgtinsByList', response)


    def getSgtinInfo(self, sgtin):
        # 8.3.4. Метод для получения детальной информации о КИЗ и связанным с ним ЛП
        # я забью на какую-то инф. по gtin
        response = self._get('getSgtinInfo', self.dirSgtinInfo % urllib.quote_plus(sgtin))
        if response.status_code == 200:
            data = response.json()
            return CSgtinInformation(self, data['sgtin_info'])
        self._raiseExceptionFromResponse('getSgtinInfo', response)


    def getSsccHierarchy(self, sscc):
        # 8.4.1. Метод для получения информации об иерархии вложенности третичной упаковки
        response = self._get('getSsccHierarchy', self.dirSsccHierarchy % urllib.quote_plus(sscc))
        if response.status_code == 200:
            return C841HierarchyInformation(self, response.json())
        self._raiseExceptionFromResponse('getSsccHierarchy', response)


    def getSsccSgtins(self, sscc, start=0, count=100, isVed=None, inHcl=None):
        # 8.4.2. Метод для получения информации о КИЗ, вложенных в третичную упаковку
        query = {'start_from': start,
                 'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('isVed', 'gnvlp',    None),
                                                      ('inHcl', 'vzn_drug', None),
                                                    )
                                                  ),
                }
        response = self._post('getSsccSgtins', self.dirSsccSgtins % urllib.quote_plus(sscc), query)
        if response.status_code == 200:
            return CGetSsccSgtinsResult(self, response.json())
        self._raiseExceptionFromResponse('getSsccSgtins', response)


    def getSsccFullHierarchy(self, sscc):
        # 8.4.3. Метод для получения информации о полной иерархии вложенности третичной упаковки
        response = self._get('getSsccFullHierarchy', self.dirSsccFullHierarchy % urllib.quote_plus(sscc))
        if response.status_code == 200:
            return CHierarchyInformation(self, response.json())
        self._raiseExceptionFromResponse('getSsccFullHierarchy', response)


    def getSsccFullHierarchyByList(self, ssccs):
        # 8.4.4. Метод для получения информации о полной иерархии вложенности третичной упаковки для нескольких SSCC
        # * — Максимальное количество элементов в списке запрашиваемых SSCC: 10
        MAXCNT = 10
        result = []
        for i in xrange(0, len(ssccs), MAXCNT):
            part = ssccs[i:i+MAXCNT]
            params = urllib.urlencode([('sscc', part)], True)
            # на форуме ЧЗ пишут ( https://честныйзнак.рф/forum/?PAGE_NAME=message&FID=7&TID=239&TITLE_SEO=239-testirovali-priemku-sscc-poluchili-oshibku&MID=2810&tags=&q=sscc&FORUM_ID%5B0%5D=0&DATE_CHANGE=0&order=relevance&s=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8#message2810 )
            # что можно писать api.mdlp.crpt.ru/api/v1/reestr/sscc/full-hierarchy?sscc=046070083659300568,046070083637881287
            # params = urllib.urlencode({'sscc', ','.join(part)})
            response = self._get('getSsccFullHierarchyByList', self.dirSsccFullHierarchyByList + '?' + params)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    result.append(CHierarchyInformation(self, item))
            else:
                self._raiseExceptionFromResponse('getSsccFullHierarchyByList', response)
        return result


    def getPublicProducts(self,
                         start=0,
                         count=100,

                         gtin           = None, # Идентификатор GTIN
                         drugCode       = None, # Внутренний уникальный идентификатор лекарственного препарата в реестре ЕСКЛП
                         tradeName      = None, # Торговое наименование лекарственного препарата
                         regHolder      = None, # Наименование  держателя РУ
                         regNumber      = None, # Номер регистрационного удостоверения
                         begRegDate     = None, # Дата гос.регистрации, начальная дата
                         endRegDate     = None, # Дата гос.регистрации, конечная дата
                         isVed          = None, # Признак наличия в ЖНВЛП
                         inHcl          = None, # Признак, отображающий, относится ли ЛП к списку 7ВЗН
                         fabricatorName = None, # Производитель готовой ЛФ
                        ):
        # 8.5.3. Метод для поиска публичной информации в реестре производимых ЛП
        query = {'start_from': start,
                 'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('gtin',           'gtin',           None),
                                                      ('drugCode',       'drug_code',      None),
                                                      ('tradeName',      'prod_sell_name', None),
                                                      ('regHolder',      'reg_holder',     None),
                                                      ('regNumber',      'reg_id',         None),
                                                      ('begRegDate',     'reg_date_from',  self._dateToStr),
                                                      ('endRegDate',     'reg_date_to',    self._dateToStrUp),
                                                      ('isVed',          'gnvlp',          None),
                                                      ('inHcl',          'vzn_drug',       None),
                                                      ('fabricatorName', 'glf_name',       None),
                                                    )
                                                  ),
                }
        response = self._post('getPublicProducts', self.dirPublicProducts, query)
        if response.status_code == 200:
            data = response.json()
            return ( [ CPublicProductInformation(self, entry)
                       for entry in data.get('entries',[])
                     ],
                     data.get('total')
                   )

            return data
        self._raiseExceptionFromResponse('getPublicProducts', response)


    def getPartners(self,
                    start = 0,
                    count = 100,
                    entityType          = 1,    # Тип участника,
                                                # 1 - резидент РФ
                                                # 2 - представительство иностранного держателя регистрационного удостоверения
                                                # 3 - иностранный держатель регистрационного удостоверения
                                                # 8 - иностранный контрагент
                    sysId               = None, # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП»
                    regionCode          = None, # Код ОКТМО субъекта Российской Федерации
                    federalDistrictCode = None, # Код округа Российской Федерации
                    countryCode         = None, # Код страны
                    name                = None, # Наименование организации
                    inn                 = None, # ИНН
                    kpp                 = None, # КПП
                    ogrn                = None, # ОГРН
                   ):
        # 8.8. Получение информации о субъектах обращения (участниках ИС "Маркировка")
        query = {'start_from': start,
                 'count'     : count,
                 'filter'    : self._prepareFilter( locals(),
                                                    ( ('entityType',          'reg_entity_type',       None),
                                                      ('sysId',               'system_subj_id',        None),
                                                      ('regionCode',          'federal_subject_code',  None),
                                                      ('federalDistrictCode', 'federal_district_code', None),
                                                      ('countryCode',         'country',               None),
                                                      ('name',                'org_name',              None),
                                                      ('inn',                 'inn',                   None),
                                                      ('kpp',                 'kpp',                   None),
                                                      ('ogrn',                'ogrn',                  None),
                                                    )
                                                  ),
                }

        response = self._post('getPartners', self.dirPartners, query)
        if response.status_code == 200:
            data = response.json()
            return [ CForeignCounterparty(self, entry)
                     if 'counterparty_itin' in entry
                     else CRegistrationEntry(self, entry)
                     for entry in data.get('filtered_records', [])
                   ]
        self._raiseExceptionFromResponse('getPartners', response)


    #################################################
    #
    # Подробности реализации

    def _cleanUrlMorphRules(self):
        self._urlMorphRules = []


    def _addUrlMorphRules(self, targetUrl, substUrl):
        target = CUrlComporents(targetUrl)
        if target.path and not target.path.endawith('/'):
            target.path += '/'
        subst  = CUrlComporents(substUrl)
        self._urlMorphRules.append((target, subst))


    def _morphUrl(self, destUrl):
        dest = CUrlComporents(destUrl)
        for (target, subst) in self._urlMorphRules:
            if (    dest.scheme == target.scheme
                and dest.host == target.host
                and dest.port == target.port
                and dest.path.startswith(target.path)
               ):
                dest.scheme = subst.scheme
                dest.host   = subst.host
                dest.port   = subst.port
                return dest.unparse()
        return destUrl


    def _sleepAfterLastCall(self, lastCall, interval):
        if lastCall is None:
            return
        wakeup = lastCall + timedelta(seconds=interval+0.01)
        # просто спать без цикла - не получится,
        # потому что sleep иногда прерывается...
        # пишут, что в python3.6 цикл не нужен
        while True:
            now  = datetime.now()
            duration = wakeup-now
            #seconds = duration.total_seconds()
            # python 2.6 has no timedelta.total_seconds(), and we can not path it
            seconds = duration.days*86400 + duration.seconds + duration.microseconds*1e-6
            if seconds<=0:
                return
            time.sleep(seconds)


    def _post(self, action, urlDir, query):
        logger = logging.getLogger()
        interval = initialInterval = self._mapActionToInterval.get(action, 0.5)
        lastCall = self._mapActionToLastCall.get(action)

        data = json.dumps(query)
        url = self._morphUrl(self.baseUrl) + urlDir
        logger.info(u'mdlp Action:%s post url:%s query=%s', action, url, query)
        attempt = 0
        while True:
            attempt += 1
            self._sleepAfterLastCall(lastCall, interval)
            self._checkToken()
            response = requests.post( url,
                                      data    = data,
                                      headers = { 'Content-Type':  self.contentTypeJson,
                                                  'Authorization': 'token ' + self._token
                                                }
                                    )
            self._mapActionToLastCall[action] = lastCall = datetime.now()
#            print response.status_code, response.text
            logger.info(u'mdlp Action:%s status=%s text=%s', action, response.status_code, anyToUnicode(response.content))
            if response.status_code != 429 or attempt>=10:
                return response
            interval *= 1.5
            rertyAfter = response.headers.get('Retry-After', '').strip()
            if rertyAfter.isdigit():
                recommendedInterval = float(rertyAfter)
                interval = max(interval, recommendedInterval)
                if recommendedInterval>initialInterval:
                    self._mapActionToInterval[action] = recommendedInterval


    def _get(self, action, relUrl=None, absUrl=None):
        logger = logging.getLogger()
        interval = initialInterval = self._mapActionToInterval.get(action, 0.5)
        lastCall = self._mapActionToLastCall.get(action)

        url = self._morphUrl(absUrl) if absUrl else self._morphUrl(self.baseUrl) + relUrl
        logger.info(u'mdlp Action:%s get url:%s', action, url)
        attempt = 0
        while True:
            attempt += 1
            self._sleepAfterLastCall(lastCall, interval)
            self._checkToken()
            response = requests.get( url,
                                     headers = {'Authorization': 'token ' + self._token
                                               }
                                   )
#            print response.status_code, response.text
            self._mapActionToLastCall[action] = lastCall = datetime.now()
            logger.info(u'mdlp Action:%s status=%s text=%s', action, response.status_code, anyToUnicode(response.content))
            if response.status_code != 429 or attempt>=10:
                return response
            interval *= 1.5
            rertyAfter = response.headers.get('Retry-After', '').strip()
            if rertyAfter.isdigit():
                recommendedInterval = float(rertyAfter)
                interval = max(interval, recommendedInterval)
                if recommendedInterval>initialInterval:
                    self._mapActionToInterval[action] = recommendedInterval


    def _getCert(self):
        if self._cert is None:
            self._cert = self._api.findCertInStores(self._api.SNS_OWN_CERTIFICATES, sha1hex=self._certHash)
            if self._cert is None:
                raise Exception('Cert not found')
            self._certProvider = self._cert.provider() # для исключения массового запроса пароля
        return self._cert


    def _auth(self):
        start = datetime.now()
        authCode = self._getAuthCode('SIGNED_CODE', self._clientId, self._clientSecret, self._certHash)
        signature = self._getCert().createDetachedSignature(authCode.encode('latin1'))
        token, lifeTime = self._getTokenAndLifeTime(authCode, signature)
        self._token = token
        self._tokenExpired = start + timedelta(minutes=lifeTime, seconds=-5)


    def _checkToken(self):
        if self._token is None:
            raise Exception('Not authenticated')
        if self._tokenExpired < datetime.now():
            self._auth()


    def _close(self):
        self._certProvider = None
        self._cert = None
        if self._token:
            try:
                if self._tokenExpired >= datetime.now():
                    requests.get( self._morphUrl(self.baseUrl) + self.dirLogout,
                                  headers = { 'Authorization': 'token ' + self._token
                                            }
                                )
            finally:
               self._token = None
               self._tokenExpired = None


    def _raiseExceptionFromResponse(self, action, response):
#        print  response.status_code, response.text
        contentType = response.headers.get('Content-Type', '').split(';',1)[0].strip().lower()
        addDescr = True
        if contentType == 'application/json':
            try:
                text = response.json()['error_description']
                addDescr = False
            except:
                text = response.text
        else:
            text = response.text
        if len(text)>1024:
            text = text[:1024]+'...'
        if addDescr:
            text = u'код http %s, сообщение сервера «%s»' % ( response.status_code, text )
        raise Exception(u'%s: %s' % (action, text))


    def _getAuthCode(self, auth_type, client_id, client_secret, user_id):
        query = {
                    'client_id'     : client_id,
                    'client_secret' : client_secret,
                    'auth_type'     : 'SIGNED_CODE',
                    'user_id'       : user_id,
                }

        response = requests.post( self._morphUrl(self.baseUrl) + self.dirAuth,
                                  data    = json.dumps(query),
                                  headers = { 'Content-Type': self.contentTypeJson,
                                            }
                                )

        if response.status_code == 200:
            return response.json()['code']

        self._raiseExceptionFromResponse('auth', response)


    def _getTokenAndLifeTime(self, auth_code, signature):
        query = {
                     'code'     : auth_code,
                     'signature': base64.b64encode(signature),
                }

        response = requests.post( self._morphUrl(self.baseUrl) + self.dirToken,
                                  data    = json.dumps(query),
                                  headers = { 'Content-Type': self.contentTypeJson,
                                            }
                                )
        if response.status_code == 200:
            tokenInfo = response.json()
            return tokenInfo['token'], tokenInfo['life_time']

        self._raiseExceptionFromResponse('token', response)


    def _getDocumentUrl(self, documentId):
        response = self._get('getDocumentUrl',
                             self.dirDocumentDownload % urllib.quote_plus(documentId)
                            )
        if response.status_code == 200:
            return response.json()['link']
        if response.status_code == 404:
            return None
        self._raiseExceptionFromResponse('getDocumentUrl', response)


    def _getDocumentReceiptUrl(self, documentId):
        response = self._get('getDocumentReceiptUrl',
                             self.dirDocumentReceiptDownload % urllib.quote_plus(documentId)
                            )
        if response.status_code == 200:
            return response.json()['link']
        if response.status_code == 404:
            return None
        self._raiseExceptionFromResponse('getDocumentReceiptUrl', response)


    def _downloadDocument(self, documentUrl):
        response = self._get('downloadDocument', absUrl=documentUrl)
        if response.status_code == 200:
            return response.text

        self._raiseExceptionFromResponse('downloadDocument', response)



    @classmethod
    def _prepareFilter(cls, vars_, params):
        result = {}
        for (varName, filterName, converter) in params:
            val = vars_.get(varName)
            if val is not None:
                result[filterName] = converter(val) if converter else val
        return result


    @classmethod
    def _dateToStr(cls, dateOrDatetime):
        if isinstance(dateOrDatetime, date):
            return dateOrDatetime.strftime('%Y-%m-%dT00:00:00')
        else:
            return dateOrDatetime.strftime('%Y-%m-%dT%H:%M:%S')


    @classmethod
    def _dateToStrUp(cls, dateOrDatetime):
        if isinstance(dateOrDatetime, date):
            return dateOrDatetime.strftime('%Y-%m-%dT23:59:59')
        else:
            return dateOrDatetime.strftime('%Y-%m-%dT%H:%M:%S')


    @classmethod
    def _strToDateTime(cls, s):
        if s is None:
           return None
        if 'T' not in s and ' ' in s:
            s = s.replace(' ','T')
        return isodate.parse_datetime(s)


    @classmethod
    def _strToDate(cls, s):
        if s is None:
           return None
        return isodate.parse_date(s)



###################################################################
#
# Параметр mdlp передаётся для разбора дат и даты-и-времени
# в наследнике можно перекрыть - и получать QDate и QDateTime
#

class COutcomingDocument(object):
    def __init__(self, mdlp, jsonDict):
        self.requestId      = jsonDict['request_id']                           # Уникальный идентификатор запроса
        self.documentId     = jsonDict['document_id']                          # Уникальный идентификатор документа
        self.date           = mdlp._strToDateTime(jsonDict.get('date'))        # Дата получения документа
        self.processedDate  = mdlp._strToDateTime(jsonDict.get('processed_date'))# Дата обработки документа
        self.senderId       = jsonDict['sender']                               # Отправитель документа, SysID или  BranchID
#        self.receiverId     = jsonDict['receiver']
        self.sysId          = jsonDict['sys_id']                               # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП»
        self.docType        = jsonDict['doc_type']                             # Тип документа, Соответствуе т номеру схемы XSD
        self.docStatus      = jsonDict['doc_status']                           # Статус документа
        self.fileUploadType = jsonDict['file_uploadtype']                      # Тип загрузки в систему
        self.version        = jsonDict.get('version')                          # Версия документа
        self.deviceId       = jsonDict.get('device_id')                        # Уникальный идентификатор регистратора событий
        self.skzkmOriginId  = jsonDict.get('skzkm_origin_msg_id')              # Уникальный идентификатор системы сформировавшей сообщение
        self.skzkmReportId  = jsonDict.get('skzkm_report_id')                  # Идентификатор отчета СУЗ
        self.processingDocumentStatus = jsonDict.get('processing_document_status') # Статус обработки документа {PROCESSING, ACCEPTED, PARTIAL, REJECTED, TECH_ERROR}
#        print jsonDict


class CIncomingDocument(object):
    def __init__(self, mdlp, jsonDict):
        self.requestId      = jsonDict['request_id']
        self.documentId     = jsonDict['document_id']
        self.date           = mdlp._strToDateTime(jsonDict['date'])
        self.processedDate  = mdlp._strToDateTime(jsonDict['processed_date'])

        self.senderId       = jsonDict['sender']                               # Отправитель документа, SysID или  BranchID
        self.senderSysId    = jsonDict['sender_sys_id']                        # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП», SysID
        self.receiverId     = jsonDict['receiver']                             # Получатель документа, SysID или  BranchID
        self.sysId          = jsonDict['sys_id']                               # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП», SysID
        self.docType        = jsonDict['doc_type']
        self.docStatus      = jsonDict['doc_status']
        self.fileUploadType = jsonDict['file_uploadtype']
        self.isNew          = jsonDict.get('is_new')                           # Признак, регулирующий возможность получать только новые (непрочитанные) документы
        self.version        = jsonDict.get('version')


class C841HierarchyInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.errorCode = jsonDict.get('error_code')                       # 2 — "Запрашиваемые данные не найдены";
                                                                          # 4 — "Запрашиваемые данные доступны только текущему владельцу или контрагенту по операции".
        self.errorText = jsonDict.get('error_desc')
        self.up   = [C841HierarchySsccInformation(mdlp, item) for item in jsonDict['up']]
        self.down = [C841HierarchySsccInformation(mdlp, item) for item in jsonDict['down']]


class C841HierarchySsccInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.sscc = jsonDict['sscc']                                      # Идентификационный код третичной упаковки
        self.packingDate = mdlp._strToDateTime(jsonDict['release_date'])  # Дата и время совершения операции упаковки
        self.ownerId  = jsonDict['system_subj_id']                        # Идентификатор субъекта обращения, осуществившего операцию упаковки;
                                                                          # по факту возвращается владелец, поэтому я переименовал


class CHierarchyInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.up   = CHierarchySsccInformation(mdlp, jsonDict['up'])
        self.down = CHierarchySsccInformation(mdlp, jsonDict['down'])

    @property
    def sscc(self):
        return self.down.sscc


    @property
    def sgtins(self):
        return self.down.sgtins



class CHierarchySsccInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.sscc         = jsonDict['sscc']                              # Идентификационный код третичной упаковки             String           SSCC               1
        self.packingDate  = mdlp._strToDateTime(jsonDict['packing_date']) # Дата и время совершения операции упаковки            String           DateTime           1
        self.ownerId      = jsonDict['owner_id']                          # Идентификатор текущего владельца упаковки            String           SysID или BranchID 1
        self.ownerName    = jsonDict['owner_organization_name']           # Наименование организации текущего владельца упаковки String                              1
        self.children     = []
        if 'childs' in jsonDict:
            for child in jsonDict['childs']:                                 # Список вложенных элементов в упаковку
                if 'sgtin' in child:
                    self.children.append( CHierarchySgtinInformation(mdlp, child) ) # В случае, если в упаковку вложен КИЗ, то в списке он будет элементом типа "HierarchySgtinInfo".
                else:
                    self.children.append( CHierarchySsccInformation(mdlp, child) )  # В случае, если в упаковку вложена другая упаковка, то в списке она будет элементом типа "HierarchySsccInfo"

    @property
    def sgtins(self):
        result = []
        self._getSgtins(result)
        return result


    def _getSgtins(self, sgtins):
        for child in self.children:
            if isinstance(child, CHierarchySsccInformation):
                child._getSgtins(sgtins)
            elif isinstance(child, CHierarchySgtinInformation):
                sgtins.append(child)



class CHierarchySgtinInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.sgtin  = jsonDict['sgtin']                                        # Идентификатор SGTIN
        self.sscc   = jsonDict['sscc']                                         # Номер транспортной упаковки
        self.gtin   = jsonDict['gtin']                                         # Идентификатор товара в GS1
        self.status = jsonDict.get('status') or jsonDict.get('internal_state') # Статус SGTIN: См. раздел 4.43, Список возможн ых статусов КИЗ
        self.batch  = jsonDict['batch']                                        # Номер производственной серии
        self.expirationDate = mdlp._strToDateTime(jsonDict['expiration_date']) # Срок годности препарата
        if 'pause_decision_info' in jsonDict:
            self.haltInfo = CSgtinHaltInformation(mdlp, jsonDict['pause_decision_info']) # Информация о решении о приостановке (HierarchyPauseDecisionInfo)
        else:
            self.haltInfo = None


class CSgtinHaltInformation(object):
    def __init__(self, mdlp, jsonDict):
        self.id       = jsonDict.get('id')                                      # Идентификатор решения
        self.number   = jsonDict.get('number')                                  # Номер решения
        self.date     = mdlp._strToDate(jsonDict.get('date'))                   # Дата решения
        self.haltDate = mdlp._strToDate(jsonDict.get('halt_date'))              # Дата вступления в силу


class CGetSsccSgtinsResult(object):
    def __init__(self, mdlp, jsonDict):
        self.entries   = [ CSgtinInformation(mdlp, entry)
                           for entry in jsonDict.get('entries', [])
                         ]
        self.total     = jsonDict.get('total')
        self.errorCode = jsonDict.get('error_code') # 2 or 4
        self.errorText = jsonDict.get('error_desc')


class CSgtinInformation(object):
    # 4.34. Формат объекта SGTIN
    # 4.35. Формат объекта SgtinExtended
    # я не вижу смысла различать эти объекты, тем более что все свойства SgtinExtended опциональны,
    # oms_order_id входит в оба,
    # в некоторых местах не указано что мы получаем...

    def __init__(self, mdlp, jsonDict):
        strToDateTime = mdlp._strToDateTime

        self.id             = jsonDict['id']                                         # Уникальный идентификатор
        self.sgtin          = jsonDict['sgtin']                                      # SGTIN (КИЗ)
        self.gtin           = jsonDict['gtin']                                       # GTIN

        self.fullProductName= jsonDict.get('full_prod_name')                         # Полное наименование товара
        self.productName    = jsonDict.get('prod_name')                              # Торговая марка (бренд)
        self.productINName  = jsonDict.get('prod_norm_name')                         # МНН или что-то вроде
        self.tradeName      = jsonDict.get('sell_name')                              # Торговое наименование
        self.descr          = jsonDict.get('pack1_desc')                             # Полное наименование товара (на самом деле - описание первичной или вторичной упаковки)
        self.dosageForm     = jsonDict.get('prod_form_name')                         # Лекарственная форма
        self.normDosageForm = jsonDict.get('prod_form_norm_name')                    # Лекарственная форма, нормализованное значение
        self.dosage         = jsonDict.get('prod_d_name')                            # Количество единиц измерения дозировки лекарственного препарата (строковое представление) (???)
        self.normDosage     = jsonDict.get('prod_d_norm_name')                       # Количество единиц измерения дозировки лекарственного препарата (строковое представление), нормализованное значение (???)
        self.drugCode       = jsonDict.get('drug_code')                              # Внутренний уникальный идентификатор лекарственного препарата в реестре ЕСКЛП

#        self.regHolder      = jsonDict.get('reg_holder')                             # Держатель рег.удостоверения
        self.isVed          = jsonDict.get('gnvlp')                                  # Признак наличия в ЖНВЛП (Vital & Essential Drugs)
        self.inHcl          = jsonDict.get('vzn_drug')                               # Признак, отображающий относится ли ЛП к списку 7 ВЗН
        self.batch          = jsonDict['batch']                                      # Номер производственной серии
        self.releaseDate    = strToDateTime(jsonDict.get('release_date'))            # Дата изготовления
        self.expirationDate = strToDateTime(jsonDict.get('expiration_date'))         # Срок годности

        self.emissionType   = jsonDict.get('emission_type')                          # Тип эмиссии, См. раздел 4.44. Типы эмиссии
        self.emissionDate   = strToDateTime(jsonDict.get('emission_operation_date')) # Дата регистрации

        self.packagerInn    = jsonDict.get('packing_inn')                            # ИНН/ITIN упаковщика во вторичную/третичную упаковку
        self.packagerName   = jsonDict.get('packing_name')                           # Наименование упаковщика во вторичную/третичную упаковку
        self.packagerId     = jsonDict.get('packing_id')                             # Идентификатор упаковщика во вторичную/третичную упаковку (SysID или BranchID)

        self.qaInn          = jsonDict.get('control_inn')                            # ИНН/ITIN производителя стадии выпускающий контроль качества
        self.qaName         = jsonDict.get('control_name')                           # Наименование производителя стадии выпускающий контроль качества
        self.qaId           = jsonDict.get('control_id')                             # Идентификатор производителя стадии выпускающий контроль качества (SysID или BranchID)

        self.sscc           = jsonDict.get('pack3_id')                               # Идентификационный код третичной упаковки

        self.status         = jsonDict['status']                                     # Статус, См. раздел 4.43. Список возможных статусов КИЗ
        self.statusDate     = strToDateTime(jsonDict['status_date'])                 # Дата последней смены статуса

        self.customsPostId  = jsonDict.get('customs_point_id')                       # Идентификатор места нахождения товара в ЗТК
        self.omsOrderId     = jsonDict.get('oms_order_id')                           # Идентификатор заказа системы управления заказами (СУЗ)
        self.fundingSource  = jsonDict.get('source_type')                            # Источник финансирования: 1 — собственные средства, 2 — средства федерального бюджета 3 — средства регионального бюджета
        self.ownerInn       = jsonDict['inn']                                        # ИНН владельца
        self.ownerName      = jsonDict['owner']                                      # Наименование владельца
        self.ownerRegionCode= jsonDict.get('federal_subject_code')                   # Код субъекта РФ (предположим, что владельца)
        self.ownerRegionName= jsonDict.get('federal_subject_name')                   # Местонахождение ЛП (предположим, что определяется по владельцу)
        self.ownerId        = jsonDict['sys_id']                                     # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП» (предположим, что владельца)

        bi = jsonDict.get('billing_info')
        if bi:
            self.billingInfo = CSgtinBillingInformation(mdlp, bi)                    # Информация о биллинге
        else:
            self.billingInfo = None                                                  # Информация о биллинге
        self.billingState   = jsonDict.get('billing_state')                          # Состояние оплаты SGTIN: 0 — успешно оплачен, 1 — выбран для перемещения в очередь на оплату, 2 — помещается в очередь на оплату, 3 — помещён в очередь на оплату, 4 — не оплачен в установленные сроки

        haltId      = jsonDict.get('halt_id')                                        # Идентификатор решения о приостановке
        haltDocNum  = jsonDict.get('halt_doc_num')                                   # Номер решения о приостановке
        haltDocDate = jsonDict.get('halt_doc_date')                                  # Дата решения о приостановке
        haltDate    = jsonDict.get('halt_date')                                      # Дата вступления в силу решения о приостановке
        if haltId or haltDocDate or haltDocNum or haltDate:
            self.haltInfo = CSgtinHaltInformation(mdlp,
                                                  { 'id'          : haltId,
                                                    'number'      : haltDocNum,
                                                    'date'        : haltDocDate,
                                                    'halt_date'   : haltDate
                                                  }
                                                 )
        else:
            self.haltInfo = None

        self.lastOperationDate = strToDateTime(jsonDict.get('last_tracing_op_date')) # Дата последней операции


class CSgtinBillingInformation(object):
    # 4.36. Формат объекта SgtinBillingInformation
    def __init__(self, mdlp, jsonDict):
        self.isPrepayment = jsonDict['is_prepaid']                        # Признак предоплаты
        self.isFree       = jsonDict['free_code']                         # Признак бесплатного кода (код - бесплатно? а таблетки - за деньги? ну ок)
        self.isPaid       = jsonDict['is_paid']                           # Статус оплаты
        self.containHcl   = jsonDict['contains_vzn']                      # Признак вхождения в список высокозатратных нозологий (high-cost list)
        self.payments     = [ CSgtinPaymentInformation(mdlp, paymentDict) # Список информации о платежах
                              for paymentDict in jsonDict.get('payments', [])
                            ]

class CSgtinPaymentInformation(object):
    # 4.37. Формат объекта SgtinPaymentInformation
    def __init__(self, mdlp, jsonDict):
        if 'created_date' in jsonDict:
            self.creationDate = mdlp._strToDateTime(jsonDict['created_date']) # Дата создания платежа
        else:
            self.creationDate = None
        if 'payment_date' in jsonDict:
            self.paymentDate = mdlp._strToDateTime(jsonDict['payment_date'])  # Дата оплаты платежа
        else:
            self.paymentDate = None
        self.tariff = jsonDict.get('tariff')                                      # Тариф оплаты (WFT? тариф - в прейскуранте, оплата - по счёту...)


class CFailedSgtinInformation(object):
    def __init__(self, mdlp, jsonDictOrSgtin):
        if isinstance(jsonDictOrSgtin, dict):
            jsonDict = jsonDictOrSgtin
            self.sgtin     = jsonDict['sgtin']
            self.errorCode = jsonDict['error_code']
            self.errorText = jsonDict['error_desc']
        else:
            self.sgtin     = jsonDictOrSgtin
            self.errorCode = 2
            self.errorText = u'Запрашиваемые данные не найдены'


class CPublicSgtinInformation(object):
    # Объект PublicSgtin:
    def __init__(self, mdlp, jsonDict):
        strToDateTime = mdlp._strToDateTime
        self.sgtin          = jsonDict['sgtin'] # SGTIN (КИЗ)
        self.gtin           = self.sgtin[:14]
        self.drugCode       = jsonDict.get('drug_code')                              # Внутренний уникальный идентификатор лекарственного препарата в реестре ЕСКЛП
        self.batch          = jsonDict['batch']                                      # Номер производственной серии
        self.expirationDate = strToDateTime(jsonDict.get('expiration_date'))         # Срок годности
        self.productName    = jsonDict.get('prod_name')                              # Торговая марка (бренд)
        self.tradeName      = jsonDict.get('sell_name')                              # Торговое наименование
        self.dosage         = jsonDict.get('prod_d_name')                            # Количество единиц измерения дозировки лекарственного препарата (???)
        self.dosageForm     = jsonDict.get('prod_form_name')                         # Лекарственная форма

        self.regHolder      = jsonDict.get('reg_holder')                             # Держатель рег.удостоверения
        self.regNumber      = jsonDict.get('reg_number')                             # Рег.номер
        self.regDate        = strToDateTime(jsonDict.get('reg_date'))                # Дата гос. Регистрации


class CPublicProductInformation(object):
    # Формат объекта MedProductPublic:
    def __init__(self, mdlp, jsonDict):
        strToDateTime = mdlp._strToDateTime
        self.gtin           = jsonDict['gtin']                                       # Идентификатор GTIN
        self.drugCode       = jsonDict.get('drug_code')                              # Внутренний уникальный идентификатор лекарственного препарата в реестре ЕСКЛП
        self.drugCodeVersion= jsonDict.get('drug_code_version')                      # Версия внутреннего идентификатора ЛП в реестре ЕСКЛП: 1 — устаревшие данные ЕСКЛП, 2 — актуальные данные ЕСКЛП

        self.regNumber      = jsonDict.get('reg_number')                             # Номер рег. Удостоверения
        self.regDate        = strToDateTime(jsonDict.get('reg_date'))                # Дата гос. Регистрации
        self.tradeName      = jsonDict.get('prod_sell_name')                         # Торговое наименование лекарственного препарата
        self.fullProductName= jsonDict.get('prod_desc')                              # Наименование товара на этикетке
        self.productINName  = jsonDict.get('prod_name')                              # Международное непатентованное наименование, или группировочное, или химическое наименование, стандартизованное значение
        self.normProductINName = jsonDict.get('prod_norm_name')                      # Международное непатентованное наименование, или группировочное, или химическое наименование, нормализованное значение
        self.completeness   = jsonDict.get('completeness')                           # Комплектность
        self.regNumber      = jsonDict.get('reg_number')                             # Номер рег. Удостоверения
        self.regDate        = strToDateTime(jsonDict.get('reg_date'))                # Дата гос. Регистрации
        self.regHolder      = jsonDict.get('reg_holder')                             # Наименование держателя РУ
#        self.regStatus      = jsonDict.get('reg_status')                             #  Статус рег.  Удостоверения (устарело)
        self.dosageForm     = jsonDict.get('prod_form_name')                         # Лекарственная форма, стандартизованное значение (строковое представление)
        self.normDosageForm = jsonDict.get('prod_form_norm_name')                    # Лекарственная форма, нормализованное значение (строковое представление)
        self.dosage         = jsonDict.get('prod_d_name')                            # Количество единиц измерения дозировки лекарственного препарата, стандартизованное значение (строковое представление)
        self.normDosage     = jsonDict.get('prod_d_norm_name')                       # Количество единиц измерения дозировки лекарственного препарата, нормализованное значение (строковое представление)
        self.primaryPerSecondary      = jsonDict.get('prod_pack_1_2')                # Кол-во первичной в потребительской упаковке
        self.primaryPackage = jsonDict.get('prod_pack_1_name')                       # Первичная упаковка (строковое представление)
        self.primaryPackageCapacity  = jsonDict.get('prod_pack_1_ed')                # Количество массы/объема в первичной упаковке
        self.primaryPackageUnit      = jsonDict.get('prod_pack1_ed_name')            # Количество (мера, ед. измерения) массы/объема в первичной упаковке (на самом деле - ед.изм)

        self.isVed          = jsonDict.get('gnvlp')                                  # Признак наличия в ЖНВЛП (Vital & Essential Drugs)
        self.inHcl          = jsonDict.get('vzn_drug')                               # Признак, отображающий относится ли ЛП к списку 7 ВЗН

        self.fabricatorName = jsonDict.get('glf_name')                               # Производитель готовой ЛФ
        self.fabricatorCountry = jsonDict.get('glf_country')                         # Страна регистрации производителя готовой ЛФ
        self.costLimit      = jsonDict.get('cost_limit')                             # Предельная зарегистрированная цена



class CForeignCounterparty(object):
    # Формат объекта ForeignCounterparty
    def __init__(self, mdlp, jsonDict):
        self.sysId      = jsonDict['system_subj_id']                              # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП»
        self.itin       = jsonDict['counterparty_itin']                           # ИТИН
        self.name       = jsonDict['counterparty_name']                           # Наименование субъекта обращения
        self.address    = CForeignAddress(mdlp, jsonDict['counterparty_address']) # Адрес субъекта обращения
        # self.regDate    = mdlp._strToDateTime(jsonDict['op_date']['$date'])       # Дата регистрации
        # self.id         = jsonDict.get('id')                                      # Уникальный идентификатор
        self.entityType = 8
        self.branches   = []
        self.warehouses = []
#        self.inn        = None
#        self.kpp        = None


class CRegistrationEntry(object):
    # Формат объекта RegistrationEntry
    def __init__(self, mdlp, jsonDict):
        self.sysId      = jsonDict['system_subj_id']                              # Идентификатор субъекта обращения в «ИС "Маркировка". МДЛП»
        self.branches   = [ CResolvedFiasAddress(mdlp, item)                      # Список мест осуществления деятельности
                            for item in jsonDict.get('branches', [])
                          ]
        self.warehouses = [ CResolvedFiasAddress(mdlp, item)                      # Список мест ответственного хранения
                            for item in jsonDict.get('safe_warehouses', [])
                          ]
        self.inn        = jsonDict.get('inn')                                     # ИНН субъекта обращения в «ИС "Маркировка ". МДЛП»
        self.kpp        = jsonDict.get('KPP') or jsonDict.get('kpp')              # КПП
        self.name       = jsonDict['ORG_NAME']                                    # Наименование субъекта обращения в «ИС "Маркировка ". МДЛП»
        self.ogrn       = jsonDict.get('OGRN') or jsonDict.get('ogrn')            # ОГРН
        # FIRST_NAME                  | Имя руководителя организации                               | String          |                     | 1              |
        # MIDDLE_NAME                 | Отчество руководителя организации                          | String          |                     | 1              |
        # LAST_NAME                   | Фамилия руководителя организации                           | String          |                     | 1              |
        self.entityType = jsonDict['entity_type']
        # self.regAppDate = mdlp._strToDateTime(jsonDict['op_date']['$date'])       # Дата заявки на регистрацию
        # self.regDate    = mdlp._strToDateTime(jsonDict['op_exec_date'])           # Дата фактической регистрации в системе
        self.countryCode= jsonDict.get('country_code')                            # Код страны
        self.regionCode = jsonDict.get('federal_subject_code')                    # Код субъекта РФ
        self.itin       = jsonDict.get('itin')                                    # ИТИН
        address = jsonDict.get('org_address')
        self.address   = CForeignAddress(mdlp, address) if address else None      # Адрес организации
        # по факту ещё бывают chiefs, но нам пока не интересно.


class CAddress(object):
    # 4.28. Формат объекта Address
    def __init__(self, mdlp, jsonDict):
        self.aoguid    = jsonDict.get('aoguid')                                          # Уникальный идентификатор адресного объекта (ФИАС)
        self.houseguid = jsonDict.get('houseguid')                                       # Адрес установки (код ФИАС)
        self.address   = jsonDict.get('address_description')                             # Текстовый  адрес объекта


class CForeignAddress(object):
    # 4.29. Формат объекта ForeignAddress
    def __init__(self, mdlp, jsonDict):
        self.city        = jsonDict.get('city')                                          # Город
        self.countryCode = jsonDict.get('country_code')                                  # Код страны
        self.postalCode  = jsonDict.get('postal_code')                                   # Почтовый индекс
        self.region      = jsonDict.get('region')                                        # Регион
        self.locality    = jsonDict.get('locality')                                      # Населённый пункт
        self.street      = jsonDict.get('street')                                        # Улица
        self.house       = jsonDict.get('house')                                         # Дом
        self.corpus      = jsonDict.get('corpus')                                        # Корпус
        self.litera      = jsonDict.get('litera')                                        # Литера
        self.room        = jsonDict.get('room')                                          # № помещения (квартиры)


class CResolvedFiasAddress(object):
    # Формат объекта ResolvedFiasAddress:
    def __init__(self, mdlp, jsonDict):
        self.id   = jsonDict['id']                                                       # Идентификатор (branchId?)
        fias = jsonDict['address_fias']
        self.aoguid    = fias.get('aoguid')                                              # Уникальный идентификатор адресного объекта (ФИАС)
        self.houseguid = fias.get('houseguid')                                           # Адрес установки (код ФИАС)
        self.room      = fias.get('room')                                                # Комната
        resolved = jsonDict['address_resolved']
        self.address   = resolved.get('address') if resolved.get('code',0) == 0 else ''  # Текстовый  адрес объекта
        self.status    = jsonDict.get('status')                                          # Статус: 0 — не действует, 1 — действует, 2 — в процессе приостановления

    def asString(self):
        return self.address or self.id


class CBranchInformation(object):
    # Безымянный объект :)
    def __init__(self, mdlp, jsonDict):
        self.id = jsonDict['branch_id']
        self.address = CAddress(mdlp, jsonDict['address'])
        self.canWithdrawViaDocument = jsonDict.get('is_withdrawal_via_document_allowed')
        self.hasMedLicense          = jsonDict.get('has_med_license')
        self.hasNarcoticLicense     = jsonDict.get('has_narcotic_license')
        self.hasPharmLicense        = jsonDict.get('has_pharm_license')
        self.hasProdLicense         = jsonDict.get('has_prod_license')
