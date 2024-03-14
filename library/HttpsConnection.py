# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Обнаружено, что разные платформы и разрые версии питона имеют
## серьёзные различия в реализации httplib.HTTPSConnection,
## поэтому проще завести свою реализацию чем настраивать существующую :(
##
## Плюс к этому обнаружено, что несмотря на то, что в стандартной библиотеке
## есть logger, ни ZSI ни httplib.HTTPConnection его не используют,
## а тупо гонят вывод в файлы.
##
## При этом ZSI не выводит всей интересующей информации,
## (url, заголовки http) зато выводит в произвольный файл
## тогда как httplib.HTTPConnection выводит заголовки и запрос - не не ответ
## да и выводит в sys.stdout :(
##
#############################################################################

import base64
import logging
import httplib
import socket
import ssl


class CHttpsConnection(httplib.HTTPSConnection):
    @staticmethod
    def getCaPath():
        # None: не проверят сертификат
        # варианты реализации:
        # - использовать setuptools.ssl_support.find_ca_bundle()
        #   при этом для виндовс нужно дополнительно установить wincertstore или аналог (https://pypi.org/project/wincertstore/)
        # - использовать переменную окружения getenv('SSL_CERT_FILE')
        return None

    def __init__(self, host, port=None, proxy={}):
        proxyAddress  = proxy.get('address', None)
        proxyPort     = proxy.get('port', None)
        proxyLogin    = proxy.get('login', None)
        proxyPassword = proxy.get('password', None) or ''
        if proxyAddress and proxyPort:
            httplib.HTTPSConnection.__init__(self, proxyAddress, port=proxyPort)
            headers = {}
            if proxyLogin:
                headers['Proxy-Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % (proxyLogin, proxyPassword))
            if hasattr(self, 'set_tunnel'):
                # 2.7
                set_tunnel = self.set_tunnel
            else:
                # 2.6
                set_tunnel = self._set_tunnel
            set_tunnel(host, port or self.default_port, headers)
        else:
            httplib.HTTPSConnection.__init__(self, host, port=port or self.default_port)
        self.logger = logging.getLogger('soap')
        self.auto_open = False


    def connect(self):
        try:
            self.logger.info(u'connect: ' + '%s:%s' % (self.host, self.port))
        except UnicodeDecodeError:
            pass
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        self.sock = ssl.wrap_socket(sock,
                                    keyfile=self.key_file,
                                    certfile=self.cert_file,
                                    ca_certs=self.getCaPath()
#                                       server_side=False,
#                                       cert_reqs=CERT_NONE,
#                                       ssl_version=PROTOCOL_SSLv23,
#                                       ca_certs=None,
#                                       do_handshake_on_connect=True,
#                                       suppress_ragged_eofs=True)
                                   )


    def send(self, data):
        try:
            self.logger.info(u'send: ' + data)
        except UnicodeDecodeError:
            pass
        httplib.HTTPSConnection.send(self, data)


    def getresponse(self):
        result = httplib.HTTPSConnection.getresponse(self)
        try:
            self.logger.info(u'resp: %s %s\n%s' % (result.status, result.reason, result.msg))
        except UnicodeDecodeError:
            pass
        origRead = result.read

        result.read = lambda amt=None: self.__read(origRead, amt)
        return result


    def __read(self, origRead, amt):
        result = origRead(amt)
        try:
            self.logger.info(u'read: ' + result)
        except UnicodeDecodeError:
            pass
        return result
