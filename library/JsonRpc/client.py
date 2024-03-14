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


import json
import socket
import urllib2
from threading import Thread
from library.Utils import anyToUnicode, exceptionToUnicode


class JsonRpc:
    PARSE_ERROR       = -32700
    INVALID_REQUEST   = -32600
    METOD_NOT_FOUND   = -32601
    INVALID_PARAMS    = -32602
    INTERNAL_ERROR    = -32603


class EJsonRpcBaseException(Exception):
    def __init__(self, code, message, data=None):
        Exception.__init__(self, message)
        self.code = code
        self.data = data


class EJsonRpcParseError(EJsonRpcBaseException):
    def __init__(self, message, data=None):
        EJsonRpcBaseException.__init__(self, JsonRpc.PARSE_ERROR, message, data)


class EJsonRpcInvalidRequest(EJsonRpcBaseException):
    def __init__(self, message, data=None):
        EJsonRpcBaseException.__init__(self, JsonRpc.INVALID_REQUEST, message, data)


class EJsonRpcMethodNotFound(EJsonRpcBaseException):
    def __init__(self, message, data=None):
        EJsonRpcBaseException.__init__(self, JsonRpc.METOD_NOT_FOUND, message, data)


class EJsonRpcInvalidParams(EJsonRpcBaseException):
    def __init__(self, message, data=None):
        EJsonRpcBaseException.__init__(self, JsonRpc.INVALID_PARAMS, message, data)


class EJsonRpcInternamError(EJsonRpcBaseException):
    def __init__(self, message, data=None):
        EJsonRpcBaseException.__init__(self, JsonRpc.INTERNAL_ERROR, message, data)


def exceptionFactory(code, message, data=None):
    mapCodeToClass = { JsonRpc.PARSE_ERROR:      EJsonRpcParseError,
                       JsonRpc.INVALID_REQUEST:  EJsonRpcInvalidRequest,
                       JsonRpc.METOD_NOT_FOUND:  EJsonRpcMethodNotFound,
                       JsonRpc.INVALID_PARAMS:   EJsonRpcInvalidParams,
                       JsonRpc.INTERNAL_ERROR:   EJsonRpcInternamError,
                     }
    if code in mapCodeToClass:
        return mapCodeToClass[code](message, data)
    return EJsonRpcBaseException(code, message, data)


# urllib2.HTTPRedirectHandler теряет data и Content-type
class CSimpleRedirector(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        result = urllib2.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, hdrs, newurl)
        if result is not None and req.has_data() and not result.has_data():
            result.add_header('Content-type', req.get_header('Content-type'))
            result.add_data(req.get_data())
        return result


class CLoaderThread(Thread):

    connectionError = u'Ошибка соединения с сервером'

    def __init__(self, opener, request):
        Thread.__init__(self)
        self.daemon = True
        self.opener = opener
        self.request = request
        self.reader = None
        self.result = None
        self.message = None


    def run(self):
        try:
            self.reader = self.opener.open(self.request, timeout=30)
        except urllib2.HTTPError, e:
            try:
                self.message = u'%s (HTTP %s: %s %s)' % ( self.connectionError, e.code, e.url, anyToUnicode(e.reason) )
            except:
                pass
        except urllib2.URLError, e:
            try:
                if isinstance(e.reason, socket.error):
                    if e.reason.errno:
                        self.message = u'%s (errno=%s) %s)' % (self.connectionError, e.reason.errno, anyToUnicode(e.reason.strerror))
                    else:
                        self.message = u'%s (%s)' % (self.connectionError, exceptionToUnicode(e.reason))
                else:
                    self.message = u'%s (%s)' % (self.connectionError, exceptionToUnicode(e))
            except:
                pass
        except Exception, e:
            self.message = u'%s (%s)' % (self.connectionError, exceptionToUnicode(e))

        if self.reader is None:
            if not self.message:
                self.message = u'%s' % (self.connectionError, )
            return

        try:
            self.result = self.reader.read()
        except:
            pass # нет смысла выбрасывать исключение в отдельном потоке
                 # и нет смысла его обрабатывать - оно скорее всего наведённое


    def closeReader(self):
        try:
            if self.reader is not None:
                self.reader.close()
            self.reader = None
        except:
            pass


