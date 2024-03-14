# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2024 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Описание присоединённого файла, который хранится где-то
## и модель списка таких файлов.
##
#############################################################################

import posixpath
import locale
import zlib

from PyQt4 import QtGui
from PyQt4.QtCore  import (
                            Qt,
                            SIGNAL,
                            QAbstractTableModel,
                            QByteArray,
                            QDateTime,
                            QModelIndex,
                            QVariant,
                         )

from library.Utils import forceDateTime, forceRef, forceString, forceInt, toVariant
from library.CertComboBox import extractCertInfo
from library.MSCAPI       import MSCApi
from library.naturalSort import convertKeyForNaturalSort
from library.database    import CTableRecordCache


class CAttachedFileSignature:
    u"""Описание подписи присоединённого файла"""
    def __init__(self, signatureBytes=None, signerId=None, signingDatetime=None):
        self.signatureBytes  = signatureBytes   # отсоединённая подпись присоединённого файла
        self.signerId        = signerId         # id врача
        self.signingDatetime = signingDatetime  # дата и время подписи

        self.certName = None
        self.certHtml = None
        self.certCustom = None

        if self.signatureBytes:
            try:
                api = MSCApi(QtGui.qApp.getCsp())
            except:
#                QtGui.qApp.logCurrentException()
                self.certName = self.certHtml = u'ОШИБКА: Криптопровайдер не настроен'
                return

            try:
                with api.signatureAsStore(signatureBytes) as store:
                    for cert in store.listCerts():
                        with cert:
                            _, self.certName, self.certHtml = extractCertInfo(cert)
                            self.certCustom = cert
                            break
            except Exception:
                QtGui.qApp.logCurrentException()
                self.certName = self.certHtml = u'ОШИБКА: смотри журнал'


class CAttachedFileSignatureFull:
    u"""Полное описание подписи присоединённого файла (включая несохраненные подписи)"""
    def __init__(self, signId=None, signatureBytes=None, signerId=None, signingDatetime=None,
                                                            signerTitle=None, masterId=None):
        self.signId = signId
        self.signatureBytes  = signatureBytes   # отсоединённая подпись присоединённого файла
        self.signerId        = signerId         # id врача
        self.signingDatetime = signingDatetime  # дата и время подписи
        self.signerTitle = signerTitle
        self.masterId = masterId


class CAttachedFile:
    u"""Описание присоединённого файла, который хранится где-то (в WebDAV)"""
    def __init__(self):
        self._record       = None
        self.id            = None
        self.persistentDir = None
        self.tmpDir        = None
        self.oldName       = None
        self.newName       = None
        self.comment       = None

        self.size          = None
        self.lastModified  = None
        self.authorId      = None
        self.respSigner_name = None
