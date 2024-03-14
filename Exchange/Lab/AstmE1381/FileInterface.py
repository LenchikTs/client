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
## Средство приёма/отравки отного сообщения согласно протокола ASTM E1381
## (через файлы)
##
#############################################################################

import os
import time


class CFileInterface(object):
    EOL = '\r\n'
    lastUsedTs = None
    tsCounter = 0

    def __init__(self, opts):
        self.inDir        = self.expand(opts.get('inDir', opts.get('dir', '.')))
        self.inPrefix     = opts.get('inPrefix', opts.get('prefix',''))
        self.inDataExt    = self.fixExt(opts.get('inDataExt', opts.get('dataExt','')))
        self.inSignalExt  = self.fixExt(opts.get('inSignalExt',opts.get('signalExt','.ok')))

        self.outDir       = self.expand(opts.get('outDir', opts.get('dir', '.')))
        self.outPrefix    = opts.get('outPrefix', opts.get('prefix',''))
        self.outDataExt   = self.fixExt(opts.get('outDataExt', opts.get('dataExt','')))
        self.outSignalExt = self.fixExt(opts.get('outSignalExt',opts.get('signalExt','.ok')))


    @classmethod
    def createFile(cls, dir, prefix, suffix, appendIntoFileName=''):
        while True:
            ts = time.localtime()
            if cls.lastUsedTs != ts:
                cls.lastUsedTs = ts
                cls.tsCounter = 0
            else:
                cls.tsCounter += 1
            if cls.tsCounter:
                fileName = '%s%s%s_%03d%s' % (prefix, appendIntoFileName, time.strftime('%y%m%d_%H%M%S'), cls.tsCounter, suffix)
            else:
                fileName = '%s%s%s%s' % (prefix, appendIntoFileName, time.strftime('%y%m%d_%H%M%S'), suffix)
            filePath = os.path.join(dir, fileName)
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            flags |= os.__dict__.get('O_BINARY',0)
            try:
                fileHandle = os.open(filePath, flags, 0666)
                return fileHandle, filePath
            except OSError, e:
                if e.errno != os.errno.EEXIST:
                    raise


    @classmethod
    def reuseFile(cls, dir, fileName, signalExt):
        filePath = os.path.join(dir, fileName)
        signalFilePath = cls.replaceExt(filePath, signalExt)
        try:
            os.unlink(signalFilePath)
        except OSError, e:
            if e.errno != os.errno.ENOENT:
                raise
        flags = os.O_CREAT | os.O_TRUNC | os.O_WRONLY
        flags |= os.__dict__.get('O_BINARY',0)
        fileHandle = os.open(filePath, flags, 0666)
        return fileHandle, filePath


    @staticmethod
    def expand(path):
        return os.path.expandvars(os.path.expanduser(path))


    @staticmethod
    def fixExt(ext):
        if ext == '.':
            return ''
        if ext and not ext.startswith('.'):
            return '.'+ext
        return ext


    @staticmethod
    def replaceExt(fileName, ext):
        prefix, suffix = os.path.splitext(fileName)
        return prefix + ext


    @staticmethod
    def extIs(fileName, ext):
        prefix, suffix = os.path.splitext(fileName)
        if suffix == '.':
            suffix = ''
        return suffix == ext


    def write(self, message, forceFileName=None, appendIntoFileName=''):
        # handle - ориентированный I/O появился из-за того, что я не знаю
        # как более высокоуровневыми средствами python создать файл с условием O_EXCL
        if forceFileName:
            handle, dataFilePath = self.reuseFile(self.outDir,
                                                  forceFileName,
                                                  self.outSignalExt)
        else:
            if appendIntoFileName:
                appendIntoFileName += '_'
            handle, dataFilePath = self.createFile(dir=self.outDir,
                                                   prefix=self.outPrefix,
                                                   suffix=self.outDataExt,
                                                   appendIntoFileName=appendIntoFileName)
        try:
            os.write(handle, self.EOL.join(message.body))
            os.write(handle, self.EOL)
            os.fsync(handle)
        finally:
            os.close(handle)
        signalFilePath = self.replaceExt(dataFilePath, self.outSignalExt)
        signalFile = file(signalFilePath, 'w')
        signalFile.close()
        return dataFilePath


