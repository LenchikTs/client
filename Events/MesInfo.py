# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

from library.PrintInfo      import CInfo, CInfoList, CDateInfo, CRBInfo
from library.Utils          import forceDate, forceInt, forceRef, forceString
from RefBooks.Service.Info  import CServiceInfo


class CMesGroupInfo(CRBInfo):
    tableName = 'mes.mrbMESGroup'


class CKSGInfo(CRBInfo):
    tableName = 'mes.CSG'


class CMKBInfoList(CInfoList):
    def __init__(self,  context, id):
        CInfoList.__init__(self, context)
        self.masterId = id

    def _load(self):
        rows = []
        query = QtGui.qApp.db.query(self.getMKBQuery(self.masterId))
        while query.next():
            rows.append(query.record())
        self._items = [ self.getInstance(CMesMKBInfo, row) for row in rows ]
        return True

    def getMKBQuery(self, masterId):
        return u"""
        SELECT mes.MES_mkb.mkb as 'code',
        CONCAT_WS(' / ', MKB.DiagName, rbMKBSubclass_Item.name) as 'name',
        mes.MES_mkb.mkbEx as 'exCode',
        CONCAT_WS(' / ', mesMKB_mkbEx.DiagName, MKBEx_SUBCLASS.name) as 'exName',
        mes.MES_mkb.groupingMKB AS 'grouping',
        IF(mes.MES_mkb.blendingMKB = 0, 'основной и дополнительный', IF(mes.MES_mkb.blendingMKB = 1, 'основной', 'дополнительный')) AS 'blending'
        FROM mes.MES_mkb
        LEFT JOIN MKB on MKB.DiagID = LEFT(mes.MES_mkb.mkb, 5)
        LEFT JOIN MKB AS mesMKB_mkbEx on mesMKB_mkbEx.DiagID = LEFT(mes.MES_mkb.mkbEx, 5)
        LEFT JOIN rbMKBSubclass_Item ON (rbMKBSubclass_Item.master_id = MKB.MKBSubclass_id
        AND (length(mes.MES_mkb.mkb) = 6 AND rbMKBSubclass_Item.code = RIGHT(mes.MES_mkb.mkb, 1)))
        LEFT JOIN rbMKBSubclass_Item AS MKBEx_SUBCLASS ON (MKBEx_SUBCLASS.master_id = mesMKB_mkbEx.MKBSubclass_id
        AND (length(mes.MES_mkb.mkbEx) = 6 AND MKBEx_SUBCLASS.code = RIGHT(mes.MES_mkb.mkbEx, 1)))
        WHERE mes.MES_mkb.master_id = %s
        and mes.MES_mkb.deleted = 0
        """%(masterId)


class CMesMKBInfo(CInfo):
    def __init__(self,  context, row):
        CInfo.__init__(self, context)
        self.record = row

    def _load(self):
        if self.record:
            self._code = forceString(self.record.value('code'))
            self._name = forceString(self.record.value('name'))
            self._exCode = forceString(self.record.value('exCode'))
            self._exName = forceString(self.record.value('exName'))
            self._grouping = forceString(self.record.value('grouping'))
            self._blending = forceString(self.record.value('blending'))

    code = property(lambda self: self.load()._code)
    name = property(lambda self: self.load()._name)
    exCode = property(lambda self: self.load()._exCode)
    exName = property(lambda self: self.load()._exName)
    grouping = property(lambda self: self.load()._grouping)
    blending = property(lambda self: self.load()._blending)


class CServiceTypeInfoList(CInfoList):
    def __init__(self,  context, id):
        CInfoList.__init__(self, context)
        self.masterId = id

    def _load(self):
        rows = []
        query = QtGui.qApp.db.query(self.getServicesQuery(self.masterId))
        while query.next():
            rows.append(query.record())
        self._items = [ self.getInstance(CServiceTypeInfo, row) for row in rows ]
        return True

    def getServicesQuery(self, masterId):
        return u"""
        SELECT mes.mrbServiceGroup.name as `groupName`,
        mes.mrbService.code as `code`,
        mes.mrbService.name as `name`,
        mes.mrbService.doctorWTU as `doctorWTU`,
        mes.mrbService.paramedicalWTU as `paramedicalWTU`,
        mes.MES_service.averageQnt as `averageQnt`,
        mes.MES_service.necessity as `necessity`,
        mes.MES_service.groupCode as `groupCode`,
        mes.MES_service.binding as `binding`,
        IF(sex = 1, 'М', IF(sex = 2, 'Ж', 'не определено')) as `sex`,
        IF(begAgeUnit = 1, 'Д', IF(begAgeUnit = 2, 'Н', IF(begAgeUnit = 3, 'М', IF(begAgeUnit = 4, 'Г','не определено')))) as `begAgeUnit`,
        minimumAge as `minimumAge`,
        IF(endAgeUnit = 1, 'Д', IF(endAgeUnit = 2, 'Н', IF(endAgeUnit = 3, 'М', IF(endAgeUnit = 4, 'Г','не определено')))) as `endAgeUnit`,
        maximumAge as `maximumAge`,
        IF(controlPeriod = 1, 'Конец года случая', IF(controlPeriod = 2, 'Конец предыдущего случаю года', 'Дата случая')) as `controlPeriod`
        FROM mes.MES_service
        LEFT JOIN mes.mrbService ON mes.mrbService.id = mes.MES_service.service_id
        LEFT JOIN mes.mrbServiceGroup ON mes.mrbServiceGroup.id = mes.mrbService.group_id
        WHERE master_id = %d
        and mes.MES_service.deleted = 0
        """%masterId


