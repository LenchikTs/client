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
## Интерфес для доступа к хранилищу из модели и кнопки,
## считается что в приложении достаточного одного экземпляра
##
#############################################################################

import os.path
import posixpath
import requests
import requests.exceptions
import uuid
from cStringIO import StringIO
from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDateTime

from library.Attach.WebDAV import CWebDAVClient, FileInfo, EWebDavException

from library.Attach.AttachedFile import CAttachedFile


class CWebDAVInterface:
    u'Интерфес для доступа к файлам из модели и кнопки, считается что в приложении достаточного одного экземпляра'

    def __init__(self):
        self.client = None


    def __nonzero__(self):
        return bool(self.client)


    def setWebDAVUrl(self, url):
        if url:
            self.client = CWebDAVClient(url)

            try:
                requests.request('PROPFIND', url)
            except requests.exceptions.RequestException:
                QtGui.qApp.logCurrentException()

                messageBox = QtGui.QMessageBox(
                    QtGui.QMessageBox.Warning,
                    u'Ошибка доступа',
                    u"На данном рабочем месте нет доступа к файлохранилищу по адресу: {0}".format(url))
                messageBox.exec_()

                self.client = None

        else:
            self.client = None


    def getTmpDir(self):
        d = QDate.currentDate()
        return 'tmp/%04d/%02d/%02d/%s' % ( d.year(), d.month(), d.day(), uuid.uuid1() )


    def getPersistentDir(self):
        d = QDate.currentDate()
        return '%04d/%02d/%02d/%s' % ( d.year(), d.month(), d.day(), uuid.uuid1() )


    def createAttachedFileItem(self, attachedFilePath):
        try:
            fileInfoList = self.client.ls(attachedFilePath)
        except EWebDavException:
#            print repr(e)
            QtGui.qApp.logCurrentException()
            fileInfoList = []
        if fileInfoList and len(fileInfoList) == 1 and isinstance(fileInfoList[0], FileInfo):
            fileInfo = fileInfoList[0]
            return CAttachedFile.remoteFile(attachedFilePath, fileInfo.contentLength, QDateTime(fileInfo.lastmodified))
        else:
            return CAttachedFile.lostFile(attachedFilePath)


    def createTmpAttachedFileItem(self, attachedFilePath):
        fileInfoList = self.client.ls(attachedFilePath)
        if fileInfoList and len(fileInfoList) == 1 and isinstance(fileInfoList[0], FileInfo):
            fileInfo = fileInfoList[0]
            return CAttachedFile.tmpFile(attachedFilePath, fileInfo.contentLength, QDateTime(fileInfo.lastmodified))
        else:
            return None # когда это бывает?


    def uploadBytes(self, name, bytes):
        tmpDir = self.getTmpDir()
        path = posixpath.join(tmpDir, os.path.basename(name))
        self.client.mkdir(tmpDir)
        self.client.uploadStream(path=path, stream=StringIO(bytes))
        return self.createTmpAttachedFileItem(path)


    def uploadFile(self, localFile):
        tmpDir = self.getTmpDir()
        path = posixpath.join(tmpDir, os.path.basename(localFile))
        self.client.mkdir(tmpDir)
        self.client.uploadFile(path=path, localFile=localFile)
        return self.createTmpAttachedFileItem(path)


    def uploadFiles(self, localFileList):
        return filter(None, [ self.uploadFile(localFile) for localFile in localFileList])


    def saveFile(self, attachedFileItem):
        if attachedFileItem.isLost:
            pass
        if not attachedFileItem.persistentDir:
            persistentDir = self.getPersistentDir()
            oldPath = attachedFileItem.getPath()
            newPath = posixpath.join(persistentDir, attachedFileItem.newName)
            self.client.mkdir(persistentDir)
            self.client.mv(oldPath, newPath)
            attachedFileItem.persistentDir, attachedFileItem.oldName = persistentDir, attachedFileItem.newName
        elif attachedFileItem.oldName != attachedFileItem.newName:
            oldPath = attachedFileItem.getPath()
            newPath = posixpath.join(attachedFileItem.persistentDir, attachedFileItem.newName)
            self.client.mv(oldPath, newPath)
            attachedFileItem.oldName = attachedFileItem.newName


    def saveFiles(self, attachedFileItemList):
        for attachedFileItem in attachedFileItemList:
            self.saveFile(attachedFileItem)


    def getUrl(self, attachedFileItem):
        return self.client._geturl(attachedFileItem.getPath())


    def downloadFile(self, attachedFileItem, localFile):
       self.client.downloadFile(attachedFileItem.getPath(), localFile)


    def downloadBytes(self, attachedFileItem):
       stream = StringIO()
       self.client.downloadStream(attachedFileItem.getPath(), stream)
       return stream.getvalue()


    def downloadFile_test(self, path, localFile):
       self.client.downloadFile(path, localFile)

