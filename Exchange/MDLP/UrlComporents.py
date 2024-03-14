#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
## в python есть urlparse, но мне его немного не хватило: 
## мне нужно выделять и заменять схему, host и порт
## в Qt есть QUrl, но я не хочу завязываться на Qt.
##
#############################################################################

import urlparse

class CUrlComporents:
    defaultPorts = { 'http' : 80,
                     'https': 443
                   }
    def __init__(self, url):
        ( self.scheme,
          netloc,
          self.path,
          self.params,
          self.query,
          self.fragment
        ) = urlparse.urlparse(url)
        self.username, self.password, self.host, self.port = self._parseNetLoc(netloc)
        if not self.port:
            self.port = self.defaultPorts.get(self.scheme, None)


    def unparse(self):
        port = self.port if self.port != self.defaultPorts.get(self.scheme) else None
        netloc = self._unparseNetLoc(self.username,
                                     self.password,
                                     self.host,
                                     port
                                    )
        return urlparse.urlunparse((self.scheme,
                                    netloc,
                                    self.path,
                                    self.params,
                                    self.query,
                                    self.fragment)
                                  )


    def __str__(self):
        return self.unparse()


    def __unicode__(self):
        return self.unparse()


    @staticmethod
    def _parseNetLoc(netloc):
        username = password = host = ''
        port = None
        components = netloc.rsplit('@',1)
        if len(components) == 2:
            userInfo, hostPart = components
        else:
            userInfo, hostPart = '', netloc
        if userInfo:
           usernameAndPassword = userInfo.rsplit(':',1)
           if len(usernameAndPassword) == 2:
               username, password = usernameAndPassword
           else:
               username, password = userInfo, ''
        if hostPart:
            hostAndPort = hostPart.rsplit(':',1)
            if len(hostAndPort) == 2 and hostAndPort[1].isdigit():
                host = hostAndPort[0]
                port = int(hostAndPort[1])
            else:
                host = hostPart
                port = None
        return username, password, host, port


    @staticmethod
    def _unparseNetLoc(username, password, host, port):
        authPart = (username or '')
        if authPart:
            authPart +=  ':' + password
        hostAndPort = host or ''
        if port:
            hostAndPort += ':' + str(port)
        if authPart:
            return authPart + '@' + hostAndPort
        else:
            return hostAndPort


#u = CUrlComporents('https://api.sb.mdlp.crpt.ru/api/v1/auth')
#u.scheme = 'http'
#u.host = '127.0.0.1'
#u.port = 8080
#print u.unparse()

