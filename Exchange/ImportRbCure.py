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
from PyQt4.QtCore     import QDate, QFile
from Exchange.Cimport import CXMLimport
from library.Utils    import forceStringEx, forceInt, toVariant

from Ui_ImportRbComplain import Ui_ImportRbComplain


__all__ = ('CImportRbCureType', 'CImportRbCureMethod')


class CImportRbCureBase(QtGui.QDialog, CXMLimport, Ui_ImportRbComplain):
    def __init__(self, tableName, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self, self.logBrowser)
        self.tableName = tableName
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.itemsAdded = 0
        self.itemsPassed = 0
        self.showFullLog = False


    def codeXmlField(self):
        raise NotImplementedError()


    def nameXmlField(self):
        raise NotImplementedError()


    def endDateXmlField(self):
        raise NotImplementedError()


    def err2log(self, e):
        codeField = self.codeXmlField()
        self.logBrowser.append(u'запись %d (%s="%s"): %s' % (
            self.n, codeField, self.row[codeField], e))


    def startImport(self):
        self.progressBar.setFormat('%p%')
        fileName = forceStringEx(self.edtFileName.text())
        inFile = QFile(fileName)
        self.showFullLog = self.chkFullLog.isChecked()
        self.logBrowser.clear()

        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт из XML',
                                      u'Ошибка открытия файла для чтения %s:\n%s.' \
                                      % (fileName, inFile.errorString()))
        else:
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


    def readFile(self, device):
        self.setDevice(device)
        db = QtGui.qApp.db

        # узнать максимальное кол-во символов в поле name
        # нужно для сравнения строк, если они больше допустимой длины
        query = db.query(u"""SELECT CHARACTER_MAXIMUM_LENGTH
                             FROM information_schema.columns
                             WHERE `table_schema` = DATABASE()
                               AND `table_name` = '%s'
                               AND `column_name` = 'name' """ % self.tableName)
        query.first()
        maxNameChars = forceInt(query.value(0))

        codeField = self.codeXmlField()
        nameField = self.nameXmlField()
        endDateField = self.endDateXmlField()
        table = db.table(self.tableName)
        codeNameCache = {}
        while not self.atEnd():
            self.readNext()
            if self.isStartElement() and self.name() == 'zap':
                self.n += 1
                self.row = self.readGroup('zap', (codeField, nameField, endDateField), silent=True)
                code = self.row[codeField]
                name = self.row[nameField][:maxNameChars]
                endDate = self.row[endDateField]
                date = QDate.fromString(endDate, 'dd.MM.yyyy') if endDate else None

                if date and date < QDate.currentDate():
                    if self.showFullLog:
                        self.err2log(u'дата окончания (%s) меньше текущей, пропущено' % endDate)
                    self.itemsPassed += 1
                    continue

                itemId = self.lookupIdByCodeName(code, name, table, codeNameCache)
                if itemId:
                    if self.showFullLog:
                        self.err2log(u'запись уже существует (id=%d), пропущено' % itemId)
                    self.itemsPassed += 1
                else:
                    itemId = self.insertNewRecord(code, name, date)
                    self.err2log(u'запись добавлена (id=%d)' % itemId)
                    self.itemsAdded += 1

            if self.hasError():
                return False
        return True


    def insertNewRecord(self, code, name, endDate):
        db = QtGui.qApp.db
        record = db.record(self.tableName)
        record.setValue('code',            toVariant(code))
        record.setValue('regionalCode',    toVariant(code))
        record.setValue('name',            toVariant(name))
        record.setValue('endDate',         toVariant(endDate))
        record.setValue('modifyPreson_id', toVariant(QtGui.qApp.userId))
        record.setValue('createPreson_id', toVariant(QtGui.qApp.userId))
        return db.insertRecord(self.tableName, record)



class CImportRbCureType(CImportRbCureBase):
    def __init__(self, parent=None):
        CImportRbCureBase.__init__(self, 'rbCureType', parent)
        self.setWindowTitle(u'Импорт справочника `Виды лечения`')

    def codeXmlField(self):
        return 'IDHVID'

    def nameXmlField(self):
        return 'HVIDNAME'

    def endDateXmlField(self):
        return 'DATEEND'



class CImportRbCureMethod(CImportRbCureBase):
    def __init__(self, parent=None):
        CImportRbCureBase.__init__(self, 'rbCureMethod', parent)
        self.setWindowTitle(u'Импорт справочника `Методы лечения`')

    def codeXmlField(self):
        return 'IDHM'

    def nameXmlField(self):
        return 'HMNAME'

    def endDateXmlField(self):
        return 'DATEEND'

