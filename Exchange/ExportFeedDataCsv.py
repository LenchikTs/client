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

import os.path
import csv

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDir, QTime, pyqtSignature, SIGNAL, QDateTime

from library.DialogBase import CConstructHelperMixin
from library.Utils import forceBool, forceDate, forceInt, forceString, forceStringEx, forceTime, getPref, getPrefDate, getPrefInt, getPrefTime, setPref, toVariant

from Exchange.Ui_ExportFeedDataCsv_Wizard_1 import Ui_ExportFeedDataCsv_Wizard_1
from Exchange.Ui_ExportFeedDataCsv_Wizard_2 import Ui_ExportFeedDataCsv_Wizard_2


def exportFeedDataCsv(parent):
    fileName = forceString(QtGui.qApp.preferences.appPrefs.get('ExportFeedDataCsvFileName', ''))
    dlg = CExportFeedDataCsv(fileName, parent)
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ExportFeedDataCsvFileName'] = toVariant(dlg.fileName)


class CExportFeedDataCsv(QtGui.QWizard):
    def __init__(self, fileName,  parent=None):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowTitle(u'Экспорт данных о питании')
        self.fileName = fileName
        self.addPage(CExportFeedDataCsvWizardPage1(self))
        self.addPage(CExportFeedDataCsvWizardPage2(self))


class CExportFeedDataCsvWizardPage1(QtGui.QWizardPage, Ui_ExportFeedDataCsv_Wizard_1, CConstructHelperMixin):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        prefs = getPref(QtGui.qApp.preferences.reportPrefs, "exportFeedDataCsv", {})
        self.edtBegDate.setDate(getPrefDate(prefs, 'begDate', QDate.currentDate()))
        self.edtBegTime.setTime(getPrefTime(prefs, 'begTime', QTime.currentTime()))
        self.edtEndDate.setDate(getPrefDate(prefs, 'endDate', QDate.currentDate()))
        self.edtEndTime.setTime(getPrefTime(prefs, 'endTime', QTime.currentTime()))
        self.cmbOrgStructure.setValue(getPrefInt(prefs, 'orgStructureId', QtGui.qApp.currentOrgStructureId()))
        self.parent = parent
        self.setTitle(u'Параметры экспорта')
        self.setSubTitle(u'Выбор записей для экспорта')


    def validatePage(self):
        prefs = {}
        self.parent.begDate = forceDate(self.edtBegDate.date())
        self.parent.begTime = forceTime(self.edtBegTime.time())
        self.parent.endDate = forceDate(self.edtEndDate.date())
        self.parent.endTime = forceTime(self.edtEndTime.time())
        self.parent.orgStructureId = forceInt(self.cmbOrgStructure.value())
        setPref(prefs,  "begDate", toVariant(self.parent.begDate))
        setPref(prefs,  "begTime", toVariant(self.parent.begTime))
        setPref(prefs,  "endDate", toVariant(self.parent.endDate))
        setPref(prefs,  "endTime", toVariant(self.parent.endTime))
        setPref(prefs,  "orgStructureId", toVariant(self.parent.orgStructureId))
        setPref(QtGui.qApp.preferences.reportPrefs, "exportFeedDataCsv", prefs)
        QtGui.qApp.preferences.appPrefs['FeedDataExportData'] = toVariant(self.parent.begDate)
        return True