class CServiceTypeInfo(CInfo):
    def __init__(self,  context, row):
        CInfo.__init__(self, context)
        self.record = row

    def _load(self):
        if self.record:
            self._groupName = forceString(self.record.value('groupName'))
            self._code = forceString(self.record.value('code'))
            self._name = forceString(self.record.value('name'))
            self._doctorWTU = forceString(self.record.value('doctorWTU'))
            self._paramedicalWTU = forceString(self.record.value('paramedicalWTU'))
            self._averageQnt = forceString(self.record.value('averageQnt'))
            self._necessity = forceString(self.record.value('necessity'))
            self._groupCode = forceString(self.record.value('groupCode'))
            self._binding = forceString(self.record.value('binding'))
            self._sex = forceString(self.record.value('sex'))
            self._begAgeUnit = forceString(self.record.value('begAgeUnit'))
            self._minimumAge = forceString(self.record.value('minimumAge'))
            self._endAgeUnit = forceString(self.record.value('endAgeUnit'))
            self._maximumAge = forceString(self.record.value('maximumAge'))
            self._controlPeriod = forceString(self.record.value('controlPeriod'))

    groupName = property(lambda self: self.load()._groupName)
    code = property(lambda self: self.load()._code)
    name = property(lambda self: self.load()._name)
    doctorWTU = property(lambda self: self.load()._doctorWTU)
    paramedicalWTU = property(lambda self: self.load()._paramedicalWTU)
    averageQnt = property(lambda self: self.load()._averageQnt)
    necessity = property(lambda self: self.load()._necessity)
    groupCode = property(lambda self: self.load()._groupCode)
    binding = property(lambda self: self.load()._binding)
    sex = property(lambda self: self.load()._sex)
    begAgeUnit = property(lambda self: self.load()._begAgeUnit)
    minimumAge = property(lambda self: self.load()._minimumAge)
    endAgeUnit = property(lambda self: self.load()._endAgeUnit)
    maximumAge = property(lambda self: self.load()._maximumAge)
    controlPeriod = property(lambda self: self.load()._controlPeriod)


class CVisitTypeInfoList(CInfoList):
    def __init__(self,  context, id):
        CInfoList.__init__(self, context)
        self.masterId = id

    def _load(self):
        rows = []
        query = QtGui.qApp.db.query(self.getVisitsQuery(self.masterId))
        while query.next():
            rows.append(query.record())
        self._items = [ self.getInstance(CVisitTypeInfo, row) for row in rows ]
        return True

    def getVisitsQuery(self, masterId):
        return u"""
        SELECT mes.mrbVisitType.name as `name`,
        mes.mrbSpeciality.name as `specialityName`,
        mes.MES_visit.serviceCode as `serviceCode`,
        mes.MES_visit.additionalServiceCode as `additionalServiceCode`,
        mes.MES_visit.altAdditionalServiceCode as `altAdditionalServiceCode`,
        mes.MES_visit.groupCode as `groupCode`,
        mes.MES_visit.averageQnt as `averageQnt`,
        IF(sex = 1, 'М', IF(sex = 2, 'Ж', 'не определено')) as `sex`,
        IF(begAgeUnit = 1, 'Д', IF(begAgeUnit = 2, 'Н', IF(begAgeUnit = 3, 'М', IF(begAgeUnit = 4, 'Г','не определено')))) as `begAgeUnit`,
        minimumAge as `minimumAge`,
        IF(endAgeUnit = 1, 'Д', IF(endAgeUnit = 2, 'Н', IF(endAgeUnit = 3, 'М', IF(endAgeUnit = 4, 'Г','не определено')))) as `endAgeUnit`,
        maximumAge as `maximumAge`,
        IF(controlPeriod = 1, 'Конец года случая', IF(controlPeriod = 2, 'Конец предыдущего случаю года', 'Дата случая')) as `controlPeriod`
        FROM mes.MES_visit
        LEFT JOIN mes.mrbVisitType ON mes.mrbVisitType.id = mes.MES_visit.visitType_id
        LEFT JOIN mes.mrbSpeciality ON mes.mrbSpeciality.id = mes.MES_visit.speciality_id
        WHERE master_id = %d
        and mes.MES_visit.deleted = 0
        """%masterId