#        self.author        = None

        self.respSignature = None
        self.orgSignature  = None
        self.additionalSignatures = None
        self.additionalSignaturesList = None  # Используется, в том числе для хранения не сохраненных в БД подписей
        self.htmlTemplate = None

        self.isLost        = False


    def _setRemoteFile(self, filePath, size, lastModified):
        self.persistentDir, self.oldName = posixpath.split(filePath)
        self.size = size
        self.lastModified = lastModified
        self.newName = self.oldName
        self.tmpDir  = None


    def _setLostFile(self, filePath):
        self.persistentDir, self.oldName = posixpath.split(filePath)
        self.newName = self.oldName
        self.tmpDir = None
        self.isLost = True


    def _setTmpFile(self, filePath, size, lastModified):
        self.tmpDir, self.oldName = posixpath.split(filePath)
        self.size = size
        self.lastModified = lastModified
        self.newName = self.oldName
        self.persistentDir = None
        self.isLost = False


    def setRecord(self, record):
        self._record = record
        self.id = forceRef(record.value('id'))
        self.comment = forceString(record.value('comment'))
        self.authorId = forceRef(record.value('createPerson_id'))
        self.setRespSignature(record.value('respSignatureBytes').toByteArray().data(),
                              forceRef(record.value('respSigner_id')),
                              forceDateTime(record.value('respSigningDatetime')))
        self.setOrgSignature(record.value('orgSignatureBytes').toByteArray().data(),
                             forceRef(record.value('orgSigner_id')),
                             forceDateTime(record.value('orgSigningDatetime')))
        self.respSigner_name = forceString(record.value('respSigner_name'))
        self.loadAdditionalSignatures(self.id)
        self.loadHtmlTemplate(self.id)
        if not self.htmlTemplate:
            html = forceString(record.value('html'))
            self.htmlTemplate = html if html else None


    def getRecord(self, table):
        if self._record:
            record = self._record
        else:
            record = table.newRecord()
            record.setValue('deleted', 0)
        record.setValue('path', self.getPath())
        record.setValue('comment', self.comment)
        if self.respSignature and self.respSignature.signatureBytes:
            record.setValue('respSignatureBytes', QByteArray(self.respSignature.signatureBytes))
            record.setValue('respSigner_id',      self.respSignature.signerId)
            record.setValue('respSigningDatetime', self.respSignature.signingDatetime)
            if self.respSignature.certCustom:
                record.setValue('respSigner_name', u'{0} {1} {2}'.format(forceString(self.respSignature.certCustom.surName()),
                                                                         forceString(self.respSignature.certCustom.givenName()),
                                                                         forceString(self.respSignature.certCustom.snils())))
            else:
                record.setValue('respSigner_name', None)
        if self.orgSignature and self.orgSignature.signatureBytes:
            record.setValue('orgSignatureBytes', QByteArray(self.orgSignature.signatureBytes))
            record.setValue('orgSigner_id',      self.orgSignature.signerId)
            record.setValue('orgSigningDatetime', self.orgSignature.signingDatetime)
        return record


    def loadAdditionalSignatures(self, masterId):
        db = QtGui.qApp.db
        table = db.table('Action_FileAttach_Signature')
        cond = db.joinAnd([table['deleted'].eq(0), table['master_id'].eq(masterId)])
        records = db.getRecordList(table, '*', cond)
        self.additionalSignatures = []
        self.additionalSignaturesList = []

        for record in records:
            signId = forceInt(record.value('id'))
            signBytes = record.value('signatureBytes').toByteArray().data()
            signerId = forceRef(record.value('signer_id'))
            signDatetime = forceDateTime(record.value('signingDatetime'))
            signerTitle = forceString(record.value('signerTitle'))
            self.additionalSignaturesList.append(CAttachedFileSignatureFull(signId=signId,
                                                                            signatureBytes=signBytes,
                                                                            signerId=signerId,
                                                                            signingDatetime=signDatetime,
                                                                            signerTitle=signerTitle,
                                                                            masterId=masterId
                                                                            ))
            self.additionalSignatures.append(CAttachedFileSignature(signatureBytes=signBytes,
                                                                    signerId=signerId,
                                                                    signingDatetime=signDatetime
                                                                    ))


    def loadHtmlTemplate(self, masterId):
        db = QtGui.qApp.db
        table = db.table('Action_FileAttach_PrintTemplate')
        record = db.getRecord(table, '*', masterId)
        if record:
            html = record.value('html').toByteArray()
            try:
                self.htmlTemplate = zlib.decompress(html).decode('utf8')
            except Exception:
                QtGui.qApp.logCurrentException()


    def addSignature(self, signId=None, signBytes=None, signerId=None, signDatetime=None,
                                                                signerTitle=None, masterId=None):
        self.additionalSignaturesList.append(CAttachedFileSignatureFull(signId=signId,
                                                                        signatureBytes=signBytes,
                                                                        signerId=signerId,
                                                                        signingDatetime=signDatetime,
                                                                        signerTitle=signerTitle,
                                                                        masterId=masterId
                                                                        ))
        self.additionalSignatures.append(CAttachedFileSignature(signatureBytes=signBytes,
                                                                signerId=signerId,
                                                                signingDatetime=signDatetime
                                                                ))


    def setAuthorId(self, authorId):
        self.authorId = authorId


    def setHtmlTemplate(self, html):
        self.htmlTemplate = html


    def setRespSignature(self, signatureBytes, singerId, signingDateTime):
        if signatureBytes:
            self.respSignature = CAttachedFileSignature(signatureBytes, singerId, signingDateTime)
        else:
            self.respSignature = None


    def hasRespSignature(self):
        s = self.respSignature
        return s and s.signatureBytes and s.signerId and s.signingDatetime


    def setOrgSignature(self, signatureBytes, singerId, signingDateTime):
        if signatureBytes:
            self.orgSignature = CAttachedFileSignature(signatureBytes, singerId, signingDateTime)
        else:
            self.orgSignature = None


    def hasOrgSignature(self):
        s = self.orgSignature
        return s and s.signatureBytes and s.signerId and s.signingDatetime


    def getRespSignerId(self):
        if self.respSignature and self.respSignature.signatureBytes:
            return self.respSignature.signerId
        return None


    def getRespSignerToolTip(self):
        if self.respSignature and self.respSignature.certHtml:
            return self.respSignature.certHtml
        return None


    def getOrgSignerId(self):
        if self.orgSignature and self.orgSignature.signatureBytes:
            return self.orgSignature.signerId
        return None


    def getOrgSignerToolTip(self):
        if self.orgSignature and self.orgSignature.certHtml:
            return self.orgSignature.certHtml
        return None


    @classmethod
    def remoteFile(cls, path, size, lastModified):
        result = cls()
        result._setRemoteFile(path, size, lastModified)
        return result


    @classmethod
    def lostFile(cls, path):
        result = cls()
        result._setLostFile(path)
        return result


    @classmethod
    def tmpFile(cls, path, size, lastModified):
        result = cls()
        result._setTmpFile(path, size, lastModified)
        result.setAuthorId(QtGui.qApp.userId)
        return result


    def rename(self, newName):
        self.newName = newName


    def edtComment(self, comment):
        self.comment = comment


    def getPath(self):
        return posixpath.join(self.persistentDir if self.persistentDir else self.tmpDir,
                              self.oldName
                             )


