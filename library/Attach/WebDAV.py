#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Начальная реализация клиента WebDAV
##
#############################################################################

from PyQt4 import QtGui

import collections
import datetime
import email.utils
import os
import os.path
import posixpath
import requests
import requests.exceptions
import urllib
import urlparse
import xml.etree.ElementTree as xml


DirInfo  = collections.namedtuple('DirInfo',
                                   ('name',
                                    'lastmodified',
                                   )
                                 )

FileInfo = collections.namedtuple('FileInfo',
                                   ('name',
                                    'contentType',
                                    'contentLength',
                                    'lastmodified',
                                   )
                                 )



class EWebDavException(Exception):
    u'У webdav что-то нехорошо'
    def __init__(self, title, url, code, reason):
        Exception.__init__(self, u'%s %s failed with [%s] %s' % (title, url, code, reason))


class EInvalidPath(Exception):
    u'получился недопустимый путь'
    def __init__(self, path):
        Exception.__init__(self, 'Invalid path "%s"' % path)


class EInvalidDirectory(Exception):
    u'получился недопустимый директорий'
    def __init__(self, url):
        Exception.__init__(self, 'Invalid directory "%s"' % url)


class CWebDAVClient:
    u'клиент для загрузки файлов по протоколу WebDAV'

    CHUNK_SIZE = 1048576

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.cwd = '/'


    def _upath(self, path):
        u'преобразует путь на сервере с учётом cwd'
        result = path if posixpath.isabs(path) else posixpath.join(self.cwd, path)
        if not posixpath.isabs(result):
            raise EInvalidPath(path)
        if result.startswith('//'):
            result = result[1:]
        return result


    def _geturl(self, path):
        u'преобразует путь на сервере с учётом cwd в url'
        return self.baseUrl + self._upath(path)


    def _request(self, title, method, url, codes, **kwargs):
        u'основной запрос'
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code not in codes:
                raise EWebDavException(title, url, response.status_code, response.reason)
            return response
        except requests.exceptions.RequestException:
            QtGui.qApp.logCurrentException()
            raise EWebDavException(title, url, '-', 'request error (see error.log for details)')


    def _strToDateTime(self, s):
        u'даты создания и изменения файлов возвращаются в формате RFC 1123, «D, d M Y H:i:s O»'
#        print '_strToDateTime: [%s]' % s
        if s:
            timestamp = email.utils.mktime_tz(email.utils.parsedate_tz(s))
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None


    def _extractNodeInfo(self, element, basePath):
        u'разбор описания узла'
# это работает в python 2.7:
#        path = urllib.unquote(element.findtext('.{DAV:}href', '')).decode('utf8')
#        prop = element.find('.{DAV:}propstat/{DAV:}prop')
#        isCollection = prop.find('.{DAV:}resourcetype/{DAV:}collection') is not None
#        lastmodified = self._strToDateTime( prop.findtext('.{DAV:}getlastmodified') )
# а это - в 2.6:
        path = urllib.unquote(element.findtext('{DAV:}href', '')).decode('utf8')
        propstat = element.find('{DAV:}propstat')
        prop     = propstat.find('{DAV:}prop')
        resourcetype = prop.find('{DAV:}resourcetype')
        isCollection = resourcetype.find('{DAV:}collection') is not None
#        lastmodified = self._strToDateTime( prop.findtext('.{DAV:}getlastmodified') )
        lastmodified = self._strToDateTime( prop.findtext('{DAV:}getlastmodified') )

        if isCollection:
            if path.endswith('/'):
                path = path[:-1]
            if path == basePath:
                path = '.'
            else:
                path = posixpath.basename(path)
            return DirInfo(path, lastmodified)
        else:
#            contentType   = prop.findtext('.{DAV:}getcontenttype')
#            contentLength = int(prop.findtext('.{DAV:}getcontentlength','0'))
            contentType   = prop.findtext('{DAV:}getcontenttype')
            contentLength = int(prop.findtext('{DAV:}getcontentlength','0'))
            return FileInfo(posixpath.basename(path), contentType, contentLength, lastmodified)


    def _isDir(self, path):
        u'признак того, что путь соответствует директорию'
        # True: is dir
        # False: is file
        # None: not exists
        url = self._geturl(path)
        response = self._request('Check node type', 'PROPFIND', url, (404, 200, 207), headers={'Depth':'0'})
        if response.status_code == 404:
            return None
        tree = xml.fromstring(response.content)