class CJsonRpcClientHttpTransport:
    def __init__(self, url, user=None, password=None, realm=None):
        self.url = url
        self.user = user
        self.password = password
        self.timeout = 45.0

        self.redirectionHandler = CSimpleRedirector()
        handlers = [ self.redirectionHandler ]

# так правильно
#        if user:
#            self.passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
#            self.passwordManager.add_password(realm, self.url, user, password)
#            self.basicAuthHandler = urllib2.HTTPBasicAuthHandler(self.passwordManager)
#            handlers.append(self.basicAuthHandler)
## оставим про запас
##            self.digestAuthHandler = urllib2.HTTPDigestAuthHandler(self.passwordManager)
##            handlers.append(self.digestAuthHandler)
## это бывает полезно для отладки
#        self.httpHandler = urllib2.HTTPHandler()
#        self.httpHandler.set_http_debuglevel(1)
#        handlers.append(self.httpHandler)

        self.opener = urllib2.build_opener(*handlers)


    def exchange(self, data, timeout = 60):
        request = urllib2.Request(self.url)
        request.add_header('Content-type', 'application/json')
        request.add_header('Accept', 'application/json')
        request.add_header('Connection', 'close')
        request.add_header('User-agent', 'jsonrpc/1.0')

# а так - быстрее (но годится только для basic auth
#        if self.user:
#            user     = self.user.encode('utf8') if isinstance(self.user, unicode) else str(self.user)
#            password = self.password.encode('utf8') if isinstance(self.password, unicode) else str(self.password)
#            request.add_header('Authorization', 'Basic ' + base64.b64encode(user + ':' + password))

# а так - не работает, нужно писать свой HTTPHandler
#        request.add_header('Expect', '100-continue')
        if isinstance(data, unicode):
            data = data.encode('utf8')
        request.add_data(data)

        r = self.opener.open(request, timeout = timeout)
        d = r.read()
        return d


class CJsonRpcClent:
    def __init__(self, url, user=None, password=None, realm=None):
        self.transport = CJsonRpcClientHttpTransport(url, user, password, realm)
        self.requestId = 0


    def call(self, methodName, params=None, timeout = 60):
        request = self.preparerequest(self.getRequestId(), methodName, params)
        raw_response = self.transport.exchange(json.dumps(request), timeout)
        try:
            response = json.loads(raw_response)
        except Exception, e:
            raise Exception(exceptionToUnicode(e) + u'\n' + raw_response)
        if 'error' in response:
            error = response['error']
            raise self.createException(error)
        else:
            return response.get('result')


    def notify(self, methodName, params=None):
        request = self.preparerequest(None, methodName, params)
        encodedResponse = self.transport.exchange(json.dumps(request))
        if encodedResponse:
            response = json.loads(encodedResponse)
            if 'error' in response:
                error = response['error']
                raise self.createException(error)
            else:
                return None


    def preparerequest(self, id, methodName, params):
        request = { 'jsonrpc': '2.0',
                    'method' : methodName,
                  }
        if params is not None:
           request['params'] = params

        if id is not None:
           request['id'] = id
        return request


    def getRequestId(self):
        self.requestId += 1
        return self.requestId


    @staticmethod
    def createException(error):
        if ( isinstance(error, dict) ):
            return exceptionFactory( error.get('code'), error.get('message'), error.get('data') )
        else:
            return Exception('parse response bug')


#    def batch(self):
#        return CJsonRpcBatch(self)


#    def process(self, batch):
#        list = [ self.preparerequest(*task) for task in batch ]
#        encodedResponse = self.transport.exchange(json.dumps(list))
#        if encodedResponse:
#            response = json.loads(encodedResponse)
#            if isinstance(response, dict):
#                error = response.get('error')
#                raise self.createException(error)
#            else:
#                return response
#        return None


#class CJsonRpcBatch:
#    def __init__(self, client):
#        self.client = client
#        self.calls = []
#
#    def call(self, id, methodName, params=None):
#        self.calls.append((id, methodName, params))
#
#
#    def notify(self, methodName, params=None):
#        self.calls.append((None, methodName, params))
#
#
##    def fluch(self):
##        self.calls = []
#
#    def proceed(self):
#        return self.client.process(self.calls)
