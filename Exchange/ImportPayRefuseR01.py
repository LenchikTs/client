# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Импорт реестров счетов, Республика Адыгея"""
import os
from zipfile import is_zipfile, ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, QString, QDir, pyqtSignature, QRegExp, Qt

from library.Utils import forceString, toVariant
from Exchange.Cimport import CXMLimport, Cimport

from Exchange.Ui_ImportPayRefuseR01 import Ui_Dialog


def ImportPayRefuseR01Native(widget):
    u"""Создает диалог импорта флк/возвратов реестров счетов"""
    dlg = CImportPayRefuseR01Native()
    prefs = QtGui.qApp.preferences.appPrefs
    dlg.edtFileName.setText(forceString(prefs.get('ImportPayRefuseR01FileName', '')))

    dlg.load_zip(dlg.edtFileName.text())
    dlg.exec_()
    prefs['ImportPayRefuseR01FileName'] = toVariant(dlg.edtFileName.text())


class CImportPayRefuseR01Native(QtGui.QDialog, Ui_Dialog, CXMLimport):

    @pyqtSignature('')
    def on_btnImport_clicked(self): Cimport.on_btnImport_clicked(self)

    @pyqtSignature('')
    def on_btnClose_clicked(self): Cimport.on_btnClose_clicked(self)

    zapFields = ('N_ZAP', 'PR_NOV')
    schetFields = ('CODE', 'CODE_MO', 'YEAR', 'MONTH')

    pacFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'SMO_OGRN', 'SMO_OK', 'SMO', 'NOVOR')
    sluchFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'DATE_1', 'DATE_2', 'CODE_MES1', 'ED_COL')


    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        CXMLimport.__init__(self)
        self.progressBar.setFormat('%p%')
        self.policyFileNames = []
        self.recordList = []
        self.idCases = []
        self.checkName()
        self.schetDict = {}
        self.aborted = False

        self.nProcessed = 0
        self.nUpdated = 0
        self.table = self.db.table('soc_policyIdentification')
        self.tempDirList = []


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, u'Укажите архив с данными', self.edtFileName.text(), u'Архивы(*.7z *.zip)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.checkName()
            self.load_zip(self.edtFileName.text())


    def load_zip(self, archiveName):
        if is_zipfile(forceString(archiveName)):
            self.btnImport.setEnabled(True)
        else:
            self.err2log(u'Выбранный файл отсутствует или не является архивом')
            self.btnImport.setEnabled(False)


    def startImport(self):
        archiveName = forceString(self.edtFileName.text())
        try:
            rx_arch = QRegExp('HI[0-9]{8}_[0-9]*.zip$', Qt.CaseInsensitive)
            if not rx_arch.exactMatch(os.path.basename(archiveName)):
                self.err2log(u'Указанный файл не является архивом ФЛК')
                return

            flcRE = QRegExp('HI[0-9]{8}_[0-9]*.xml$', Qt.CaseInsensitive)
            archive = ZipFile(archiveName, 'r')
            names = archive.namelist()
            tmpDir = QtGui.qApp.getTmpDir('flc')
            self.tempDirList.append(tmpDir)
            self.policyFileNames = []

            for name in names:
                if flcRE.exactMatch(name):
                    self.policyFileNames.append(archive.extract(name, tmpDir))
            archive.close()
            if not any([self.policyFileNames]):
                self.err2log(u'В архиве отсутствуют протоколы ФЛК')
                return
        except Exception, e:
            self.err2log(u'Ошибка распаковки архива: Невозможно распаковать архив\n' + unicode(e))
            return

        # импорт протоколов ФЛК
        self.db.deleteRecordSimple(self.table, '')
        for fileName in self.policyFileNames:
            self.processFile(fileName, fileType='policy')
        if self.policyFileNames:
            self.log.append(u'Обновление полисных данных...')
            QtGui.qApp.processEvents()
            QtGui.qApp.db.query('CALL updateClientPolicyByFlc01();')
            self.log.append(u'Обновление полисных данных завершено!')


    def processFile(self, fileName, fileType):
        baseDir, name = os.path.split(forceString(fileName))
        self.nProcessed = 0
        self.nUpdated = 0
        if not self.readFile(fileName, fileType):
            self.log.append(u'Ошибка импорта данных файла %s' % name)
        else:
            self.log.append(u'Импорт файла %s завершен успешно: %d обработано' % (name, self.nProcessed))
        QtGui.qApp.processEvents()


    def readFile(self, fileName, fileType):
        u"""Разбирает указанный XML файл, отправляет данные в БД"""
        if not fileName:
            return False

        inFile = QFile(fileName)

        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт данных из XML',
                                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                                      .arg(fileName)
                                      .arg(inFile.errorString()))
            return False

        self.progressBar.setFormat(u'%v байт')
        self.progressBar.setMaximum(max(inFile.size(), 1))
        self.setDevice(inFile)
        self.recordList = []
        table = self.table
        if self.readHeader(fileType):
            if fileType in ['policy']:
                self.schet = self.readSchet()

            for item in self.readData(fileType):
                self.progressBar.setValue(inFile.pos())
                QtGui.qApp.processEvents()
                if item:
                    self.processItem(item, fileType)
                if self.aborted:
                    break

            if self.recordList:
                self.insertRecordList(table, self.recordList)
                self.recordList = []

        if not (self.hasError() or self.aborted):
            self.err2log(u'Готово')
            return True
        else:
            self.err2log(u'Прервано')
            if self.aborted:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл %s, %s' % (fileName, self.errorString()))
            return False


    def readHeader(self, fileType):
        u"""Разбирает заголовок"""
        while not self.atEnd():
            self.readNext()
            if self.name() == 'ZGLV' and self.isEndElement():
                return True
            continue
        return False


    def readSchet(self):
        QtGui.qApp.processEvents()
        if self.name() != 'SCHET':
            self.readNext()
        if self.name() != 'SCHET':
            self.readNext()
        if self.isStartElement():
            if self.name() == 'SCHET':
                return self.readGroupEx('SCHET', self.schetFields, silent=True)
            else:
                self.readUnknownElement()
        if self.hasError() or self.aborted:
            return


    def readData(self, fileType):
        while not self.atEnd():
            QtGui.qApp.processEvents()
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'ZAP':
                    yield self.readGroupEx('ZAP', self.zapFields, silent=True, subGroupDict={'PACIENT': {'fields': self.pacFields},
                                                                                             'SLUCH': {'fields': self.sluchFields}})
                else:
                    self.readUnknownElement()
            if self.hasError() or self.aborted:
                break


    def processItem(self, item, fileType):
        def fillRecord(table, pacItem, sluchItem):
            newRecord = table.newRecord()
            newRecord.setValue('ID_PAC', pacItem['ID_PAC'])
            newRecord.setValue('VPOLIS', pacItem.get('VPOLIS'))
            newRecord.setValue('SPOLIS', pacItem.get('SPOLIS'))
            newRecord.setValue('NPOLIS', pacItem.get('NPOLIS'))
            newRecord.setValue('SMO_OGRN', pacItem.get('SMO_OGRN'))
            newRecord.setValue('SMO_OK', pacItem.get('SMO_OK'))
            newRecord.setValue('SMO', pacItem.get('SMO'))
            newRecord.setValue('NOVOR', pacItem.get('NOVOR'))
            newRecord.setValue('IDCASE', sluchItem['IDCASE'])
            newRecord.setValue('USL_OK', sluchItem['USL_OK'])
            newRecord.setValue('VIDPOM', sluchItem['VIDPOM'])
            newRecord.setValue('DATE_1', sluchItem['DATE_1'])
            newRecord.setValue('DATE_2', sluchItem['DATE_2'])
            newRecord.setValue('CODE_MES1', sluchItem['CODE_MES1'])
            newRecord.setValue('ED_COL', sluchItem['ED_COL'])
            return newRecord

        if isinstance(item['SLUCH'], list):
            for sl in item['SLUCH']:
                record = fillRecord(self.table, item['PACIENT'], sl)
                self.recordList.append(record)
                if len(self.recordList) == 1000:
                    self.insertRecordList(self.table, self.recordList)
                    self.recordList = []
        else:
            record = fillRecord(self.table, item['PACIENT'], item['SLUCH'])
            self.recordList.append(record)
            if len(self.recordList) == 1000:
                self.insertRecordList(self.table, self.recordList)
                self.recordList = []
        self.nProcessed += 1


    def insertRecordList(self, table, recordList):
        self.db.checkdb()
        table = self.db.forceTable(table)
        fields = []
        valuesList = []
        for record in recordList:
            fieldsCount = record.count()
            values = []
            for i in range(fieldsCount):
                if len(fields) < fieldsCount:
                    fields.append(self.db.escapeFieldName(record.fieldName(i)))
                values.append(self.db.formatValue(record.field(i)))
            valuesList.append('(' + (', '.join(values)) + ')')
        stmt = ('INSERT INTO ' + table.name() +
                '(' + (', '.join(fields)) + ') ' +
                'VALUES ' + ', '.join(valuesList))
        query = self.db.query(stmt)
        return query


    def closeEvent(self, event):
        for _dir in self.tempDirList:
            QtGui.qApp.removeTmpDir(_dir)
        event.accept()