class CExportFeedDataCsvWizardPage2(QtGui.QWizardPage, Ui_ExportFeedDataCsv_Wizard_2):
    def __init__(self,  parent):
        self.done = False
        self.pathIsValid = True
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.setTitle(u'Параметры сохранения')
        self.setSubTitle(u'Выбор места для сохранения')
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.edtFileName.setText(self.parent.fileName)
        self.btnExport.setEnabled(self.parent.fileName != '')
        self.setFileName()


    def setFileName(self):
        homePath = QDir.toNativeSeparators(QDir.homePath())
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('FeedDataExportDir', homePath))
        exportDate = forceString(forceDate(QtGui.qApp.preferences.appPrefs.get('FeedDataExportData', QDate.currentDate())).toString('yyyy-MM-dd'))
        self.edtFileName.setText(QDir.toNativeSeparators(exportDir+'/%s-feedData.csv'%exportDate))
        if exportDir and exportDate:
            self.btnExport.setEnabled(True)


    def initializePage(self):
        self.setFileName()
        self.done = False


    def isComplete(self):
        return self.done


    def getFeedData(self, begDate, begTime, endDate, endTime, orgStructureId):
        result = []
        cond = []
        group = u''
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableRbMealTime = db.table('rbMealTime')
        tableRbDiet = db.table('rbDiet')
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableActionProperty_OrgStructure = db.table('ActionProperty_OrgStructure')
        tableOrgStructure = db.table('OrgStructure')
        tableRbFinance = db.table('rbFinance')
        tableEventFeed = db.table('Event_Feed')
        queryTable = tableEventFeed
        queryTable = queryTable.leftJoin(tableEvent, queryTable['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.leftJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.leftJoin(tableRbMealTime, queryTable['mealTime_id'].eq(tableRbMealTime['id']))
        queryTable = queryTable.leftJoin(tableRbDiet, queryTable['diet_id'].eq(tableRbDiet['id']))
        queryTable = queryTable.leftJoin(tableAction, queryTable['event_id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.leftJoin(tableActionProperty, tableAction['id'].eq(tableActionProperty['action_id']))
        queryTable = queryTable.leftJoin(tableActionPropertyType, tableActionProperty['type_id'].eq(tableActionPropertyType['id']))
        queryTable = queryTable.leftJoin(tableActionProperty_OrgStructure, tableActionProperty['id'].eq(tableActionProperty_OrgStructure['id']))
        queryTable = queryTable.leftJoin(tableOrgStructure, tableActionProperty_OrgStructure['value'].eq(tableOrgStructure['id']))
        queryTable = queryTable.leftJoin(tableRbFinance, queryTable['finance_id'].eq(tableRbFinance['id']))
        cond.append(db.joinAnd([queryTable['date'].ge(begDate), queryTable['date'].lt(endDate)]))
        cond.append(db.joinOr([tableRbMealTime['begTime'].ge(begTime), tableRbMealTime['endTime'].ge(begTime)]))
        cond.append(tableActionType['flatCode'].like('moving'))
        begDateInDate = 'CONCAT(\'%s\',\'%%\')'%forceString(forceDate(begDate).toString('yyyy-MM-dd'))
        cond.append(db.joinOr([tableAction['begDate'].le(begDate), tableAction['begDate'].signEx(" LIKE ", begDateInDate)]))
        endDateTime = QDateTime(endDate, endTime)
        begDateTime = QDateTime(begDate,  begTime)
        cond.append(db.joinOr([tableAction['endDate'].isNull(), db.joinOr([tableAction['endDate'].ge(endDateTime), tableAction['endDate'].ge(begDateTime)])]))
        cond.append('(IF(Action.`begDate` LIKE %s, TIME(Action.`begDate`)<=TIME(rbMealTime.`endTime`),rbMealTime.`endTime` is not NULL))'%begDateInDate)
        cond.append(tableActionPropertyType['name'].like(u'Отделение пребывания'))
        cond.append(db.joinOr([tableOrgStructure['parent_id'].eq(orgStructureId), tableOrgStructure['id'].eq(orgStructureId)]))
        cond.append(queryTable['refusalToEat'].eq(0))
        cond.append(tableAction['deleted'].eq(0))
        cond.append(tableEvent['deleted'].eq(0))
        cond.append(tableClient['deleted'].eq(0))
        cond.append(tableActionType['deleted'].eq(0))
        cond.append(tableActionProperty['deleted'].eq(0))
        cond.append(tableActionPropertyType['deleted'].eq(0))
        cond.append(tableOrgStructure['deleted'].eq(0))
        cond.append(tableEventFeed['deleted'].eq(0))
        group = u'typeFeed, finance, dietName, orgStr, date'
        records = db.getRecordListGroupBy(queryTable,
                             ['DATE(Event_Feed.date) as date', 'OrgStructure.code as orgStr', 'rbDiet.name as dietName', 'rbFinance.name as finance', 'Event_Feed.typeFeed as typeFeed',  'count(Event_Feed.id) as count'],
                             cond,
                             group)
        if records:
            for record in records:
                feedData = {}
                date = forceString(forceDate(record.value('date')).toString('dd.MM.yyyy'))
                orgStr = forceString(record.value('orgStr'))
                dietName = forceString(record.value('dietName'))
                finance = forceString(record.value('finance'))
                typeFeed = forceBool(record.value('typeFeed'))
                count = forceInt(record.value('count'))
                if typeFeed != 0:
                    typeMark = u'У'
                else:
                    typeMark = u'Пац'
                if finance == u'платные услуги':
                    typeFeedAndFinanceType = typeMark + u'-' + u'ПЛ'
                else:
                    typeFeedAndFinanceType = typeMark + u'-' + finance
                feedData['date'] = date
                feedData['orgStructureCode'] = orgStr.encode('cp1251')
                feedData['dietName'] = dietName.encode('cp1251')
                feedData['typeFeedAndFinanceType'] = typeFeedAndFinanceType.encode('cp1251')
                feedData['count'] = count
                result.append(feedData)
            return result
        else:
            return False


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
            dir = QtGui.QFileDialog.getExistingDirectory(self,
                u'Выберите директорий для сохранения файл',
                 forceStringEx(self.edtFileName.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
            date = forceString(forceDate(QDate.currentDate()).toString('yyyy-MM-dd'))
            if forceString(dir):
                QtGui.qApp.preferences.appPrefs['FeedDataExportDir'] = toVariant(dir)
                self.edtFileName.setText(QDir.toNativeSeparators(dir+'/%s-feedData.csv'%date))


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        fileName = self.edtFileName.text()

        if fileName.isEmpty():
            return

        feedData = self.getFeedData(self.parent.begDate, self.parent.begTime, self.parent.endDate, self.parent.endTime, self.parent.orgStructureId)

        if feedData:
            outFile = open(fileName, "wb")
            wrtr = csv.DictWriter(outFile, fieldnames=['date', 'orgStructureCode', 'dietName', 'typeFeedAndFinanceType', 'count'])
            self.progressBar.setMaximum(len(feedData))
            for line in feedData:
                wrtr.writerow(line)
                self.progressBar.step()
            self.progressBar.setText(u'Готово')
            outFile.close()
        else:
            self.progressBar.setText(u'Нет данных')

        self.done = True
        self.btnExport.setEnabled(False)
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self):
        fileName = forceStringEx(self.edtFileName.text())
        dir = os.path.dirname(fileName)
        pathIsValid = os.path.isdir(dir)
        self.btnExport.setEnabled(pathIsValid)
