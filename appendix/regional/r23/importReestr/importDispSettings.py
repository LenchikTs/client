# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import sys
import traceback
from zipfile import ZipFile

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from library.Utils import *

from Ui_SimpleProgress import Ui_SimpleProgress


class CDispSettingsImportDialog(QtGui.QDialog, Ui_SimpleProgress):
    startWork = pyqtSignal()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.startWork.connect(self.work, Qt.QueuedConnection)

    def exec_(self):
        self.startWork.emit()
        return QtGui.QDialog.exec_(self)

    def work(self):
        self.inTransaction = False
        self.canceled = False
        self.working = True

        try:
            dispImportFileName = forceString(self.parent().edtDispSettingsFileName.text())
            dispImportZip = ZipFile(dispImportFileName)

            def xmlToDict(xmlName, idField):
                xml = dispImportZip.open(xmlName).read()
                xmlReader = QtCore.QXmlStreamReader(xml)
                rows = {}

                while (not xmlReader.atEnd()):
                    if self.canceled:
                        break
                    xmlReader.readNext()
                    QtGui.qApp.processEvents()

                    if xmlReader.isStartElement() and xmlReader.qualifiedName() == 'z:row':
                        attributes = xmlReader.attributes()
                        attributesDict = {}
                        for attribute in attributes:
                            key = str(attribute.name().toString())
                            value = unicode(attribute.value().toString())
                            attributesDict[key] = value
                        if idField not in attributesDict:
                            self.logInfo(str(len(attributesDict)))
                            self.logInfo(str(attributes))
                            self.logInfo(str(attributes.count()))
                            for attribute in attributes:
                                self.logInfo(str(attribute))
                                self.logInfo(attribute.name().toString())
                            raise Exception(
                                u'У элемента в файле %s не найден ключевой атрибут %s; атрибуты элемента: %s' % (
                                    xmlName, idField, unicode(attributesDict)))
                        id = attributesDict[idField]
                        rows[id] = attributesDict

                if xmlReader.hasError():
                    raise Exception(u'Ошибка при чтении xml файла: ' + unicode(xmlReader.error()))
                return rows

            self.progressInitialize(u'Чтение данных из архива', 7)
            self.dispExamin = xmlToDict('DISP_EXAMIN.xml', 'ID')
            self.progressStep()
            self.dispInspect = xmlToDict('DISP_INSPECT.xml', 'ID')
            self.progressStep()
            self.dispInspectKusl = xmlToDict('DISP_INSPECT_KUSL.xml', 'INSPECT_ID')
            self.progressStep()

            totalCount = len(self.dispExamin) + len(self.dispInspect) + len(self.dispInspectKusl)

            self.progressInitialize(u'Импорт настроек всеобщей диспансеризации', totalCount)

            self.importDispExamin()
            self.importDispInspect()
            self.importDispInspectKusl()

            if not self.canceled:
                # QtGui.qApp.db.query(u'''
                #     SET SQL_SAFE_UPDATES = 0;
                #     update rbNomenclature set type_id =
                #         case when coalesce(trnCode, '') = ''
                #               and coalesce(mnnCode, '') = ''
                #               and coalesce(regionalCode, '') = ''
                #              then null
                #              else 999 end;
                #     SET SQL_SAFE_UPDATES = 1;
                # ''')
                self.progressDone(u'Импорт завершен')

                self.working = False
                self.btnCancel.setText(u'Закрыть')
            else:
                self.working = False
                self.reject()
        except Exception as e:
            self.logError(unicode(e) or repr(e))
            traceback.print_exc()
            if self.inTransaction:
                QtGui.qApp.db.rollback()
            self.working = False
            self.btnCancel.setText(u'Закрыть')


    def importDispExamin(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        tableDispExamin = db.table('disp_examin')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, dispExamin in self.dispExamin.iteritems():
            ID = dispExamin.get('ID')
            if forceBool(ID):
                QtGui.qApp.processEvents()
                if self.canceled:
                    break
                record = db.getRecord(tableDispExamin, '*', toVariant(ID))
                if record:
                    update = True
                else:
                    record = tableDispExamin.newRecord()
                    record.setValue('id', toVariant(ID))
                    update = False

                title = dispExamin.get('TITLE')
                issecondst = dispExamin.get('ISSECONDSTAGE')
                fedcode = dispExamin.get('FEDCODE')
                fedtype = dispExamin.get('FEDTYPE')

                record.setValue('TITLE', forceString(title))
                record.setValue('ISSECONDST', 1 if 'True' in issecondst else 0)
                record.setValue('FEDCODE', forceString(fedcode) if fedcode else None)
                record.setValue('FEDTYPE', forceString(fedtype) if fedtype else None)

                try:
                    if update:
                        db.updateRecord(tableDispExamin, record)
                        updated += 1
                    else:
                        db.insertRecord(tableDispExamin, record)
                        inserted += 1
                except Exception as e:
                    self.logRecord(record)
                    raise e
                self.progressStep(100)
        if self.canceled:
            QtGui.qApp.db.rollback()
            self.inTransaction = False
        else:
            QtGui.qApp.db.commit()
            self.inTransaction = False
            countInsertedText = agreeNumberAndWord(inserted, (
                u'добавлена %d запись', u'добавлено %d записи', u'добавлено %d записей')) % inserted
            countUpdatedText = agreeNumberAndWord(updated, (
                u'обновлена %d запись', u'обновлено %d записи', u'обновлено %d записей')) % updated
            self.logInfo(u'Справочник DISP_EXAMIN.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))


    def importDispInspect(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        tableDispInspect = db.table('disp_inspect')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, dispInspect in self.dispInspect.iteritems():
            QtGui.qApp.processEvents()
            if self.canceled:
                break
            record = db.getRecord(tableDispInspect, '*', id)
            if record:
                update = True
            else:
                record = tableDispInspect.newRecord()
                record.setValue('ID', toVariant(id))
                update = False

            examinId = dispInspect.get('EXAMIN_ID')
            age = dispInspect.get('AGE')
            sex = dispInspect.get('SEX')
            kusl = dispInspect.get('KUSL')
            isProfOsm = dispInspect.get('ISPROFOSM')
            includeInCalc = dispInspect.get('INCLUDEINCALC')

            record.setValue('EXAMIN_ID', forceInt(examinId))
            record.setValue('AGE', forceInt(age))
            record.setValue('SEX', 1 if 'True' in sex else 2)
            record.setValue('KUSL', forceString(kusl) if kusl else None)
            record.setValue('IsProfOsm', 1 if 'True' in isProfOsm else 0)
            record.setValue('IncludeInCalc', 1 if 'True' in includeInCalc else 0)

            try:
                if update:
                    db.updateRecord(tableDispInspect, record)
                    updated += 1
                else:
                    db.insertRecord(tableDispInspect, record)
                    inserted += 1
            except Exception as e:
                self.logRecord(record)
                raise e
            self.progressStep(100)
        if self.canceled:
            QtGui.qApp.db.rollback()
            self.inTransaction = False
        else:
            QtGui.qApp.db.commit()
            self.inTransaction = False
            countInsertedText = agreeNumberAndWord(inserted, (
                u'добавлена %d запись', u'добавлено %d записи', u'добавлено %d записей')) % inserted
            countUpdatedText = agreeNumberAndWord(updated, (
                u'обновлена %d запись', u'обновлено %d записи', u'обновлено %d записей')) % updated
            self.logInfo(u'Справочник DISP_INSPECT.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))


    def importDispInspectKusl(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        tableDispInspectKusl = db.table('disp_inspect_kusl')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, dispInspectKusl in self.dispInspectKusl.iteritems():
            QtGui.qApp.processEvents()
            if self.canceled:
                break
            inspectId = dispInspectKusl.get('INSPECT_ID')
            record = db.getRecordEx(tableDispInspectKusl, '*', tableDispInspectKusl['inspect_id'].eq(inspectId))
            if record:
                update = True
            else:
                record = tableDispInspectKusl.newRecord()
                record.setValue('INSPECT_ID', toVariant(inspectId))
                update = False

            inspectId = dispInspectKusl.get('INSPECT_ID')
            kusl = dispInspectKusl.get('KUSL')
            isuse = dispInspectKusl.get('ISUSE')

            record.setValue('INSPECT_ID', forceInt(inspectId))
            record.setValue('KUSL', forceString(kusl) if kusl else None)
            record.setValue('ISUSE', 1 if 'True' in isuse else 0)

            try:
                if update:
                    db.updateRecord(tableDispInspectKusl, record)
                    updated += 1
                else:
                    db.insertRecord(tableDispInspectKusl, record)
                    inserted += 1
            except Exception as e:
                self.logRecord(record)
                raise e
            self.progressStep(100)
        if self.canceled:
            QtGui.qApp.db.rollback()
            self.inTransaction = False
        else:
            QtGui.qApp.db.commit()
            self.inTransaction = False
            countInsertedText = agreeNumberAndWord(inserted, (
                u'добавлена %d запись', u'добавлено %d записи', u'добавлено %d записей')) % inserted
            countUpdatedText = agreeNumberAndWord(updated, (
                u'обновлена %d запись', u'обновлено %d записи', u'обновлено %d записей')) % updated
            self.logInfo(u'Справочник DISP_INSPECT_KUSL.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))


    def progressInitialize(self, caption, maxCount=1):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(maxCount)
        self.prbProgress.setValue(0)
        self.lblElapsed.setVisible(True)
        self.lblElapsed.setText(u'Текущая операция: ??? зап/с, окончание в ??:??:??')
        self.time = QTime()
        self.time.start()
        self.totalTime = QTime()
        self.totalTime.start()
        self.startPos = 0
        self.oldSpeed = 0

    def progressStep(self, minimumDifference=1):
        self.prbProgress.setValue(self.prbProgress.value() + 1)

        elapsed = self.time.elapsed()
        difference = self.prbProgress.value() - self.startPos
        if elapsed != 0 and (difference >= minimumDifference):
            self.startPos = self.prbProgress.value()
            self.oldSpeed = difference * 1000 / elapsed
            newSpeed = (self.oldSpeed + difference * 1000 / elapsed) / 2
            if newSpeed != 0:
                totalElapsed = self.totalTime.elapsed()
                partRemaining = float(self.prbProgress.maximum()) / self.prbProgress.value() - 1

                finishTime = QTime.currentTime().addSecs(totalElapsed * partRemaining / 1000)
                self.lblElapsed.setText(
                    u'Текущая операция: %01.f зап/с, окончание в %s' % (newSpeed, finishTime.toString('hh:mm:ss')))
                self.time.restart()

    def progressDone(self, caption):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(1)
        self.prbProgress.setValue(1)
        self.lblElapsed.setVisible(False)

    def logInfo(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(text)
        else:
            for str in text:
                self.txtLog.append(str)
        self.txtLog.append('')

    def logError(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text)
        else:
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text[0])
            for str in text[1:]:
                self.txtLog.append(str)
        self.txtLog.append('')

    def logRecord(self, record):
        for i in xrange(0, record.count()):
            self.txtLog.append("%s = %s" % (unicode(record.fieldName(i)), unicode(record.value(i).toString())))
        self.txtLog.append('')

    @pyqtSignature("")
    def on_btnCancel_clicked(self):
        if self.working:
            self.canceled = True
        else:
            self.accept()
