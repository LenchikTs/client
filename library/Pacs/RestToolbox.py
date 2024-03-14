# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import urllib
import urllib2
import base64

import json

from PyQt4 import QtGui
from library.Utils import forceString

def checkPacsConnection(addr, login = None, password = None):
    url = 'http://%s/statistics'%addr
    request = urllib2.Request(url)
    if login and password:
        base64string = base64.encodestring('%s:%s' % (login, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
    try:
        answer = _request(request)
        return True if 'CountInstances' in answer else False
    except:
        return False


def _decodeJson(s):
    try:
        return json.loads(s)
    except:
        return s


def _setupCredentials(request):
    login = forceString(QtGui.qApp.preferences.appPrefs.get('pacsLogin', None))
    passwd = forceString(QtGui.qApp.preferences.appPrefs.get('pacsPassword', None))
    if login:
        base64string = base64.encodestring('%s:%s' % (login, passwd)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)


def getRequest(baseUrl, data = {}, interpretAsJson = True):
    d = ''
    if len(data.keys()) > 0:
        d = '?' + urllib.urlencode(data)

    req = urllib2.Request(baseUrl + d)
    _setupCredentials(req)
    return _request(req)


def _putOrPostRequest(method, url, data, contentType):
    if isinstance(data, basestring):
        body = data
        if contentType:
            headers = { 'content-type' : contentType }
        else:
            headers = { 'content-type' : 'text/plain' }
    else:
        body = json.dumps(data)
        headers = { 'content-type' : 'application/json',  'content-length': len(body) }


    req = urllib2.Request(url, body, headers)
    _setupCredentials(req)
    req.get_method = lambda: method
    return _request(req)


def delete(url):
    req = urllib2.Request(url)
    _setupCredentials(req)
    req.get_method = lambda: 'DELETE'
    return _request(req)


def putRequest(url, data = {}, contentType = ''):
    return _putOrPostRequest('PUT', url, data, contentType)


def postRequest(url, data = {}, contentType = ''):
    return _putOrPostRequest('POST', url, data, contentType)


def _request(req):
    try:
        proxy = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        resp = urllib2.urlopen(req, timeout=2)
        content = resp.read()
        return _decodeJson(content)
    except urllib2.HTTPError as e:
        if e.code == 401:
            msg = u'Необходима аутентификация!\nУкажите авторизационные данные в настройках соединения с pacs сервером'
        else:
            msg = e.msg
        QtGui.QMessageBox.critical(None,
                    u'Ошибка',
                    msg,
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)
#    except urllib2.URLError as e:
#        import socket
#        import errno
#        if type(e.reason) == socket.error:
#            if e.reason.errno != errno.ECONNREFUSED:
#                msg = u'При попытке установить соединение с сервером заданий, возникла ошибка номер %i'%e.reason.errno
#            else:
#                msg = u'При попытке установить соединение с сервером заданий в соединении было отказано'
#        elif type(e.reason) == socket.timeout:
#            msg = u'Сервер хранения изображений не отвечает'
#        else:
#            msg = forceString(e.reason)
#        QtGui.QMessageBox.critical(None,
#                    u'Ошибка связи',
#                    msg,
#                    QtGui.QMessageBox.Ok,
#                    QtGui.QMessageBox.Ok)

    return {}