class CAttachedFilesLoader:

    @staticmethod
    def itemsPresent(interface, tableName, masterId):
        if interface:
            db = QtGui.qApp.db
            table = db.table(tableName)
            cond = db.joinAnd([table['deleted'].eq(0), table['master_id'].eq(masterId)])
            return db.getCount(table, countCol='1', where=cond)
        else:
            return 0


    @staticmethod
    def loadItems(interface, tableName, masterId):
        if interface:
            db = QtGui.qApp.db
            table = db.table(tableName)
            cond = db.joinAnd([table['deleted'].eq(0), table['master_id'].eq(masterId)])
            records = db.getRecordList(table, '*', cond)
            result = []
            for record in records:
                path = forceString(record.value('path'))
                item = interface.createAttachedFileItem(path)
                item.setRecord(record)
                result.append(item)
            return result
        else:
            return []


    @staticmethod
    def loadItemsFromRecords(interface, records):
        if interface:
            result = []
            for record in records:
                path = forceString(record.value('path'))
                item = interface.createAttachedFileItem(path)
                item.setRecord(record)
                result.append(item)
            return result
        else:
            return []


    @staticmethod
    def saveItems(interface, tableName, masterId, items):
        if interface:
            interface.saveFiles(items)
            idSet = set([item.id for item in items if item.id])
            db = QtGui.qApp.db
            table = db.table(tableName)
            cond = db.joinAnd([table['deleted'].eq(0),
                               table['master_id'].eq(masterId),
                               table['id'].notInlist(idSet)
                              ])
            db.deleteRecord(table, cond)
            for item in items:
                record = item.getRecord(table)
                record.setValue('master_id', masterId)
                _id = db.insertOrUpdate(table, record)
                item.id = _id
                CAttachedFilesLoader.saveAdditionalSign(item)
                CAttachedFilesLoader.savePrintTemplate(item)
                item.setRecord(record)

    @staticmethod
    def saveAdditionalSign(item):
        db = QtGui.qApp.db
        tableAFAS = db.table('Action_FileAttach_Signature')
        signList = item.additionalSignaturesList
        if signList:
            for sign in signList:
                if not sign.signId:
                    signatureBytes = sign.signatureBytes
                    signerId = sign.signerId
                    signingDatetime = sign.signingDatetime
                    signerTitle = sign.signerTitle
                    masterId = item.id
                    record = tableAFAS.newRecord()
                    record.setValue('createDatetime', toVariant(QDateTime().currentDateTime()))
                    record.setValue('createPerson_id', QtGui.qApp.userId)
                    record.setValue('modifyDatetime', toVariant(QDateTime().currentDateTime()))
                    record.setValue('modifyPerson_id', QtGui.qApp.userId)
                    record.setValue('master_id', masterId)
                    record.setValue('signatureBytes', QByteArray(signatureBytes))
                    record.setValue('signer_id', signerId)
                    record.setValue('signingDatetime', signingDatetime)
                    record.setValue('signerTitle', toVariant(signerTitle))
                    db.insertOrUpdate(tableAFAS, record)


    @staticmethod
    def savePrintTemplate(item):
        if item.htmlTemplate:
            db = QtGui.qApp.db
            table = db.table('Action_FileAttach_PrintTemplate')
            record = db.getRecord(table, '*', item.id)
            if not record:
                record = table.newRecord()
                value = item.htmlTemplate.encode('utf8')
                compData = zlib.compress(value)
                record.setValue('id', item.id)
                record.setValue('html', QByteArray(compData))
                db.insertRecord(table, record)


