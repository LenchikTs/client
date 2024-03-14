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
## Интерфейсный объект для свсзи с регисиратором выбытия МДЛП
##
#############################################################################

import base64
#import json
#import time
#import logging
import urllib
import urlparse
#import uuid
import warnings
from datetime import datetime as DateTime

import isodate

import requests

#from library.Utils import anyToUnicode


class CRetReg(object):
    defaultUser     = u'user1'
    defaultPassword = u'Pas$w0rd'

    contentTypeJson = 'application/json;charset=UTF-8'

    deviceInfoPath      = '/v1/deviceInfo'
    requestStatusRvPath = '/v1/state'
    queueUpPath         = '/v1/requests'
    requestStatusPath   = '/v1/requests/%s'
    deleteRequestPath   = '/v1/requests/%s'

    def __init__(self, url, user, password, deviceId=None):
        p = urlparse.urlparse(url)
        self._scheme, self._netloc = p.scheme, p.netloc
        self._queryDict = dict(urlparse.parse_qsl(p.query))
        self._auth      = (user.encode('utf-8'), password.encode('utf-8'))
        self._deviceId  = deviceId

    #################################################
    #
    # Интерфейсные методы

    def test(self):
        try:
            resp = self._get(self.requestStatusRvPath)
            if resp.status_code == 200:
                j = resp.json()
                # {u'lifePhase': u'registered', u'expirationDate': u'2022-11-07T10:03:58Z', u'processState': u'waiting', u'logState': u'full'}
                lifePhase = j.get('lifePhase')
                try:
                    expirationDate = isodate.parse_datetime(j.get('expirationDate'))
                    expirationDate = expirationDate.astimezone(isodate.LOCAL)
                    expirationDate = expirationDate.strftime('%x %X')
                except:
                    expirationDate = u'неизвестен'
                if lifePhase == 'registered':
                    return True, u'Зарегистрирован, срок регистрации ' + expirationDate
                elif lifePhase == 'notRegistered':
                    return False, u'Не зарегистрирован, учебный режим'
                elif lifePhase == 'onRegistration':
                    return False, u'В процессе регистрации'
                elif lifePhase == 'expired':
                    return False, u'Истёк срок регистрации'
                else:
                    return False, u'Ответ не распознан'
            elif resp.status_code == 401:
                return False, u'Неверное имя пользователя или пароль'
            else:
                return False, u'Произошла ошибка, код %s' % resp.status_code
        except requests.exceptions.ConnectTimeout:
            return False, u'Время соединения вышло'
        except requests.exceptions.ConnectionError:
            return False, u'В соединении отказано'


    def deviceInfo(self):
        resp = self._get(self.deviceInfoPath)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
#        print 'status ', resp.status_code
#        print 'content', resp.content
#        print 'headers', resp.headers



    def queueUp(self, requestId, doc):
        resp = self._post(self.queueUpPath,
                          {'rvRequestId': requestId,
                           'request'    : doc.json(),
                          }
                         )
        print 'status ', resp.status_code
        print 'content', resp.content
        print 'headers', resp.headers


    def requestStatus(self, requestId):
        resp = self._get(self.requestStatusPath % requestId)
        print 'status ', resp.status_code
        print 'content', resp.content
        print 'headers', resp.headers


    def deleteRequest(self, requestId):
        resp = self._delete(self.deleteRequestPath % requestId)
        print 'status ', resp.status_code
        print 'content', resp.content
        print 'headers', resp.headers


    #################################################
    #
    # Подробности реализации

    def _prepareUrl(self, path, queryDict=None):
        qd = {}
        if self._queryDict:
            qd.update(self._queryDict)
        if queryDict:
            qd.update(queryDict)
        if self._deviceId:
            qd['deviceId'] = self._deviceId
        if qd:
            query = urllib.urlencode(qd)
        else:
            query = ''

        return urlparse.urlunparse( (self._scheme, self._netloc, path, '', query, '') )


    def _get(self, path, queryDict=None):
        url = self._prepareUrl(path, queryDict)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            r = requests.get(url, auth=self._auth, verify=False, timeout=(3, 60))
            return r


    def _post(self, path, jsonDict):
        url = self._prepareUrl(path)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            r = requests.post(url, json=jsonDict, auth=self._auth, verify=False, timeout=(3, 60))
            return r


    def _delete(self, path):
        url = self._prepareUrl(path)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            r = requests.delete(url, auth=self._auth, verify=False, timeout=(3, 60))
            return r