#        isCollection = tree.find('.{DAV:}response/{DAV:}propstat/{DAV:}prop/{DAV:}resourcetype/{DAV:}collection') is not None
        response = tree.find('{DAV:}response')
        propstat = response.find('{DAV:}propstat')
        prop     = propstat.find('{DAV:}prop')
        resourcetype = prop.find('{DAV:}resourcetype')
        isCollection = resourcetype.find('{DAV:}collection') is not None
        return isCollection


    def _mkdir(self, path):
        u'низкоуровневое создание директория'
        url = self._geturl(path)
        self._request('mkdir', 'MKCOL', url, (201,))


    def cd(self, path):
        u'сменить директорий'
        if not self._isDir(path):
            raise EInvalidDirectory(self._geturl(path))
        self.cwd = self._upath(path)



    def ls(self, path=''):
        u'список файлов директория'
        url = self._geturl(path)
        basePath = posixpath.normpath( urlparse.urlsplit(url).path )
        response = self._request('list files', 'PROPFIND', url, (200, 207), headers={'Depth':'1'})
        tree = xml.fromstring(response.content)
        return [ self._extractNodeInfo(element, basePath)
                 for element in tree.findall('{DAV:}response')
               ]


    def mkdir(self, path):
        u'создать директорий "по богатому" - на произв. глубину'
        upath = self._upath(path)
        trails = []
        while True:
            isDir = self._isDir(upath)
            if isDir is None:
                upath, part = posixpath.split(upath)
                if part == '':
                    raise EInvalidDirectory(self._geturl(path))
                trails.insert(0, part)
            elif isDir:
                break
            else:
                raise EInvalidDirectory(self._geturl(path))
        for trail in trails:
            upath = posixpath.join(upath, trail)
            self._mkdir(upath)


    def rm(self, path):
        u'удалить файл или директорий'
        url = self._geturl(path)
        self._request('remove', 'DELETE', url, (204,))


    def mv(self, oldPath, newPath):
        u'переместить файл'
        oldUrl = self._geturl(oldPath)
        newUrl = self._geturl(newPath)
        headers = {'Destination':newUrl.encode('utf8'),
                   'Overwrite': 'F',
                   'Depth': '1',
                  }
        self._request('move', 'MOVE', oldUrl, (201,204,), headers=headers)


    def uploadStream(self, path, stream):
        u'загрузить файл из потока'
        url = self._geturl(path)
        headers = {}
#        try:
#            mtime = os.fstat(stream.fileno()).st_mtime
#            headers['Last-Modified'] = email.utils.formatdate(mtime, False, True)
#            print repr(headers)
#        except:
#            pass
        self._request('upload', 'PUT', url, (200, 201, 204), data=stream, headers=headers)


    def uploadFile(self, path=None, localFile=None):
        u'загрузить файл из локального файла'
        if path is None:
            path = os.path.basename(localFile)
        self.uploadStream(path, open(localFile, 'rb'))


    def downloadStream(self, path, stream):
        u'скачать файл в поток'
        url = self._geturl(path)
        response = self._request('download', 'GET', url, (200,), stream=True)
        for chunk in response.iter_content(self.CHUNK_SIZE):
            stream.write(chunk)


    def downloadFile(self, path, localFile=None):
        u'скачать файл в локальный файл'
        if localFile is None:
            localFile = posixpath.basename(path)
        with open(localFile, 'wb') as stream: # в случае отказа файл останется?
            self.downloadStream(path, stream)




#    def setProps(self, filePath, props):
#        pass

#    def getProps(self, filePath):
#        pass



if __name__ == '__main__':

    c = CWebDAVClient('http://serv/sabre')
#    c = CWebDAVClient('http://serv/storage')
#    print c.ls()
    print c.ls('Music/Fizika-Tretiakov.mp3')
#    print c.ls('mumu')

#    print c._isDir('/Music')
#    print c._isDir('/Music/Fizika-Tretiakov.mp3')
#    print c._isDir('/01/02/03')

    c.mkdir('/01/02/03')
    c.cd('/01/02/03')
    c.uploadFile(localFile='sample.txt')
    c.uploadStream('sample2.txt', '-sample-2-')
    print c.ls()
    c.downloadFile('sample2.txt')
    c.mv('sample2.txt', 'sample2a.txt')

    c.rm('/01')

#    c.setProps('sample.txt', { 'clientId' : 123, 'eventId': 321 })
#    print c.getProps('sample.txt');
#    print c.get('sample.txt')