class CVisitTypeInfo(CInfo):
    def __init__(self,  context, row):
        CInfo.__init__(self, context)
        self.record = row

    def _load(self):
        if self.record:
            self._name = forceString(self.record.value('name'))
            self._specialityName = forceString(self.record.value('specialityName'))
            self._serviceCode = forceString(self.record.value('serviceCode'))
            self._additionalServiceCode = forceString(self.record.value('additionalServiceCode'))
            self._altAdditionalServiceCode = forceString(self.record.value('altAdditionalServiceCode'))
            self._groupCode = forceString(self.record.value('groupCode'))
            self._averageQnt = forceString(self.record.value('averageQnt'))
            self._sex = forceString(self.record.value('sex'))
            self._begAgeUnit = forceString(self.record.value('begAgeUnit'))
            self._minimumAge = forceString(self.record.value('minimumAge'))
            self._endAgeUnit = forceString(self.record.value('endAgeUnit'))
            self._maximumAge = forceString(self.record.value('maximumAge'))
            self._controlPeriod = forceString(self.record.value('controlPeriod'))

    name = property(lambda self: self.load()._name)
    specialityName = property(lambda self: self.load()._specialityName)
    serviceCode = property(lambda self: self.load()._serviceCode)
    additionalServiceCode = property(lambda self: self.load()._additionalServiceCode)
    altAdditionalServiceCode = property(lambda self: self.load()._altAdditionalServiceCode)
    groupCode = property(lambda self: self.load()._groupCode)
    averageQnt = property(lambda self: self.load()._averageQnt)
    sex = property(lambda self: self.load()._sex)
    begAgeUnit = property(lambda self: self.load()._begAgeUnit)
    minimumAge = property(lambda self: self.load()._minimumAge)
    endAgeUnit = property(lambda self: self.load()._endAgeUnit)
    maximumAge = property(lambda self: self.load()._maximumAge)
    controlPeriod = property(lambda self: self.load()._controlPeriod)


class CMesInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('mes.MES', '*', self.id)
        if record:
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._descr = forceString(record.value('descr'))
            self._service = self.getInstance(CServiceInfo, forceRef(db.translate('rbService', 'code', self._code, 'id')))
            self._active = forceInt(record.value('active'))
            self._internal =  forceInt(record.value('internal'))
            self._group = self.getInstance(CMesGroupInfo, forceRef(record.value('group_id')))
            self._min = forceInt(record.value('minDuration'))
            self._max = forceInt(record.value('maxDuration'))
            self._avg = forceInt(record.value('avgDuration'))
            self._patientModel = forceString(record.value('patientModel'))
            self._norm = forceInt(record.value('KSGNorm'))
            self._periodicity = forceInt(record.value('periodicity'))
            self._ksg = self.getInstance(CKSGInfo, forceRef(record.value('ksg_id')))
            self._endDate = CDateInfo(forceDate(record.value('endDate')))
            self._isPolyTrauma = forceInt(record.value('isPolyTrauma'))
            self._MKB = self.getInstance(CMKBInfoList, forceRef(record.value('id')))
            self._serviceTypes = self.getInstance(CServiceTypeInfoList, forceRef(record.value('id')))
            self._visitTypes  = self.getInstance(CVisitTypeInfoList, forceRef(record.value('id')))
            return True
        else:
            self._code = ''
            self._name = ''
            self._descr = ''
            self._service = None
            self._active = 1
            self._internal = 0
            self._group = self.getInstance(CMesGroupInfo, None)
            self._min = 0
            self._max = 0
            self._avg = 0
            self._patientModel = ''
            self._norm = 0
            self._periodicity = 0
            self._ksg = self.getInstance(CKSGInfo, None)
            self._endDate = CDateInfo()
            self._isPolyTrauma = 0
            self._MKB = self.getInstance(CMKBInfoList, None)
            self._serviceTypes = self.getInstance(CServiceTypeInfoList, None)
            self._visitTypes = self.getInstance(CVisitTypeInfoList, None)
            return False

    code  = property(lambda self: self.load()._code)
    name  = property(lambda self: self.load()._name)
    descr = property(lambda self: self.load()._descr)
    service = property(lambda self: self.load()._service)
    active = property(lambda self: self.load()._active)
    internal = property(lambda self: self.load()._internal)
    group = property(lambda self: self.load()._group)
    min =  property(lambda self: self.load()._min)
    max = property(lambda self: self.load()._max)
    avg = property(lambda self: self.load()._max)
    patientModel = property(lambda self: self.load()._max)
    norm = property(lambda self: self.load()._norm)
    periodicity =  property(lambda self: self.load()._periodicity)
    ksg = property(lambda self: self.load()._ksg)
    endDate = property(lambda self: self.load()._endDate)
    isPolyTrauma = property(lambda self: self.load()._isPolyTrauma)
    MKB = property(lambda self: self.load()._MKB)
    serviceTypes = property(lambda self: self.load()._serviceTypes)
    visitTypes = property(lambda self: self.load()._visitTypes)
