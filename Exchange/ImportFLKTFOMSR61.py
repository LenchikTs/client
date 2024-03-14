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
u"""Импорт реестров счетов, Ростовская область"""
import os
import shutil
from zipfile import is_zipfile, ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import QFile, QString, QDir, pyqtSignature, QRegExp, Qt, QDate

from Accounting.Utils import updateAccount
from Exchange.Utils import compressFileInZip, getChecksum
from Orgs.Utils import getOrganisationInfo, COrgInfo
from library import xlrd
from library.AmountToWords import amountToWords
from library.PrintInfo import CInfoContext
from library.Utils import forceString, toVariant, forceBool, forceInt, forceDouble, forceRef, forceStringEx, \
    lastMonthDay, forceDate, formatDate
from Exchange.Cimport import CXMLimport

from Exchange.Ui_ImportPayRefuseR61TFOMS import Ui_Dialog
from library.xlwt import easyxf


def importFLKTFOMSR61Native(widget):
    u"""Создает диалог импорта флк/мэк/повторного мэк"""
    dlg = CImportFLK()
    prefs = QtGui.qApp.preferences.appPrefs
    dlg.edtFileName.setText(forceString(prefs.get('importFLKTFOMSR61FileName', '')))
    dlg.chkUpdatePolicy.setChecked(forceBool(prefs.get('importFLKTFOMSR61UpdatePolicy', '')))
    dlg.chkUpdateAccounts.setChecked(forceBool(prefs.get('importFLKTFOMSR61UpdateAccounts', '')))
    dlg.edtOutputDir.setText(forceString(prefs.get('importFLKTFOMSR61OutputDir', '')))

    dlg.lblOutputDir.setVisible(dlg.chkUpdateAccounts.isChecked())
    dlg.edtOutputDir.setVisible(dlg.chkUpdateAccounts.isChecked())
    dlg.btnSelectDir.setVisible(dlg.chkUpdateAccounts.isChecked())

    dlg.load_zip(dlg.edtFileName.text())
    dlg.exec_()
    prefs['importFLKTFOMSR61FileName'] = toVariant(dlg.edtFileName.text())
    prefs['importFLKTFOMSR61UpdatePolicy'] = toVariant(dlg.chkUpdatePolicy.isChecked())
    prefs['importFLKTFOMSR61UpdateAccounts'] = toVariant(dlg.chkUpdateAccounts.isChecked())
    prefs['importFLKTFOMSR61OutputDir'] = toVariant(dlg.edtOutputDir.text())