class CAttachedFilesModel(QAbstractTableModel):
    u"""Список прикреплённых файлов"""

    def __init__(self, parent):
        QAbstractTableModel.__init__(self)
        self.interface = None
        self.tableName = None
        self.items = []
        self.personsCache = CTableRecordCache(QtGui.qApp.db, 'vrbPersonWithSpeciality', '*')


    def setInterface(self, interface):
        self.interface = interface


    def setTable(self, tableName):
        self.tableName = tableName


    def loadItems(self, masterId):
        self.items = CAttachedFilesLoader.loadItems(self.interface, self.tableName, masterId)
        self.reset()


    def saveItems(self, masterId):
        CAttachedFilesLoader.saveItems(self.interface, self.tableName, masterId, self.items)


    def columnCount(self, index=None):
        return 8


    def rowCount(self, index=None):
        return len(self.items)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant((u'Имя файла', u'Комментарий', u'Размер', u'Дата', u'Автор', u'Владелец подписи', u'Подпись отв.лица', u'Подпись организации')[section])
        return QVariant()


#    def flags(self, index):
#        row = index.row()
#        item = self.items[row]
#        if item.isLost:
#            return Qt.ItemIsSelectable
#        else:
#            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def _getPersonName(self, personId):
        return self.personsCache.get(personId).value('name') if personId else None


    def _getAddSignatures(self, currentItem):
        if currentItem:
            res = []
            result = ''
            additionalSignatures = currentItem.additionalSignaturesList
            if additionalSignatures:
                for sign in additionalSignatures:
                    if forceString(sign.signerTitle):
                        titleList = forceString(sign.signerTitle).split(',')[0].split(' ')
                        fullLastName = titleList[0] if titleList else ''
                        cutFirstName = u' %s.' % titleList[1][:1] if len(titleList) >= 2 else ''
                        cutPatrName = u' %s.' % titleList[2][:1] if len(titleList) == 3 else ''
                        temp = u'{0}{1}{2}'.format(fullLastName, cutFirstName, cutPatrName)
                    else:
                        temp = u'----'
                    if sign.signId:
                        res.append(u'{1} {0} <b>ЭЦП</b> {2} <br>'.format(
                            forceString(self._getPersonName(sign.signerId)),
                            forceString(sign.signingDatetime), temp))
                    else:
                        res.append(u'{1} {0} <b>ЭЦП</b> {2} - ПОДПИСЬ НЕ СОХРАНЕНА<br>'.format(
                            forceString(self._getPersonName(sign.signerId)),
                            forceString(sign.signingDatetime), temp))
                result = '\n'.join(res)
            return result


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            item = self.items[row]
            if column == 0:
                return QVariant(item.newName)
            if column == 1:
                return QVariant(item.comment)
            elif column == 2:
                return QVariant(item.size)
            elif column == 3:
                return QVariant(item.lastModified)
            elif column == 4:
                return QVariant(self._getPersonName(item.authorId))
            elif column == 5:
                if item.respSignature and item.respSignature.certCustom:
                    respSigner_name = u'{0} {1} {2}'.format(forceString(item.respSignature.certCustom.surName()),
                                                            forceString(item.respSignature.certCustom.givenName()),
                                                            forceString(item.respSignature.certCustom.snils())) if item.respSignature else None
                else:
                    respSigner_name = None
                return QVariant(item.respSigner_name if item.respSigner_name else respSigner_name)
            elif column == 6:
                return self._getPersonName(item.getRespSignerId())
            elif column == 7:
                return self._getPersonName(item.getOrgSignerId())
            # elif column == 7:
            #     return QVariant(self._getAddSignatures(item.additionalSignatures))
            return QVariant()

        elif role == Qt.TextAlignmentRole:
            column = index.column()
            if column == 0:
                return QVariant(Qt.AlignLeft | Qt.AlignVCenter)
            elif column == 2:
                return QVariant(Qt.AlignRight | Qt.AlignVCenter)
            elif column == 3:
                return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
            elif column == 4:
                return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
            elif column == 5:
                return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
            elif column == 6:
                return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
            return QVariant(Qt.AlignLeft | Qt.AlignVCenter)

        elif role == Qt.DecorationRole:
            row = index.row()
            column = index.column()
            item = self.items[row]
            if column == 0:
                if item.isLost:
                    return QVariant(QtGui.qApp.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning))
                else:
                    #                    return QVariant(QtGui.QIcon(QtGui.QPixmap(row*10,row*10)))
                    return QVariant(QtGui.QColor(0, 0, 0, 0))
        #        elif role == Qt.DecorationRole:
            if column == 4:
                if item.additionalSignatures:
                    return QVariant(QtGui.qApp.style().standardIcon(QtGui.QStyle.SP_MessageBoxInformation))
                return QVariant()

        elif role == Qt.ToolTipRole:
            column = index.column()
            if column == 4:
                row = index.row()
                item = self.items[row]
                tooltip = ('<html><body><table width = 400>'
                           + ''.join(
                            '<tr><td>%s</td></tr>' % (self._getAddSignatures(item))
                            # '<tr><td>%s</td></tr>' % (self._getAddSignatures(item.id))
                           + '</table></body></html>'))
                return tooltip
                # return QVariant(self._getAddSignatures(item.id))
            if column == 6:
                row = index.row()
                item = self.items[row]
                return QVariant(item.getRespSignerToolTip())
            if column == 7:
                row = index.row()
                item = self.items[row]
                return QVariant(item.getOrgSignerToolTip())

        return QVariant()


    def sort(self, column, order = Qt.AscendingOrder):
