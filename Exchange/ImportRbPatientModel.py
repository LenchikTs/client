# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4            import QtGui
from PyQt4.QtCore     import QDate, QFile, QDir, pyqtSignature
from Exchange.Cimport import CXMLimport
from library.Utils    import forceStringEx, forceInt, toVariant

from Ui_ImportRbPatientModel import Ui_ImportRbPatientModel


class CImportRbPatientModel(QtGui.QDialog, CXMLimport, Ui_ImportRbPatientModel):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self, self.logBrowser)
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.itemsAdded = 0
        self.itemsPassed = 0
        self.showFullLog = False
        self.rbCureMap = {}


    def checkName(self):
        self.btnImport.setEnabled(self.edtFileName.text() != '' and self.edtFileNameHelp.text() != '')


    @pyqtSignature('')
    def on_btnSelectFileHelp_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileNameHelp.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            self.edtFileNameHelp.setText(QDir.toNativeSeparators(fileName))
            self.checkName()


    def err2log(self, e):
        if self.row:
            self.logBrowser.append(u'запись %d (%s="%s"): %s' % (self.n, 'IDMPAC', self.row['IDMPAC'], e))


    def startImport(self):
        self.progressBar.setFormat('%p%')
        fileName = forceStringEx(self.edtFileName.text())
        helpFileName = forceStringEx(self.edtFileNameHelp.text())
        inFile = QFile(fileName)
        helpFile = QFile(helpFileName)
        self.showFullLog = self.chkFullLog.isChecked()
        self.logBrowser.clear()

        if not helpFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт из XML',
                                      u'Ошибка открытия файла для чтения %s:\n%s.' \
                                      % (helpFileName, helpFile.errorString()))
            return
        else:
            self.progressBar.reset()
            self.progressBar.setValue(0)
            self.progressBar.setFormat(u'%v байт (методы лечения)')
            self.statusLabel.setText("")
            self.progressBar.setMaximum(max(inFile.size(), 1))
            self.btnImport.setEnabled(False)
            if not self.mapHelpFile(helpFile):
                if self.abort:
                    self.err2log(u'! Прервано пользователем.')
                else:
                    self.err2log(u'! Ошибка: файл %s, %s' % (helpFileName, self.errorString()))
                return


        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт из XML',
                                      u'Ошибка открытия файла для чтения %s:\n%s.' \
                                      % (fileName, inFile.errorString()))
        else:
            self._xmlReader.clear()
            self.n = 0
            self.itemsAdded = 0
            self.itemsPassed = 0
            self.progressBar.reset()
            self.progressBar.setValue(0)
            self.progressBar.setFormat(u'%v байт')
            self.statusLabel.setText("")
            self.progressBar.setMaximum(max(inFile.size(), 1))
            self.btnImport.setEnabled(False)
            if not self.readFile(inFile):
                if self.abort:
                    self.err2log(u'! Прервано пользователем.')
                else:
                    self.err2log(u'! Ошибка: файл %s, %s' % (fileName, self.errorString()))
            self.statusLabel.setText(u'Импорт завершен: %d найдено; %d добавлено; %d пропущено' % (self.n, self.itemsAdded, self.itemsPassed))


    def mapHelpFile(self, device):
        db = QtGui.qApp.db
        self.rbCureMap = {}
        self.setDevice(device)
        while not self.atEnd():
            self.readNext()
            if self.isStartElement() and self.name() == 'zap':
                row = self.readGroup('zap', ('IDHM', 'DIAG', 'HVID', 'IDMODP'), silent=True)
                cureTypeCode = row['HVID']
                cureTypeId = forceInt(db.translate('rbCureType', 'code', cureTypeCode, 'id'))
                cureMethodCode = row['IDHM']
                cureMethodId = forceInt(db.translate('rbCureMethod', 'code', cureMethodCode, 'id'))
                modelId = row.get('IDMODP', '')
                self.rbCureMap.setdefault(modelId, [])
                self.rbCureMap[modelId].append({'MKB': row['DIAG'],
                                                'cureTypeId': cureTypeId,
                                                'cureMethodId': cureMethodId,
                                               })
            if self.hasError():
                return False
        return True


    def readFile(self, device):
        self.setDevice(device)
        db = QtGui.qApp.db

        # узнать максимальное кол-во символов в поле name
        # нужно для сравнения строк, если они больше допустимой длины
        query = db.query(u"""SELECT CHARACTER_MAXIMUM_LENGTH
                             FROM information_schema.columns
                             WHERE `table_schema` = DATABASE()
                               AND `table_name` = 'rbPatientModel'
                               AND `column_name` = 'name' """)
        query.first()
        maxNameChars = forceInt(query.value(0))
        codeNameCache = {}
        itemCache = {}
        table = db.table('rbPatientModel')
        while not self.atEnd():
            self.readNext()
            if self.isStartElement() and self.name() == 'zap':
                self.n += 1
                self.row = self.readGroup('zap', ('IDMPAC', 'MPACNAME', 'DATEEND'), silent=True)
                code = self.row['IDMPAC']
                name = self.row['MPACNAME'][:maxNameChars]
                endDate = self.row['DATEEND']
                date = QDate.fromString(endDate, 'dd.MM.yyyy') if endDate else None

                if date and date < QDate.currentDate():
                    if self.showFullLog:
                        self.err2log(u'дата окончания (%s) меньше текущей, пропущено' % endDate)
                    self.itemsPassed += 1
                    continue

                cureDataList = self.rbCureMap.get(code, [])
                itemId = self.lookupIdByCodeName(code, name, table, codeNameCache)
                if itemId:
                    subItemsAdded = 0
                    for cureData in cureDataList:
                        cureTypeId = cureData['cureTypeId']
                        cureMethodId = cureData['cureMethodId']
                        if not self.lookupItemId(itemId, cureTypeId, cureMethodId, itemCache):
                            self.insertNewSlaveRecord(itemId, cureTypeId, cureMethodId)
                            subItemsAdded += 1
                    if subItemsAdded == 0:
                        if self.showFullLog:
                            self.err2log(u'запись уже существует (id=%d), пропущено' % itemId)
                        self.itemsPassed += 1
                else:
                    MKB = cureDataList[0]['MKB'] if cureDataList else None
                    itemId = self.insertNewRecord(code, name, date, MKB)
                    for cureData in cureDataList:
                        self.insertNewSlaveRecord(itemId, cureData['cureTypeId'], cureData['cureMethodId'])
                    self.err2log(u'запись добавлена (id=%d)' % itemId)
                    self.itemsAdded += 1

            if self.hasError():
                return False
        return True


    def lookupItemId(self, masterId, cureTypeId, cureMethodId, cache):
        if not masterId:
            return None
        key = (masterId, cureTypeId, cureMethodId)
        itemId = cache.get(key, None)
        if itemId:
            return itemId
        db = QtGui.qApp.db
        table = db.table('rbPatientModel_Item')
        cond = [ table['master_id'].eq(masterId) ]
        if cureTypeId:
            cond.append(table['cureType_id'].eq(cureTypeId))
        if cureMethodId:
            cond.append(table['cureMethod_id'].eq(cureMethodId))
        record = db.getRecordEx('rbPatientModel_Item', 'id', cond)
        if record:
            id = forceInt(record.value('id'))
            cache[key] = id
            return id
        return None


    def insertNewRecord(self, code, name, endDate, MKB):
        db = QtGui.qApp.db
        record = db.record('rbPatientModel')
        record.setValue('code',            toVariant(code))
        record.setValue('regionalCode',    toVariant(code))
        record.setValue('name',            toVariant(name))
        record.setValue('endDate',         toVariant(endDate))
        record.setValue('MKB',             toVariant(MKB))
        record.setValue('modifyPreson_id', toVariant(QtGui.qApp.userId))
        record.setValue('createPreson_id', toVariant(QtGui.qApp.userId))
        return db.insertRecord('rbPatientModel', record)


    def insertNewSlaveRecord(self, masterId, cureTypeId, cureMethodId):
        if not masterId:
            return None
        db = QtGui.qApp.db
        record = db.record('rbPatientModel_Item')
        record.setValue('master_id', toVariant(masterId))
        if cureTypeId:
            record.setValue('cureType_id', toVariant(cureTypeId))
        if cureMethodId:
            record.setValue('cureMethod_id', toVariant(cureMethodId))
        return db.insertRecord('rbPatientModel_Item', record)

