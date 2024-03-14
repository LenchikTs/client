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


class CMedpolImportDialog(QtGui.QDialog, Ui_SimpleProgress):
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
            medpolFileName = forceString(self.parent().edtMedpolFileName.text())
            medpolZip = ZipFile(medpolFileName)

            def xmlToDict(xmlName, idField):
                xml = medpolZip.open(xmlName).read()
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
            self.drug = xmlToDict('DRUG.xml', 'DRUG_ID')
            self.progressStep()
            self.drugform = xmlToDict('DRUGFORM.xml', 'DRUGFORM_ID')
            self.progressStep()
            self.drugtype = xmlToDict('DRUGTYPE.xml', 'DRUGTYPE_ID')
            self.progressStep()
            self.eddoza = xmlToDict('EDDOZA.xml', 'EDDOZA_ID') # передавался id из импортируемого файла
            # self.eddoza = xmlToDict('EDDOZA.xml', 'SHORT_TITLE')
            self.progressStep()
            self.formvyp = xmlToDict('FORMVYP.xml', 'FORMVYP_ID')
            self.progressStep()
            self.inn = xmlToDict('INN.xml', 'INN_ID')
            self.progressStep()
            self.manufacturer = xmlToDict('MANUFACTURER.xml', 'MANUFACTURER_ID')
            self.progressStep()

            totalCount = len(self.drug) + len(self.eddoza) + len(self.formvyp)

            self.progressInitialize(u'Импорт справочников', totalCount)

            self.importForms()
            self.importUnits()
            self.importNomenclatures()

            if not self.canceled:
                QtGui.qApp.db.query(u'''
                    SET SQL_SAFE_UPDATES = 0;
                    update rbNomenclature set type_id =
                        case when coalesce(trnCode, '') = ''
                              and coalesce(mnnCode, '') = ''
                              and coalesce(regionalCode, '') = ''
                             then null
                             else 999 end;
                    SET SQL_SAFE_UPDATES = 1;
                ''')
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

    def importForms(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        rbLfForm = db.table('rbLfForm')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, formvyp in self.formvyp.iteritems():
            QtGui.qApp.processEvents()
            if self.canceled:
                break
            record = db.getRecord(rbLfForm, '*', id)
            if record:
                update = True
            else:
                record = rbLfForm.newRecord()
                record.setValue('id', toVariant(id))
                update = False
            record.setValue('code', toVariant(formvyp.get('FED_CODE')))
            record.setValue('name', toVariant(formvyp.get('TITLE')))
            record.setValue('latinname', toVariant(formvyp.get('TITLEENG')))
            record.setValue('codePC', toVariant(formvyp.get('PC_CODE')))
            try:
                if update:
                    db.updateRecord(rbLfForm, record)
                    updated += 1
                else:
                    db.insertRecord(rbLfForm, record)
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
            self.logInfo(u'Справочник FORMVYP.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))


    def importUnits(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        rbUnit = db.table('rbUnit')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, eddoza in self.eddoza.iteritems():
            QtGui.qApp.processEvents()
            if self.canceled:
                break
            record = db.getRecordEx(rbUnit, '*', u"code = '{0}'".format(eddoza.get('TITLE')))
            if record:
                update = True
                record.setValue('federalCode', toVariant(eddoza.get('FED_CODE')))
            else:
                record = rbUnit.newRecord()
                update = False
                record.setValue('code', toVariant(eddoza.get('TITLE')))
                record.setValue('name', toVariant(eddoza.get('TITLE')))
                record.setValue('federalCode', toVariant(eddoza.get('FED_CODE')))
            try:
                if update:
                    db.updateRecord(rbUnit, record)
                    updated += 1
                else:
                    db.insertRecord(rbUnit, record)
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
            self.logInfo(u'Справочник EDDOZA.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))

    def importNomenclatures(self):
        if self.canceled:
            return
        db = QtGui.qApp.db
        rbNomenclature = db.table('rbNomenclature')
        rbUnit = db.table('rbUnit')
        inserted = 0
        updated = 0
        QtGui.qApp.db.transaction()
        self.inTransaction = True
        for id, drug in self.drug.iteritems():
            QtGui.qApp.processEvents()
            if self.canceled:
                break
            record = db.getRecord(rbNomenclature, '*', id)
            if record:
                update = True
            else:
                record = rbNomenclature.newRecord()
                record.setValue('id', toVariant(id))
                update = False

            manufacturer_id = drug.get('MANUFACTURER_ID')
            manufacturer = self.manufacturer.get(manufacturer_id) or {}
            drugtype_id = drug.get('DRUGTYPE_ID')
            drugtype = self.drugtype.get(drugtype_id) or {}
            drugform_id = drug.get('DRUGFORM_ID')
            drugform = self.drugform.get(drugform_id) or {}
            inn_id = drugtype.get('INN_ID')
            inn = self.inn.get(inn_id) or {}
            drugform_drugtype_id = drugform.get('DRUGTYPE_ID')
            drugform_drugtype = self.drugtype.get(drugform_drugtype_id) or {}

            record.setValue('code', toVariant(drug.get('DRUGFORM_ID')))
            record.setValue('regionalCode', toVariant(drug.get('FED_CODE') or ''))
            if 'TITLE' in drug and 'TITLE' in inn:
                name = inn['TITLE'] + ', ' + drug['TITLE']
            else:
                name = drug.get('TITLE')
            record.setValue('name', toVariant(name))
            if 'TITLEENG' in drugform_drugtype and 'QUANTITY' in drug:
                record.setValue('latinTradeName', toVariant(drugform_drugtype['TITLEENG'] + u' №' + drug['QUANTITY']))
            record.setValue('russianTradeName', toVariant(drugform.get('TITLE')))
            if 'TITLEENG' in inn and 'KONCEN_TITLE' in drugtype:
                internationalNonproprietaryName = inn['TITLEENG'] + ' ' + drugtype['KONCEN_TITLE']
            else:
                internationalNonproprietaryName = inn.get('TITLEENG')
            record.setValue('internationalNonproprietaryName', toVariant(internationalNonproprietaryName))
            record.setValue('producer', toVariant(manufacturer.get('TITLE')))
            record.setValue('atc', toVariant(''))
            record.setValue('packSize', toVariant(drugform.get('QUANTITY')))
            if 'DOZA' in drugform:
                doza = round(float(drugform['DOZA']), 5)
                record.setValue('dosageValue', toVariant(doza))
            record.setValue('unit_id', toVariant(drugform.get('EDDOZA_ID')))
            eddozaCode = self.eddoza[drugform.get('EDDOZA_ID')]['TITLE']
            recordUnit = forceRef(db.translate(rbUnit, 'code', eddozaCode, 'id'))
            record.setValue('unit_id', toVariant(recordUnit))
            record.setValue('lfForm_id', toVariant(drugform_drugtype.get('FORMVYP_ID')))
            record.setValue('mnnCode', toVariant(inn.get('FED_CODE') or ''))
            record.setValue('trnCode', toVariant(drugtype.get('FED_CODE') or ''))
            record.setValue('completeness', toVariant(''))
            record.setValue('mnnCodePC', toVariant(inn.get('PC_CODE')))
            record.setValue('trnCodePC', toVariant(drugtype.get('PC_CODE')))

            try:
                if update:
                    db.updateRecord(rbNomenclature, record)
                    updated += 1
                else:
                    db.insertRecord(rbNomenclature, record)
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
            self.logInfo(u'Справочник DRUG.xml загружен: %s, %s' % (countInsertedText, countUpdatedText))

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