#        def prepKey(s):
#            return ( convertKeyForNaturalSort(s.upper().replace(u'Ё', u'Е'))
#                     + unichr(0xFFFF)
#                     + s
#                   )
        def prepKey(s):
            return locale.strxfrm(convertKeyForNaturalSort(s))


        keys = { 0: lambda item: prepKey(item.newName),
                 1: lambda item: prepKey(item.comment),
                 2: lambda item: item.size,
                 3: lambda item: item.lastModified,
                 4: lambda item: prepKey(forceString(self._getPersonName(item.authorId))),
                 5: lambda item: prepKey(forceString(self._getPersonName(item.getRespSignerId()))),
                 6: lambda item: prepKey(forceString(self._getPersonName(item.getOrgSignerId()))),
               }
        self.items.sort( key=keys[column],
                         reverse = order != Qt.AscendingOrder
                       )
        self.reset()


    def removeRows(self, row,  count, parent = QModelIndex()):
        self.beginRemoveRows(parent, row, row+count-1)
        try:
            del self.items[row: row+count]
            return True
        except:
            return False
        finally:
            self.endRemoveRows()


    def isNotEmpty(self):
        return bool(self.items)


#    def append(self, item):
#        self.items.append(item)


    def setAttachedFileItemList(self, attachedFileItemList):
        self.items = attachedFileItemList
        self.reset()


    def uploadFiles(self, localFileList):
        for localFile in localFileList:
            fileItem = self.interface.uploadFile(localFile)
            if fileItem:
                self.beginInsertRows(QModelIndex(), len(self.items), len(self.items)+1)
                self.items.append( fileItem )
                self.endInsertRows()


    def uploadBytes(self, fileName, fileBytes, userSignatureBytes, orgSignatureBytes, html=''):
        fileItem = self.interface.uploadBytes(fileName, fileBytes)
        fileItem.setRespSignature(userSignatureBytes, QtGui.qApp.userId, QDateTime().currentDateTime())
        fileItem.setOrgSignature(orgSignatureBytes, QtGui.qApp.userId, QDateTime().currentDateTime())
        if html:
            fileItem.setHtmlTemplate(html)
        self.beginInsertRows(QModelIndex(), 1, len(self.items)+1)
        self.items.append(fileItem)
        self.endInsertRows()


#?
    def saveFiles(self):
        return self.interface.saveFiles(self.items)


    def indexOfItem(self, item):
        return self.items.index(item)


    def touchRow(self, row):
        self.emit(SIGNAL('dataChanged()'),
                  self.index(row, 0),
                  self.index(row, self.columnCount()-1)
                 )


    def renameFile(self, row, newName):
        self.items[row].rename(newName)
        self.touchRow(row)


    def edtComment(self, row, comment):
        self.items[row].edtComment(comment)
        self.touchRow(row)