class CRegisterMarksByRequisites(object):
    def __init__(self, **kwargs):
        self.type_ = kwargs.get('type_')
        self.code  = kwargs.get('code')
        self.codeName = kwargs.get('codeName')
        self.date     = kwargs.get('date')
        self.number   = kwargs.get('number')
        self.marks    = kwargs.get('marks',  [])


    def json(self):
        assert self.type_ in (0, 1)
        assert isinstance(self.code, basestring) and self.code.isdigit()
        assert isinstance(self.codeName, unicode) and self.codeName
        assert isinstance(self.date, DateTime)
        assert isinstance(self.number, unicode) and self.number

        date = self.date.replace(tzinfo=isodate.LOCAL)
        date = date.astimezone(isodate.UTC)

        documentOut = { 'type'    : self.type_,
                        'code'    : self.code,
                        'codeName': self.codeName,
                        'date'    : isodate.datetime_isoformat(date),
                        'number'  : self.number,
                      }
        marks = {}
        key   = 0
        for mark in self.marks:
            assert isinstance(mark, basestring)
            code = base64.b64encode(mark.encode('utf-8'))
            key += 1
            marks[key] = {'mark': code
                         }

        return { 'type': 'registerMarksByRequisites',
                 'documentOut' : documentOut,
                 'marks'       : marks
               }




if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    if 0:
        for url, user, password in [
                                     ('http://192.168.1.161',  'userX', 'Password'),
                                     ('http://192.168.1.161:8080',  'userX', 'Password'),
                                     ('https://192.168.1.161',  'userX', 'Password'),
                                     ('https://192.168.1.161:8080',  'userX', 'Password'),
                                     ('https://192.168.1.161:8080',  'user1', 'Password'),
                                     ('https://192.168.1.161:8080',  'user1', '123456'),
                                     ('https://192.168.1.161:8080',  u'проверка', u'связи'),
                                     ('https://192.168.1.161:8080',  'user1', 'Pas$w0rd'),
                                   ]:
            retReg = CRetReg(url, user, password)
            print url, user, password,
            t = retReg.test()
            print t[0], t[1]

    if 0:
        retReg = CRetReg('https://192.168.1.161:8080', 'user1', 'Pas$w0rd')
        deviceInfo = retReg.deviceInfo()

    requestId = '447b0c43-8a11-4868-87ec-b48c2c1c7b15'
    if 1:
#        requestId = str(uuid.uuid4())
        doc = CRegisterMarksByRequisites(type_    = 0,
                                         code     = '0504204',
                                         codeName = u'Требование накладная',
                                         date     = DateTime.now(),
                                         number   = u'666',
                                         marks    = [
#                                                      u'04601808014105M8zG9De6dwuP6',
#                                                      u'04601808014112JACvelBcivPIQ',

#                                                      u'010460180801410521M8zG9De6dwuP6',
#                                                      u'010460180801411221JACvelBcivPIQ',

                                                       u'010460180801410521M8zG9De6dwuP6\x1d91FAKE\x1d92TU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU0=',
                                                       u'010460180801411221JACvelBcivPIQ\x1d91FAKE\x1d92TU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU0=',

#                                                       u'010460180801410521M8zG9De6dwuP6\x1d91EE06\x1d92hv3qwjW5HxMroGCWxfsIIEmFgwYBQRzkGOqEVWyMYmw=',
#                                                       u'010460180801411221JACvelBcivPIQ\x1d91EE06\x1d92nvsmLvBs9kTTjHUNfufx4/KffPZPxdyClGDzc9msfQA='
                                                    ]
                                        )
        print requestId
        print doc.json()

        retReg = CRetReg('https://192.168.1.161:8080', 'user1', 'Pas$w0rd')
        x = retReg.queueUp(requestId, doc)

    if 1:
#        requestId = '447b0c43-8a11-4868-87ec-b48c2c1c7b15'
        retReg = CRetReg('https://192.168.1.161:8080', 'user1', 'Pas$w0rd')
        x = retReg.requestStatus(requestId)

    if 0:
#        requestId = '447b0c43-8a11-4868-87ec-b48c2c1c7b15'
        requestId = 'e537fcbb-24fc-49c2-a21c-039035dffc8f'
        retReg = CRetReg('https://192.168.1.161:8080', 'user1', 'Pas$w0rd')
        x = retReg.deleteRequest(requestId)



# u'010460180801410521M8zG9De6dwuP6\x1d91EE06\x1d92hv3qwjW5HxMroGCWxfsIIEmFgwYBQRzkGOqEVWyMYmw='
# u'010460180801411221JACvelBcivPIQ\x1d91EE06\x1d92nvsmLvBs9kTTjHUNfufx4/KffPZPxdyClGDzc9msfQA='
