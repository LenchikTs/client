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

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant, QDate
from library.DbEntityCache     import CDbEntityCache
from library.Utils             import forceString, forceDate, forceInt
from library.Pacs.RestToolbox  import postRequest, getRequest

from DoubleStringActionPropertyValueType import CDoubleStringActionPropertyValueType

class CRadiationDoseActionPropertyValueType(CDoubleStringActionPropertyValueType):
    name        = u'Доза облучения'
    variantType = QVariant.Double

    def __init__(self, domain = None):
        CDoubleStringActionPropertyValueType.__init__(self, domain)
        address = forceString(QtGui.qApp.preferences.appPrefs.get('pacsAddress', ''))
        port = forceString(QtGui.qApp.preferences.appPrefs.get('pacsPort', None))
        self.address = None
        if address:
            self.address = '%s:%s'%(address, port) if port else address
        self.dose = None

    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+CDoubleStringActionPropertyValueType.name


    def toInfo(self, context, v):
        return self.toText(v)


    def toText(self, v):
        if v:
            return v
        if self.dose == None and self.address and self.clientId and self.action:
            actionRecord = self.action.getRecord()
            begDate = forceDate(actionRecord.value('begDate'))
            endDate = forceDate(actionRecord.value('endDate'))
            begDate = begDate if begDate else QDate.currentDate()
            endDate = endDate if endDate else QDate.currentDate()
            date = '%s-%s'%(forceString(begDate.toString('yyyyMMdd')), forceString(endDate.toString('yyyyMMdd')))
            self.dose = getDose(self.address, self.clientId, date)
        return self.dose if self.dose else 0.0


    def shownUp(self, action, clientId):
        self.action = action
        self.clientId = clientId


def getDose(address, clientId, date):
    doseTag = forceString(QtGui.qApp.preferences.appPrefs.get('pacsDoseTag', '0040,0316'))
    pacsClientId = forceInt(QtGui.qApp.preferences.appPrefs.get('pacsClientId', 0))
    if pacsClientId == 0:
        id = clientId
    else:
        id = CClientSNILSCache.getSnils(clientId)
#    imageIdList = []
    dose = None
    if address:
        try:
            dose = 0.0
            patientSearchData = postRequest('http://%s/tools/lookup'%address, id)
            if len(patientSearchData) and patientSearchData[0].get('Type', '') == 'Patient':
                patientData = getRequest('http://%s/patients/%s'%(address, patientSearchData[0]['ID']))
                if patientData:
                    studiesIdList = patientData["Studies"]
                    for studyId in studiesIdList:
                        studyData = getRequest('http://%s/studies/%s'%(address, studyId))
                        if studyData:
                            dateArray = date.split('-')
                            if studyData['MainDicomTags']['StudyDate'] >= dateArray[0] and studyData['MainDicomTags']['StudyDate'] <= dateArray[1]:
                                for series in studyData["Series"]:
                                    seriesData = getRequest('http://%s/series/%s'%(address, series))
                                    for instance in seriesData["Instances"]:
                                        instanceData = getRequest('http://%s/instances/%s/tags'%(address, instance))
                                        dose += float(instanceData[doseTag]['Value'] if doseTag in instanceData else 0)
        except Exception as e:
            if e.message == 'timed out':
                QtGui.QMessageBox.critical(None,
                    u'Внимание!',
                    u'Отсутствует связь с сервером изображений!',
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)
    return dose


class CClientSNILSCache(CDbEntityCache):
    cache = {}

    @classmethod
    def getSnils(cls, id):
        snils = ''
        if id in cls.cache:
            snils = cls.cache[id]
        else:
            cls.connect()
            db = QtGui.qApp.db
            table = db.table('Client')
            record = db.getRecord(table, 'id, SNILS', id)
            if record:
                snils = forceString(record.value('SNILS'))
            cls.cache[id] = snils
        return snils