class CImportFLK(QtGui.QDialog, Ui_Dialog, CXMLimport):

    prFields = ('OSHIB', 'IM_POL', 'BAS_EL', 'N_ZAP', 'NSCHET', 'KODLPU', 'NSVOD', 'ID_PAC', 'IDCASE', 'IDSERV', 'COMMENT')

    zapFields = ('N_ZAP', 'PR_NOV')
    schetFields = ('CODE', 'CODE_MO', 'YEAR', 'MONTH', 'NSCHET', 'DSCHET', 'PLAT', 'SUMMAV', 'SUMMA_SMP', 'SUMMA_PF',
                   'SUMMA_FAP', 'COMENTS', 'SUMMAP', 'SANK_MEK', 'SANK_MEE', 'SANK_EKMP')
    pacFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ENP', 'SMO', 'SMO_OGRN', 'SMO_OK', 'SMO_NAM', 'NOVOR',
                 'VNOV_D', 'STAT_Z', 'STAT_L', 'INV', 'DATA_INV', 'MSE', 'ENP_ID', 'SMO_OGRN_ID', 'SMO_OK_ID',
                 'SMO_NAM_ID', 'SMO_ID', 'VPOLIS_ID', 'SPOLIS_ID', 'NPOLIS_ID', 'KPACI')
    sluchFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'PODR', 'LPU', 'PROFIL', 'DET', 'NHISTORY', 'DATE_1',
                   'DATE_2', 'DS1', 'C_ZAB', 'VNOV_M', 'RSLT', 'ISHOD', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'IDSP', 'SUMV',
                   'OPLATA', 'SUMP', 'NSVOD', 'KODLPU', 'PRNES', 'KD_Z', 'PCHAST', 'PR_MO', 'COMENTSL', 'DS_ONK')
    sankFields = ('S_CODE', 'S_SUM', 'S_TIP', 'SL_ID', 'S_OSN', 'DATE_ACT', 'NUM_ACT', 'CODE_EXP', 'S_IST', 'S_COM')
    sankSubGroup = {
        'SANK': {'fields': sankFields},
    }

    # Повторный МЭК
    aktFields = ('NAKT', 'DATE_AKT', 'YEAR', 'MONTH', 'SUMAKT')
    aktSluchFields = ('IDCASE', 'USL_OK', 'KOD_LPU', 'SUMP')
    aktSankFields = ('S_CODE', 'S_SUM', 'S_TIP', 'SL_ID', 'S_OSN', 'S_IST', 'S_COM')
    aktSankSubGroup = {
        'SANK': {'fields': aktSankFields},
    }


    prGroupName = 'PR'
    flkpGroupName = 'FLK_P'
    flkpFields = ('FNAME', 'FNAME_I')


    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        CXMLimport.__init__(self)
        self.progressBar.setFormat('%p%')
        self.flcFileNames = []
        self.policyFileNames = []
        self.errorFileNames = []
        self.reestrFileNames = []
        self.MekFileNames = []
        self.ReMekFileNames = []
        self.recordList = []
        self.idCases = []
        self.refuseTypeIdCache = {}
        self.checkName()
        self.schetDict = {}
        self.aborted = False

        self.nProcessed = 0
        self.nUpdated = 0
        self.table = self.db.table('ro_flc')
        self.tableFinal = self.db.table('ro_finalFLC')
        self.tempDirList = []


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, u'Укажите архив с данными', self.edtFileName.text(), u'Архивы(*.7z *.zip)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.checkName()
            self.load_zip(self.edtFileName.text())


    @pyqtSignature('')
    def on_btnSelectDir_clicked(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, u'Выберите директорий для сохранения архивов реестров счетов',
                                                      forceStringEx(self.edtOutputDir.text()), QtGui.QFileDialog.ShowDirsOnly)
        if forceString(path):
            self.edtOutputDir.setText(QDir.toNativeSeparators(path))


    def load_zip(self, archiveName):
        if is_zipfile(forceString(archiveName)):
            self.btnImport.setEnabled(True)
        else:
            self.err2log(u'Выбранный файл отсутствует или не является архивом')
            self.btnImport.setEnabled(False)


    def processFile(self, fileName, fileType):
        baseDir, name = os.path.split(forceString(fileName))
        self.nProcessed = 0
        self.nUpdated = 0
        if not self.readFile(fileName, fileType):
            self.log.append(u'Ошибка импорта данных файла %s' % name)
        else:
            self.log.append(u'Импорт файла %s завершен успешно: %d обработано' % (name, self.nProcessed))
        QtGui.qApp.processEvents()


    def startImport(self):
        archiveName = forceString(self.edtFileName.text())
        try:
            if self.tabRegime.currentWidget() == self.tabFLC:
                if self.chkUpdateAccounts.isChecked():
                    if not QDir().exists(forceString(self.edtOutputDir.text())):
                        self.err2log(u'Не указана директория для сохранения реестров счетов!')
                        return
                archive = ZipFile(archiveName, 'r')
                names = archive.namelist()
                archNames = []
                self.flcFileNames = []
                self.errorFileNames = []
                self.policyFileNames = []
                self.reestrFileNames = []
                self.schetDict = {}
                rx_arch = QRegExp('[0-9]{7}_.*.zip$', Qt.CaseInsensitive)
                flcRE = QRegExp('[LH]M.*.flc.xml$', Qt.CaseInsensitive)
                rx = QRegExp('HM.*.xml$', Qt.CaseInsensitive)
                tmpDir = QtGui.qApp.getTmpDir('flc')
                self.tempDirList.append(tmpDir)
                for name in names:
                    if rx_arch.exactMatch(name):
                        archName = archive.extract(name, tmpDir)
                        archNames.append(archName)
                        if self.chkUpdateAccounts.isChecked() and os.path.basename(name)[8:-4] not in ['err', '99']:
                            self.reestrFileNames.append(archName)
                    elif flcRE.exactMatch(name):
                        self.flcFileNames.append(archive.extract(name, tmpDir))
                for archName in archNames:
                    arch_tmp = ZipFile(forceString(archName), 'r')
                    names = arch_tmp.namelist()
                    tmpDir = QtGui.qApp.getTmpDir(str(os.path.basename(archName)[:-4]))
                    self.tempDirList.append(tmpDir)
                    for name in names:
                        if rx.exactMatch(name):
                            if os.path.basename(archName)[-8:-4] == '_err':
                                self.errorFileNames.append(arch_tmp.extract(name, tmpDir))
                            else:
                                self.policyFileNames.append(arch_tmp.extract(name, tmpDir))
                    arch_tmp.close()
                archive.close()
                if not any([self.flcFileNames, self.errorFileNames, self.policyFileNames]):
                    self.err2log(u'В архиве отсутствуют протоколы ФЛК')
                    return
            elif self.tabRegime.currentWidget() == self.tabMEK:
                archive = ZipFile(archiveName, 'r')
                names = archive.namelist()
                self.MekFileNames = []
                rx_arch = QRegExp('[0-9]{7}_[0-9]{2}.zip$', Qt.CaseInsensitive)
                rx = QRegExp('HS.*.xml$', Qt.CaseInsensitive)
                tmpDir = QtGui.qApp.getTmpDir('mek')
                tmpDir2 = QtGui.qApp.getTmpDir('mek_tmp')
                self.tempDirList.append(tmpDir)
                for name in names:
                    if rx_arch.exactMatch(name):
                        subArchName = archive.extract(name, tmpDir2)
                        subArch = ZipFile(subArchName)
                        subDir = os.path.join(tmpDir2, name[:-4])
                        os.mkdir(subDir)
                        for subName in subArch.namelist():
                            if rx_arch.exactMatch(subName):
                                subArchName2 = subArch.extract(name, subDir)
                                subArch2 = ZipFile(subArchName2)
                                for subName2 in subArch2.namelist():
                                    if rx.exactMatch(subName2):
                                        self.MekFileNames.append(subArch2.extract(subName2, tmpDir))
                                subArch2.close()
                        subArch.close()
                archive.close()
                QtGui.qApp.removeTmpDir(tmpDir2)
                if not self.MekFileNames:
                    self.err2log(u'В архиве отсутствуют протоколы МЭК')
                    return
            elif self.tabRegime.currentWidget() == self.tabReMEK:
                archive = ZipFile(archiveName, 'r')
                names = archive.namelist()
                self.reMekFileNames = []
                rx_arch = QRegExp('[0-9]{7}_R[0-9]{2}.zip$', Qt.CaseInsensitive)
                rx = QRegExp('RS.*.xml$', Qt.CaseInsensitive)
                tmpDir = QtGui.qApp.getTmpDir('remek')
                tmpDir2 = QtGui.qApp.getTmpDir('remek_tmp')
                self.tempDirList.append(tmpDir)
                for name in names:
                    if rx_arch.exactMatch(name):
                        subArchName = archive.extract(name, tmpDir2)
                        subArch = ZipFile(subArchName)
                        subDir = os.path.join(tmpDir2, name[:-4])
                        os.mkdir(subDir)
                        for subName in subArch.namelist():
                            if rx.exactMatch(subName):
                                self.ReMekFileNames.append(subArch.extract(subName, tmpDir))
                        subArch.close()
                archive.close()
                QtGui.qApp.removeTmpDir(tmpDir2)
                if not self.ReMekFileNames:
                    self.err2log(u'В архиве отсутствуют протоколы повторного МЭК')
                    return
        except Exception, e:
            self.err2log(u'Ошибка распаковки архива: Невозможно распаковать архив\n' + unicode(e))
            return

        # импорт ФЛК
        if self.tabRegime.currentWidget() == self.tabFLC:
            # импорт протоколов ФЛК
            self.db.deleteRecordSimple(self.table, '')
            for fileName in self.flcFileNames:
                self.processFile(fileName, fileType='flc')
            # импорт страховой идентификации
            self.db.deleteRecordSimple(self.tableFinal, '')
            for fileName in self.policyFileNames:
                self.processFile(fileName, fileType='policy')
            for fileName in self.errorFileNames:
                self.processFile(fileName, fileType='err')
            QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
            if self.chkUpdatePolicy.isChecked():
                self.log.append(u'Обновление полисных данных...')
                QtGui.qApp.processEvents()
                QtGui.qApp.db.query('CALL updateClientPolicyByFlc();')
                self.log.append(u'Обновление полисных данных завершено!')
                QtGui.qApp.processEvents()
            if self.chkUpdateAccounts.isChecked():
                res = []
                query = self.db.query(u"""SELECT f.IDCASE
FROM ro_finalFLC f
LEFT JOIN Event e ON e.id = f.IDCASE
LEFT JOIN Account_Item ai ON ai.event_id = f.IDCASE
LEFT JOIN Account a ON a.id = ai.master_id AND a.deleted = 0
WHERE f.payerCode NOT IN ('00000') AND a.id IS NULL""")
                while query.next():
                    res.append(forceString(query.record().value('IDCASE')))
                if res:
                    QtGui.QMessageBox.critical(self, u'Ошибка', u'В сформированных счетах отсутствуют следующие события\n{0}\nДальнейшая разделение по реестрам не возможно!'.format(', '.join(res)), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                    QtGui.qApp.restoreOverrideCursor()
                    return
                self.log.append(u'Разделение реестров по страховым компаниям...')
                QtGui.qApp.processEvents()
                QtGui.qApp.db.query('CALL updateAccountByFlc();')
                QtGui.qApp.processEvents()
                if self.reestrFileNames:
                    self.log.append(u'Сохранение реестров счетов...')
                    QtGui.qApp.processEvents()
                    tableOrg = self.db.table('Organisation')
                    code = forceString(self.db.translate(tableOrg, 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
                    fileName = 'REESTR%s%s%02d.zip' % (code[:5], self.schet['YEAR'][2:], int(self.schet['MONTH']))
                    path = os.path.join(forceString(self.edtOutputDir.text()), fileName)
                    success = compressFileInZip(self.reestrFileNames, path)
                    if success:
                        self.log.append(path)
                    for name in self.reestrFileNames:
                        dst = os.path.join(forceString(self.edtOutputDir.text()), os.path.basename(name))
                        success, _ = QtGui.qApp.call(self, shutil.move, (name, dst))
                        if success:
                            self.log.append(dst)
                        # формируем счето на СМО
                        platName = os.path.basename(name)[8:-4]
                        schet = self.schetDict.get('10' if platName == 'mtr' else platName)
                        invoiceFileName = 'invoice_' + code + '_' + schet['PLAT'] + ('_%02d' % int(schet['MONTH'])) + '.xls'
                        if platName == 'mtr':
                            self.createInvoiceTFOMS(invoiceFileName, schet)
                        else:
                            self.createInvoiceSMO(invoiceFileName, schet, name, getChecksum(dst))


                self.log.append(u'Разделение реестров по страховым компаниям завершено!')
            QtGui.qApp.restoreOverrideCursor()
        elif self.tabRegime.currentWidget() == self.tabMEK:
            # импорт МЭК
            for fileName in self.MekFileNames:
                self.idCases = []
                self.processFile(fileName, fileType='mek')
        elif self.tabRegime.currentWidget() == self.tabReMEK:
            # импорт повторного МЭК
            for fileName in self.ReMekFileNames:
                self.idCases = []
                self.processFile(fileName, fileType='remek')


    def processItem(self, item, fileType):
        if fileType == 'flc':
            newRecord = self.table.newRecord()
            newRecord.setValue('isDone', 0)
            for fieldName in item.keys():
                newRecord.setValue(fieldName, item[fieldName])
            self.recordList.append(newRecord)
            if len(self.recordList) == 1000:
                self.insertRecordList(self.table, self.recordList)
                self.recordList = []
        elif fileType == 'mek':
            if isinstance(item['SLUCH'], list):
                for sl in item['SLUCH']:
                    if sl.get('OPLATA') == '2':
                        self.processSank(sl['IDCASE'], sl['SANK'], year=self.schet['YEAR'], month=self.schet['MONTH'])
            else:
                if item['SLUCH'].get('OPLATA') == '2':
                    self.processSank(item['SLUCH']['IDCASE'], item['SLUCH']['SANK'], year=self.schet['YEAR'], month=self.schet['MONTH'])
        elif fileType == 'remek':
            if isinstance(item['SLUCH'], list):
                for sl in item['SLUCH']:
                    self.processSank(sl['IDCASE'], sl['SANK'], aktDate=item['DATE_AKT'], aktNumber=item['NAKT'], year=item['YEAR'], month=item['MONTH'])
            else:
                self.processSank(item['SLUCH']['IDCASE'], item['SLUCH']['SANK'], aktDate=item['DATE_AKT'], aktNumber=item['NAKT'], year=item['YEAR'], month=item['MONTH'])
        else:
            if isinstance(item['SLUCH'], list):
                for sl in item['SLUCH']:
                    newRecord = self.tableFinal.newRecord()
                    newRecord.setValue('ID_PAC', item['PACIENT']['ID_PAC'])
                    newRecord.setValue('IDCASE', sl['IDCASE'])
                    newRecord.setValue('ENP_ID', item['PACIENT'].get('ENP_ID'))
                    newRecord.setValue('SMO_OGRN_ID', item['PACIENT'].get('SMO_OGRN_ID'))
                    newRecord.setValue('SMO_OK_ID', item['PACIENT'].get('SMO_OK_ID'))
                    newRecord.setValue('SMO_NAM_ID', item['PACIENT'].get('SMO_NAM_ID'))
                    newRecord.setValue('SMO_ID', item['PACIENT'].get('SMO_ID'))
                    newRecord.setValue('VPOLIS_ID', item['PACIENT'].get('VPOLIS_ID'))
                    newRecord.setValue('SPOLIS_ID', item['PACIENT'].get('SPOLIS_ID'))
                    newRecord.setValue('NPOLIS_ID', item['PACIENT'].get('NPOLIS_ID'))
                    newRecord.setValue('KPACI', item['PACIENT'].get('KPACI'))
                    newRecord.setValue('payerCode', item.get('payerCode'))
                    newRecord.setValue('archiveName', item.get('archiveName'))
                    self.recordList.append(newRecord)
                    if len(self.recordList) == 1000:
                        self.insertRecordList(self.tableFinal, self.recordList)
                        self.recordList = []
            else:
                newRecord = self.tableFinal.newRecord()
                newRecord.setValue('ID_PAC', item['PACIENT']['ID_PAC'])
                newRecord.setValue('IDCASE', item['SLUCH']['IDCASE'])
                newRecord.setValue('ENP_ID', item['PACIENT'].get('ENP_ID'))
                newRecord.setValue('SMO_OGRN_ID', item['PACIENT'].get('SMO_OGRN_ID'))
                newRecord.setValue('SMO_OK_ID', item['PACIENT'].get('SMO_OK_ID'))
                newRecord.setValue('SMO_NAM_ID', item['PACIENT'].get('SMO_NAM_ID'))
                newRecord.setValue('SMO_ID', item['PACIENT'].get('SMO_ID'))
                newRecord.setValue('VPOLIS_ID', item['PACIENT'].get('VPOLIS_ID'))
                newRecord.setValue('SPOLIS_ID', item['PACIENT'].get('SPOLIS_ID'))
                newRecord.setValue('NPOLIS_ID', item['PACIENT'].get('NPOLIS_ID'))
                newRecord.setValue('KPACI', item['PACIENT'].get('KPACI'))
                newRecord.setValue('payerCode', item.get('payerCode'))
                newRecord.setValue('archiveName', item.get('archiveName'))
                self.recordList.append(newRecord)
                if len(self.recordList) == 1000:
                    self.insertRecordList(self.tableFinal, self.recordList)
                    self.recordList = []
        self.nProcessed += 1


    def processSank(self, eventId, sank, aktDate=None, aktNumber=None, year=None, month=None):
        if isinstance(sank, list):
            sank = sank[-1]
        if self.tabRegime.currentWidget() == self.tabMEK:
            aktDate = sank['DATE_ACT']
            aktNumber = sank['NUM_ACT']
        self.idCases.append(eventId)
        note = 'ImportMEK' if self.tabRegime.currentWidget() == self.tabMEK else 'ImportReMEK'
        refuseTypeId = self.getRefuseTypeId(sank['S_OSN'])
        stmt = u"UPDATE Event SET mekDate = '{0}', mekRefuseType_id = {1} WHERE id = {2}".format(aktDate, refuseTypeId, eventId)
        self.db.query(stmt)

        stmt = u"""UPDATE Account_Item ai
                    LEFT JOIN Action a on ai.action_id = a.id
                    LEFT JOIN Visit v on v.id = ai.visit_id
                    LEFT JOIN Event_CSG ec ON ec.id = ai.eventCSG_id
                    LEFT JOIN Event e ON ai.event_id = e.id AND e.MES_id IS NOT NULL AND ai.action_id IS NULL AND ai.visit_id IS NULL AND ai.eventCSG_id is null
               SET  ai.payedSum = 0,
                    ai.date = '{0}',
                    ai.number = '{1}',
                    ai.refuseType_id = {2},
                    ai.note = '{6}_{3}-{4:0>2}',
                    a.payStatus = 32,
                    v.payStatus = 32,
                    ec.payStatus = 32,
                    e.payStatus = 32
               WHERE ai.event_id = {5}""".format(aktDate, aktNumber, refuseTypeId, year, month, eventId, note)
        self.db.query(stmt)


    def getRefuseTypeId(self, regionalCode):
        u'''Поиск id типа причины отказа по его региональному коду. Результаты кэшируются.
        Для использования необходимо вызвать additionalInit()'''

        result = self.refuseTypeIdCache.get(regionalCode, -1)

        if result == -1:
            result = forceRef(self.db.translate('rbPayRefuseType', 'regionalCode', regionalCode, 'id'))
            self.refuseTypeIdCache[regionalCode] = result

        return result


    def readHeader(self, fileType):
        u"""Разбирает заголовок"""
        if fileType == 'flc':
            while not self.atEnd():
                self.readNext()
                if self.isStartElement():
                    if self.name() == self.flkpGroupName or self.name() == 'FNAME':
                        continue
                    elif self.name() == 'FNAME_I':
                        while not (self.atEnd() or self.isEndElement()):
                            self.readNext()
                        return True
                    else:
                        self.raiseError(u'Неверный формат экспорта данных.')
            return False
        else:
            while not self.atEnd():
                self.readNext()
                if self.name() == 'ZGLV' and self.isEndElement():
                    return True
                continue
            return False


    def readData(self, fileType):
        if fileType in 'flc':
            while not self.atEnd():
                QtGui.qApp.processEvents()
                self.readNext()
                if self.isEndElement():
                    break
                if self.isStartElement():
                    if self.name() == self.prGroupName:
                        yield self.readGroupEx(self.prGroupName, self.prFields)
                    else:
                        self.readUnknownElement()
                if self.hasError() or self.aborted:
                    break
        elif fileType == 'remek':
            while not self.atEnd():
                QtGui.qApp.processEvents()
                self.readNext()
                if self.isEndElement():
                    break
                if self.isStartElement():
                    if self.name() == 'AKT':
                        yield self.readGroupEx('AKT', self.aktFields, silent=True,
                                               subGroupDict={'SLUCH': {'fields': self.aktSluchFields,
                                                                       'subGroup': self.aktSankSubGroup}})
                    else:
                        self.readUnknownElement()
                if self.hasError() or self.aborted:
                    break
        else:
            while not self.atEnd():
                QtGui.qApp.processEvents()
                self.readNext()
                if self.isEndElement():
                    break
                if self.isStartElement():
                    if self.name() == 'ZAP':
                        yield self.readGroupEx('ZAP', self.zapFields, silent=True, subGroupDict={'PACIENT': {'fields': self.pacFields},
                                                                                                 'SLUCH': {'fields': self.sluchFields,
                                                                                                           'subGroup': self.sankSubGroup}})
                    else:
                        self.readUnknownElement()
                if self.hasError() or self.aborted:
                    break

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
        table = self.table if fileType == 'flc' else self.tableFinal
        if self.readHeader(fileType):
            if fileType in ['policy']:

                self.schet = self.readSchet()
                self.schetDict[self.schet['PLAT'][-2:]] = self.schet
                tableSchet = self.db.table('ro_perCapitaFinancing')
                date = QDate(forceInt(self.schet['YEAR']), forceInt(self.schet['MONTH']) + 1, 1).addDays(-1)
                payerCode = self.schet.get('PLAT', None)
                if payerCode and payerCode != '00000':
                    tableOrg = self.db.table('Organisation')
                    schetRecord = self.db.getRecordEx(tableSchet, '*', [tableSchet['date'].eq(date),
                                                                        tableSchet['infisCode'].eq(payerCode)])
                    payerRecord = self.db.getRecordEx('Organisation', 'id', [tableOrg['infisCode'].eq(payerCode),
                                                                             tableOrg['deleted'].eq(0),
                                                                             tableOrg['isInsurer'].eq(1),
                                                                             tableOrg['head_id'].isNull()])
                    payerId = forceRef(payerRecord.value('id')) if payerRecord else None

                    if schetRecord is None:
                        schetRecord = tableSchet.newRecord()
                    schetRecord.setValue('createDatetime', self.db.getCurrentDatetime())
                    schetRecord.setValue('createPerson_id', QtGui.qApp.userId)
                    schetRecord.setValue('date', date)
                    schetRecord.setValue('infisCode', payerCode)
                    schetRecord.setValue('payer_id', payerId)
                    schetRecord.setValue('summa_pf', forceDouble(self.schet.get('SUMMA_PF', 0)))
                    schetRecord.setValue('summa_cmp', forceDouble(self.schet.get('SUMMA_SMP', 0)))
                    self.db.insertOrUpdate(tableSchet, schetRecord)
            elif fileType in ['mek', 'err']:
                self.schet = self.readSchet()
            for item in self.readData(fileType):
                self.progressBar.setValue(inFile.pos())
                QtGui.qApp.processEvents()
                if item:
                    if fileType not in ['flc', 'mek', 'remek']:
                        item['payerCode'] = fileName[-15:-10]
                        item['archiveName'] = os.path.basename(unicode(self.edtFileName.text()))[:-4]
                    self.processItem(item, fileType)
                if self.aborted:
                    break

            if self.recordList:
                self.insertRecordList(table, self.recordList)
                self.recordList = []

            if fileType in ['mek', 'remek'] and self.idCases:
                self.updateAccountsAfterMEK()

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


    def updateAccountsAfterMEK(self):
        tblAccountItem = self.db.table('Account_Item')
        accountList = self.db.getDistinctIdList(tblAccountItem, idCol=['master_id'], where=tblAccountItem['event_id'].inlist(self.idCases))
        for accountId in accountList:
            updateAccount(accountId)


    def closeEvent(self, event):
        for _dir in self.tempDirList:
            QtGui.qApp.removeTmpDir(_dir)
        event.accept()


    def getOrgRequisites(self, org_id):
        accountName = personalAccount = accBankName = notes = BIK = bankName = corrAccount = ''
        tableOrgAccount = self.db.table('Organisation_Account')
        tableBank = self.db.table('Bank')
        table = tableOrgAccount.leftJoin(tableBank, tableOrgAccount['bank_id'].eq(tableBank['id']))
        cols = [tableOrgAccount['name'].alias('accountName'),
                tableOrgAccount['personalAccount'],
                tableOrgAccount['bankName'].alias('accBankName'),
                tableOrgAccount['notes'],
                tableBank['BIK'],
                tableBank['name'].alias('bankName'),
                tableBank['corrAccount']
                ]
        record = self.db.getRecordEx(table, cols, tableOrgAccount['organisation_id'].eq(org_id), tableOrgAccount['id'].name() + ' DESC')
        if record:
            accountName = forceString(record.value('accountName'))
            personalAccount = forceString(record.value('personalAccount'))
            accBankName = forceString(record.value('accBankName'))
            notes = forceString(record.value('notes'))
            BIK = forceString(record.value('BIK'))
            bankName = forceString(record.value('bankName'))
            corrAccount = forceString(record.value('corrAccount'))
        return accountName, personalAccount, accBankName, notes, BIK, bankName, corrAccount


    def createInvoiceSMO(self, invoiceFileName, schet, archName, checksum):
        u"""
        Формирование счета на СМО
        """
        xlstempfile = os.path.join(forceString(self.edtOutputDir.text()), invoiceFileName)
        try:
            success, _ = QtGui.qApp.call(self, shutil.copy, ('Exchange/invoiceR61.xls', xlstempfile))
        except IOError:
            success, _ = QtGui.qApp.call(self, shutil.copy, ('invoiceR61.xls', xlstempfile))
        if success:
            self.log.append(xlstempfile)
        # Заполняем счет
        existing_workbook = xlrd.open_workbook(xlstempfile, formatting_info=True)

        workbook = xlrd.copy(existing_workbook)
        worksheet = workbook.get_sheet(0)
        worksheet.set_fit_num_pages(1)
        style = easyxf(
            "align: horizontal center, wrap true; font: name Times New Roman, height 200; borders: bottom thin;")
        orgInfo = CInfoContext().getInstance(COrgInfo, QtGui.qApp.currentOrgId())
        worksheet.write(3, 1, orgInfo.fullName, style)
        style = easyxf("align: horizontal left; font: name Times New Roman, height 200; borders: bottom thin;")
        worksheet.write(5, 1, u'Адрес: ' + (orgInfo.address if orgInfo.address else orgInfo.addressFreeInput), style)
        worksheet.write(6, 1, u'Телефон: ' + orgInfo.phone, style)
        tableOrg = self.db.table('Organisation')
        accountName, personalAccount, accBankName, notes, BIK, bankName, corrAccount = self.getOrgRequisites(QtGui.qApp.currentOrgId())
        style = easyxf(
            "align: horizontal left, vert center, wrap true; font: name Times New Roman, height 200; borders: bottom thin;")
        worksheet.write(7, 1, u'Платежные реквизиты: ' + u' '.join([accountName, bankName, u'\n(' + accBankName + (
                    u', л/с ' + personalAccount + u')') if personalAccount else u') ',
                                                                    u'\nКБК 00000000000000000130 единый казначейский счет 40102810845370000050']),
                        style)
        style = easyxf("align: horizontal left; font: name Times New Roman, height 180; borders: bottom thin;")
        worksheet.write(8, 1, u'БИК {0} ИНН {1} КПП {2} ОКТМО 60701000'.format(BIK, orgInfo.INN, orgInfo.KPP), style)

        payerRecord = self.db.getRecordEx(tableOrg, tableOrg['id'], [tableOrg['deleted'].eq(0),
                                                                     tableOrg['isInsurer'].eq(1),
                                                                     tableOrg['isActive'].eq(1),
                                                                     tableOrg['head_id'].isNull(),
                                                                     tableOrg['infisCode'].eq(schet['PLAT'])
                                                                     ])
        if payerRecord:
            payerId = forceRef(payerRecord.value('id'))
            payerInfo = CInfoContext().getInstance(COrgInfo, payerId)
            style = easyxf(
                "align: horizontal center, wrap true; font: name Times New Roman, height 200; borders: bottom thin;")
            worksheet.write(10, 1, payerInfo.fullName, style)
            style = easyxf(
                "align: horizontal left, wrap true; font: name Times New Roman, height 200; borders: bottom thin;")
            worksheet.write(12, 1,
                            u'Адрес: ' + (payerInfo.address.__str__() if payerInfo.address else payerInfo.addressFreeInput),
                            style)
            worksheet.write(13, 1, u'Телефон: ' + payerInfo.phone, style)
            accountName, personalAccount, accBankName, notes, BIK, bankName, corrAccount = self.getOrgRequisites(payerId)
            worksheet.write(14, 1, u'Платежные реквизиты: ' + u' '.join([accountName, bankName]), style)
            style = easyxf("align: horizontal left; font: name Times New Roman, height 180; borders: bottom thin;")
            worksheet.write(15, 1, u'БИК {0} ИНН {1} КПП {2} ОКТМО 60701000'.format(BIK, payerInfo.INN, payerInfo.KPP),
                            style)
            style = easyxf("align: horizontal center, vert center; font: bold true, name Times New Roman, height 180;")
            worksheet.write(17, 1, u'СЧЕТ № {0}  от {1} г.'.format(schet['NSCHET'], formatDate(
                QDate.fromString(schet['DSCHET'], Qt.ISODate))), style)
            style = easyxf(
                "align: horizontal left, vert center, wrap true; font: bold true, name Times New Roman, height 180; borders: top medium, bottom no_line, left medium, right medium;")
            worksheet.write(20, 1,
                            u'Медицинская помощь, оказанная в медицинской организации  Ростовской области, застрахованным\n{0}, в том числе:'.format(
                                payerInfo.shortName), style)
        monthName = forceString(QDate.longMonthName(forceInt(schet['MONTH']))).lower()
        summaAll = forceDouble(schet['SUMMAV']) + forceDouble(schet['SUMMA_PF'])
        accDate = lastMonthDay(QDate(forceInt(schet['YEAR']), forceInt(schet['MONTH']), 1))
        stmt = u"""SELECT 
          (CASE   WHEN (mat.federalCode IN ('1', '3') AND IFNULL(ep.code, '') != 'r6020') THEN '1_stacionar' 
                  WHEN (mat.federalCode = '2' AND IFNULL(ep.code, '') != 'r6020') THEN '1_stacionarVMP'    
                  WHEN mat.federalCode = '7' THEN '2_D_stacionar'     
                  WHEN (mat.federalCode IN ('6', '9', '10') OR (mat.federalCode = '1' AND ep.code = 'r6020')) THEN '3_policlinic' END) 
                  AS 'kindHelp',  
          reestr.date AS 'reestrDate',
          reestr.settleDate as 'reestrSettleDate',  
          SUM(ROUND(ai.sum, 2)) AS 'summa'
        FROM Account_Item ai   
          LEFT JOIN Account reestr ON reestr.id = ai.master_id   
          LEFT JOIN rbAccountType reestrType ON reestr.type_id = reestrType.id   
          LEFT JOIN Organisation payer ON payer.id = reestr.payer_id  
          LEFT JOIN rbService serv ON serv.id = ai.service_id   
          LEFT JOIN Event e ON e.id = ai.event_id    
          LEFT JOIN EventType et ON et.id = e.eventType_id   
          LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id   
          LEFT JOIN rbEventProfile ep ON et.eventProfile_id = ep.id  
          LEFT JOIN Event_CSG ec ON ai.eventCSG_id = ec.id 
          LEFT JOIN Contract con ON reestr.contract_id = con.id   
          LEFT JOIN Client pacient ON e.client_id = pacient.id
        WHERE reestr.deleted = 0 AND ai.deleted = 0  
        AND IFNULL(ep.code, '') NOT LIKE 'r6027%'
        AND (ROUND(ai.sum, 2)) > 0
        AND reestr.date = {date}
        AND reestr.payer_id = {payerId}
        AND con.finance_id = 2
        GROUP BY kindHelp, reestrDate, reestrSettleDate
        ORDER BY kindHelp, reestrDate, reestrSettleDate DESC;""".format(payerId=payerId,
                                                                        date=self.db.formatDate(accDate))
        query = self.db.query(stmt)
        summaKSAll = 0
        summaKSPrev = 0
        prevMonthsKS = []
        summaVMPAll = 0
        summaVMPPrev = 0
        prevMonthsVMP = []
        summaDSAll = 0
        summaDSPrev = 0
        prevMonthsDS = []
        summaAmbAll = 0
        summaAmbPrev = 0
        prevMonthsAmb = []
        style = easyxf(
            "align: horizontal left, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left medium, right thin;")
        style2 = easyxf(
            "align: horizontal right, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left thin, right medium;")
        style3 = easyxf(
            "align: horizontal right, vert center; font: bold true, name Times New Roman, height 180; borders: top medium, bottom medium, left medium, right medium;")
        while query.next():
            record = query.record()
            kindHelp = forceString(record.value('kindHelp'))
            reestrDate = forceDate(record.value('reestrDate'))
            reestrSettleDate = forceDate(record.value('reestrSettleDate'))
            summa = forceDouble(record.value('summa'))
            if kindHelp == '1_stacionar':
                summaKSAll += summa
                worksheet.write(27, 2, summaKSAll, style3)
                if reestrDate == reestrSettleDate:
                    worksheet.write(23, 1,
                                    u'медицинская помощь в условиях круглосуточного стационара в {0} {1} г.'.format(
                                        monthName, schet['YEAR']), style)
                    worksheet.write(23, 2, summa, style2)
                else:
                    prevMonthName = forceString(QDate.longMonthName(reestrSettleDate.month())).lower()
                    summaKSPrev += summa
                    prevMonthsKS.append(prevMonthName)

            elif kindHelp == '1_stacionarVMP':
                summaVMPAll += summa
                worksheet.write(33, 2, summaVMPAll, style3)
                if reestrDate == reestrSettleDate:
                    worksheet.write(29, 1, u'высокотехнологичная медицинская помощь в {0} {1} г.'.format(monthName,
                                                                                                         schet['YEAR']),
                                    style)
                    worksheet.write(29, 2, summa, style2)
                else:
                    prevMonthName = forceString(QDate.longMonthName(reestrSettleDate.month())).lower()
                    summaVMPPrev += summa
                    prevMonthsVMP.append(prevMonthName)
            elif kindHelp == '2_D_stacionar':
                summaDSAll += summa
                worksheet.write(39, 2, summaDSAll, style3)
                if reestrDate == reestrSettleDate:
                    worksheet.write(35, 1,
                                    u'медицинская помощь в условиях дневного стационара в {0} {1} г.'.format(monthName,
                                                                                                             schet[
                                                                                                                 'YEAR']),
                                    style)
                    worksheet.write(35, 2, summa, style2)
                else:
                    prevMonthName = forceString(QDate.longMonthName(reestrSettleDate.month())).lower()
                    summaDSPrev += summa
                    prevMonthsDS.append(prevMonthName)
            elif kindHelp == '3_policlinic':
                summaAmbAll += summa
                worksheet.write(50, 2, summaAmbAll, style3)
                if reestrDate == reestrSettleDate:
                    worksheet.write(46, 1, u'в амбулаторных условиях  за единицу объема в {0} {1} г.'.format(monthName,
                                                                                                             schet[
                                                                                                                 'YEAR']),
                                    style)
                    worksheet.write(46, 2, summa, style2)
                else:
                    prevMonthName = forceString(QDate.longMonthName(reestrSettleDate.month())).lower()
                    summaAmbPrev += summa
                    prevMonthsAmb.append(prevMonthName)
        style = easyxf(
            "align: horizontal left, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left medium, right thin;")
        style2 = easyxf(
            "align: horizontal right, vert center; font: name Times New Roman, height 180; borders: top thin, bottom medium, left thin, right medium;")
        if prevMonthsKS:
            worksheet.write(25, 1, u'медицинская помощь в условиях круглосуточного стационара в {0} {1} г.'.format(
                u', '.join(prevMonthsKS), reestrSettleDate.year()), style)
            worksheet.write(25, 2, summaKSPrev, style2)
        if prevMonthsVMP:
            worksheet.write(31, 1,
                            u'высокотехнологичная медицинская помощь в {0} {1} г.'.format(u', '.join(prevMonthsVMP),
                                                                                          reestrSettleDate.year()),
                            style)
            worksheet.write(31, 2, summaVMPPrev, style2)
        if prevMonthsDS:
            worksheet.write(37, 1, u'медицинская помощь в условиях дневного стационара в {0} {1} г.'.format(
                u', '.join(prevMonthsDS), reestrSettleDate.year()), style)
            worksheet.write(37, 2, summaDSPrev, style2)
        style2 = easyxf(
            "align: horizontal right, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left thin, right medium;")
        if prevMonthsAmb:
            worksheet.write(48, 1,
                            u'в амбулаторных условиях  за единицу объема в {0} {1} г.'.format(u', '.join(prevMonthsAmb),
                                                                                              reestrSettleDate.year()),
                            style)
            worksheet.write(48, 2, summaAmbPrev, style2)

        worksheet.write(50, 2, summaAmbAll, style2)
        worksheet.write(51, 2, summaAmbAll + forceDouble(schet['SUMMA_PF']), style3)
        worksheet.write(20, 2, summaAll, style3)
        style2 = easyxf(
            "align: horizontal left, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left medium, right thin;")
        worksheet.write(41, 1,
                        u'Медицинская помощь в амбулаторных условиях с оплатой по подушевому нормативу за {0} текущий период'.format(
                            monthName), style2)
        style2 = easyxf(
            "align: horizontal right, vert center; font: name Times New Roman, height 180; borders: top thin, bottom thin, left thin, right medium;")
        worksheet.write(41, 2, forceDouble(schet['SUMMA_PF']), style2)
        worksheet.write(44, 2, forceDouble(schet['SUMMA_PF']), style2)
        worksheet.write(58, 2, summaAll, style3)
        style = easyxf("font: bold true, name Times New Roman, height 180;")
        worksheet.write(60, 1, u'Сумма прописью (за счет средств ОМС): {0}'.format(amountToWords(summaAll)), style)
        style2 = easyxf(
            "align: horizontal right, vert center; font: bold true, name Times New Roman, height 180; borders: top thin, bottom thin, left thin, right thin;")
        worksheet.write(63, 2, os.path.basename(archName), style2)
        worksheet.write(64, 2, checksum, style2)
        style = easyxf("font: name Times New Roman, height 220;")
        worksheet.write(67, 1,
                        u'Руководитель медицинской организации____________________________________          {0}'.format(
                            orgInfo.chief.shortName if orgInfo.chief else orgInfo.chiefFreeInput), style)
        worksheet.write(69, 1,
                        u'Главный бухгалтер медицинской организации________________________________          {0}'.format(
                            orgInfo.accountant), style)
        workbook.save(xlstempfile)


    def createInvoiceTFOMS(self, invoiceFileName, schet):
        u"""
        Формирование счета на ТФОМС
        """
        xlstempfile = os.path.join(forceString(self.edtOutputDir.text()), invoiceFileName)
        try:
            success, _ = QtGui.qApp.call(self, shutil.copy, ('Exchange/invoiceTFOMSR61.xls', xlstempfile))
        except IOError:
            success, _ = QtGui.qApp.call(self, shutil.copy, ('invoiceTFOMSR61.xls', xlstempfile))
        if success:
            self.log.append(xlstempfile)
        # Заполняем счет
        existing_workbook = xlrd.open_workbook(xlstempfile, formatting_info=True)

        workbook = xlrd.copy(existing_workbook)
        worksheet = workbook.get_sheet(0)
        worksheet.set_fit_num_pages(1)
        # Поставщик
        style = easyxf("align: horizontal center, wrap true; font: name Times New Roman, height 200, bold true; borders: bottom thin;")
        orgInfo = CInfoContext().getInstance(COrgInfo, QtGui.qApp.currentOrgId())
        worksheet.write(1, 0, orgInfo.fullName, style)
        style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 220; borders: bottom thin;")
        worksheet.write(7, 3, (orgInfo.address.__str__() if orgInfo.address else orgInfo.addressFreeInput), style)
        worksheet.write(10, 3, orgInfo.INN, style)
        worksheet.write(10, 6, orgInfo.KPP, style)
        worksheet.write(11, 3, orgInfo.phone, style)
        accountName, personalAccount, accBankName, notes, BIK, bankName, corrAccount = self.getOrgRequisites(QtGui.qApp.currentOrgId())
        worksheet.write(12, 3, personalAccount, style)
        worksheet.write(14, 3, accountName, style)
        worksheet.write(19, 3, bankName, style)
        worksheet.write(20, 3, BIK, style)
        # Покупатель
        tableOrg = self.db.table('Organisation')
        payerRecord = self.db.getRecordEx(tableOrg, tableOrg['id'], [tableOrg['deleted'].eq(0),
                                                                     tableOrg['isInsurer'].eq(1),
                                                                     tableOrg['isActive'].eq(1),
                                                                     tableOrg['head_id'].isNull(),
                                                                     tableOrg['infisCode'].eq(schet['PLAT'])
                                                                     ])
        payerId = None
        if payerRecord:
            payerId = forceRef(payerRecord.value('id'))
            payerInfo = CInfoContext().getInstance(COrgInfo, payerId)
            style = easyxf("align: horizontal center, wrap true; font: name Times New Roman, height 200, bold true; borders: bottom thin;")
            worksheet.write(26, 0, payerInfo.fullName, style)
            style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 220; borders: bottom thin;")
            worksheet.write(27, 3, (payerInfo.address.__str__() if payerInfo.address else payerInfo.addressFreeInput), style)
            worksheet.write(29, 3, payerInfo.INN, style)
            worksheet.write(29, 6, payerInfo.KPP, style)
            worksheet.write(30, 3, payerInfo.phone, style)
            accountName, personalAccount, accBankName, notes, BIK, bankName, corrAccount = self.getOrgRequisites(payerId)
            worksheet.write(31, 3, personalAccount, style)
            worksheet.write(33, 3, accountName, style)
            worksheet.write(34, 3, bankName, style)
            worksheet.write(35, 3, BIK, style)

        # Собственно сам счет
        style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 220, bold true; borders: bottom thin;")
        worksheet.write(37, 3, schet['NSCHET'], style)
        worksheet.write(37, 5, formatDate(QDate.fromString(schet['DSCHET'], Qt.ISODate)), style)
        if payerId:
            accDate = lastMonthDay(QDate(forceInt(schet['YEAR']), forceInt(schet['MONTH']), 1))
            stmt = u"""SELECT 
                      (CASE   WHEN (mat.federalCode IN ('1', '3') AND IFNULL(ep.code, '') != 'r6020') THEN '1_stacionar' 
                              WHEN (mat.federalCode = '2' AND IFNULL(ep.code, '') != 'r6020') THEN '1_stacionarVMP'    
                              WHEN mat.federalCode = '7' THEN '2_D_stacionar'     
                              WHEN (mat.federalCode IN ('6', '9', '10') OR (mat.federalCode = '1' AND ep.code = 'r6020')) THEN '3_policlinic' END) 
                              AS 'kindHelp',  
                      reestr.date AS 'reestrDate',
                      reestr.settleDate as 'reestrSettleDate',  
                      SUM(ROUND(ai.sum, 2)) AS 'summa'
                    FROM Account_Item ai   
                      LEFT JOIN Account reestr ON reestr.id = ai.master_id   
                      LEFT JOIN rbAccountType reestrType ON reestr.type_id = reestrType.id   
                      LEFT JOIN Organisation payer ON payer.id = reestr.payer_id  
                      LEFT JOIN rbService serv ON serv.id = ai.service_id   
                      LEFT JOIN Event e ON e.id = ai.event_id    
                      LEFT JOIN EventType et ON et.id = e.eventType_id   
                      LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id   
                      LEFT JOIN rbEventProfile ep ON et.eventProfile_id = ep.id  
                      LEFT JOIN Event_CSG ec ON ai.eventCSG_id = ec.id 
                      LEFT JOIN Contract con ON reestr.contract_id = con.id   
                      LEFT JOIN Client pacient ON e.client_id = pacient.id
                    WHERE reestr.deleted = 0 AND ai.deleted = 0  
                    AND IFNULL(ep.code, '') NOT LIKE 'r6027%'
                    AND (ROUND(ai.sum, 2)) > 0
                    AND reestr.date = {date}
                    AND reestr.payer_id = {payerId}
                    AND con.finance_id = 2
                    GROUP BY kindHelp, reestrDate, reestrSettleDate
                    ORDER BY kindHelp, reestrDate, reestrSettleDate DESC;""".format(payerId=payerId, date=self.db.formatDate(accDate))
            query = self.db.query(stmt)
            prevMonths = set()
            summaAll = 0
            summaKSAll = 0
            summaKSPrev = 0
            summaDSAll = 0
            summaDSPrev = 0
            summaAmbAll = 0
            summaAmbPrev = 0
            monthName = u'{0} {1} г.'.format(forceString(QDate.longMonthName(forceInt(schet['MONTH']))).lower(), schet['YEAR'])
            style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 160;")
            worksheet.write(45, 1, monthName, style)
            style = easyxf("align: horizontal right; font: name Times New Roman, height 200; borders: top thin, bottom thin, left thin, right thin;")
            style2 = easyxf("align: horizontal right; font: name Times New Roman, height 200, bold true; borders: top thin, bottom thin, left thin, right thin;")
            while query.next():
                record = query.record()
                kindHelp = forceString(record.value('kindHelp'))
                reestrDate = forceDate(record.value('reestrDate'))
                reestrSettleDate = forceDate(record.value('reestrSettleDate'))
                summa = forceDouble(record.value('summa'))
                summaAll += summa
                if kindHelp == '1_stacionar':
                    summaKSAll += summa
                    worksheet.write(49, 4, summaKSAll, style2)
                    if reestrDate == reestrSettleDate:
                        worksheet.write(45, 4, summa, style)
                    else:
                        summaKSPrev += summa
                        worksheet.write(47, 4, summaKSPrev, style2)
                        prevMonths.add(reestrSettleDate.month())
                elif kindHelp == '2_D_stacionar':
                    summaDSAll += summa
                    worksheet.write(49, 5, summaDSAll, style2)
                    if reestrDate == reestrSettleDate:
                        worksheet.write(45, 5, summa, style)
                    else:
                        summaDSPrev += summa
                        worksheet.write(47, 5, summaDSPrev, style2)
                        prevMonths.add(reestrSettleDate.month())
                elif kindHelp == '3_policlinic':
                    summaAmbAll += summa
                    worksheet.write(49, 6, summaAmbAll, style2)
                    if reestrDate == reestrSettleDate:
                        worksheet.write(45, 6, summa, style)
                    else:
                        summaAmbPrev += summa
                        worksheet.write(47, 6, summaAmbPrev, style2)
                        prevMonths.add(reestrSettleDate.month())
            worksheet.write(45, 3, summaKSAll + summaDSAll + summaAmbAll, style)
            if prevMonths:
                prevMonthNames = [forceString(QDate.longMonthName(month).lower()) for month in sorted(prevMonths)]
                style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 160;")
                worksheet.write(47, 1, u'{0} {1} г.'.format(u', '.join(prevMonthNames), schet['YEAR']), style)
                worksheet.write(47, 3, summaKSPrev + summaDSPrev + summaAmbAll, style2)
            worksheet.write(49, 3, summaAll, style2)
            style = easyxf("align: horizontal left, wrap true; font: name Times New Roman, height 180;")
            worksheet.write(50, 2, amountToWords(summaAll), style)

        style = easyxf("font: name Times New Roman, height 200;")
        worksheet.write(60, 5, orgInfo.chief.shortName if orgInfo.chief else orgInfo.chiefFreeInput, style)
        worksheet.write(63, 5, orgInfo.accountant, style)
        workbook.save(xlstempfile)
