#! /usr/bin/env python
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
##
## Цикл приёма/отравки сообщений согласно протокола ASTM E1381
## (через файлы)
##
#############################################################################

import os
import time

from library.Utils     import anyToUnicode, exceptionToUnicode

from FileInterface     import CFileInterface
from AbstractLoop      import CBaseMessage, CAbstractLoop
from Exchange.Lab.AstmE1394.Message import EUnexpectedRecord



class CFileMessage(CBaseMessage):
    def __init__(self, body, source, signalFilePath, dataFilePatch):
        CBaseMessage.__init__(self, body)
        self.source = source
        self.signalFilePath = signalFilePath
        self.dataFilePatch = dataFilePatch
        self.encoding = 'utf8'


    def dismiss(self):
        if self.source:
            self.source.unlink(self.signalFilePath, self.dataFilePatch)
            self.source = None


class CFileExchangeLoop(CAbstractLoop, CFileInterface):
    fsCheckDelay = 1 # задержка цикла проверки файлов

    def __init__(self, opts):
        CAbstractLoop.__init__(self)
        CFileInterface.__init__(self, opts)
        self.inDirStat = None
        self._skipFileSet = set()
        self._encoding = opts.get('encoding', 'utf8')
        self._optsList = []
        self._externalInfo = {}


    def unlink(self, signalFilePath, dataFilePath):
        self.log(3, u'delete file "%s"' % signalFilePath)
        os.unlink(signalFilePath)
        self.log(3, u'delete file "%s"' % dataFilePath)
        os.unlink(dataFilePath)
        self._discardFileFromSkipList(signalFilePath)


    def _mainLoop(self):
        while not self.outputQueue.empty():
            self._putMessage()
        self._GetMessages()
        time.sleep(self.fsCheckDelay)


    def _putMessage(self):
        messageProcessed = False
        message = self.outputQueue.get_nowait()
        messageBody = message.body
        try:
            self.log(2, u'output message is %s' % repr(messageBody))
            handle, dataFilePath = CFileInterface.createFile(dir=self.outDir,
                                                             prefix=self.outPrefix,
                                                             suffix=self.outDataExt)
            try:
                dataFile = os.fdopen(handle,'wb')
                dataFile.write( self.EOL.join(messageBody) )
                dataFile.write( self.EOL )
            finally:
                dataFile.close()
            signalFilePath = self.replaceExt(dataFilePath, self.outSignalExt)
            signalFile = file(signalFilePath, 'w')
            signalFile.close()
            messageProcessed = True
        finally:
            if messageProcessed:
                if self.onMessageProcessed:
                    self.onMessageProcessed(message)
                message.dismiss()
                self.log(2, u'message is processed')
            else:
                self.outputQueue.put(message) # requeue it
                self.log(2, u'message is not processed')

    def _cannotChangeOpts(self):
        pass

    def _GetMessages(self):
        # код получился таким сложным от того, что я не уверен
        # что в код другой стороны будет сохранять регистр символов
        inDir = self.inDir
        inDirStat = os.stat(inDir)
        if self.inDirStat == inDirStat:
            self.log(3, u'input directory "%s" seems unchanged' % inDir)
            if not self.changeOpts():
                self._cannotChangeOpts()
            return

        fileNameList = os.listdir(inDir)
        fileNameListUC = [ fileName.upper() for fileName in fileNameList ]
        prefix = self.inPrefix.upper()
        dataExt = self.inDataExt.upper()
        signalExt = self.inSignalExt.upper()

        for i, fileNameUC in enumerate(fileNameListUC):
            if fileNameUC.startswith(prefix) and self.extIs(fileNameUC,signalExt) and not self._fileInSkipList(fileNameList[i]):
                self.log(3, u'signal file "%s" is detected' % fileNameList[i])
                dataFileNameUC = self.replaceExt(fileNameUC,dataExt)
                try:
                    j = fileNameListUC.index(dataFileNameUC)
                except:
                    j = -1
                if j>=0:
                    signalFilePath = os.path.join(inDir, fileNameList[i])
                    dataFilePath   = os.path.join(inDir, fileNameList[j])
                    try:
                        self._processDataFile(signalFilePath, dataFilePath)
                    except IOError, e:
                        self.log(1, u'"%s" I/O error(%s): %s' % (e.filename, e.errno, anyToUnicode(e.strerror)))
                    except EUnexpectedRecord, e:
                        self.log(1, u'"%s" Недопустимая строка #%d: %s' % (dataFilePath, e.row, anyToUnicode(e.content, self._encoding)))
                    except Exception, e:
                        self.log(1, u'"%s" Ошибка %s' % (dataFilePath, exceptionToUnicode(e)))
                    self.log(2, u'input message from file "%s" is processed' % dataFilePath)
        self.inDirStat = inDirStat

    def appendOpts(self, opts, externalInfo={}):
        self._optsList.append((opts, externalInfo))


    def changeOpts(self):
        if self._optsList:
            opts, externalInfo = self._optsList.pop()
            self._externalInfo = externalInfo
            CFileInterface.__init__(self, opts)
            self._encoding = opts.get('encoding', 'utf8')
            return True
        return False


    def _fileInSkipList(self, signalFileName):
        return signalFileName in self._skipFileSet


    def _addFileToSkipList(self, signalFilePath):
        self._skipFileSet.add(os.path.basename(signalFilePath))


    def _discardFileFromSkipList(self, signalFilePath):
        self._skipFileSet.discard(os.path.basename(signalFilePath))


    def _processDataFile(self, signalFilePath, dataFilePath):
        self.log(3, u'create message from file "%s"' % dataFilePath)
        file = open(dataFilePath, 'rU')
        messageBody = [ line.strip(self.EOL) for line in file ]
        file.close()
        message = CFileMessage(messageBody, self, signalFilePath, dataFilePath)
        message.encoding = self._encoding
        self.acceptInputMessage(message)
        self._addFileToSkipList(signalFilePath)
