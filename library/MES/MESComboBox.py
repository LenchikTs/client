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
from PyQt4.QtCore import SIGNAL, QDate

from library.crbcombobox import CRBComboBox
from library.MES.MESComboBoxPopup import CMESComboBoxPopup
from library.Utils                import calcAgeTuple


class CMESComboBox(CRBComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None):
        CRBComboBox.__init__(self, parent)
        self._popup=None
        self.mesId=None
        self.clientSex = 0
        self.baseDate = None
        self.clientBirthDate = None
        self.clientAge = None
        self.clientAgePrevYearEnd = None
        self.clientAgeCurrYearEnd = None
        self.eventProfileId = None
        self.eventBegDate = None
        self.mesCodeTemplate = ''
        self.mesServiceTemplate = ''
        self.mesNameTemplate = ''
        self.specialityId = None
        self.MKB = ''
        self.AssociatedMKB = ''
        self.ComplicationMKB = ''
        self.MKBEx = ''
        self._tableName = 'mes.MES'
        self._addNone = True
        self._customFilter = None
        CRBComboBox.setTable(self, self._tableName, self._addNone, self.compileFilter(), self._order)
        self.setShowFields(CRBComboBox.showCodeAndName)
        self.contractId = None
        self.execDate = None
        self.eventTypeId = None
        self.criteriaList = None
        self.fractions = None


    def setEventBegDate(self, date):
        self.eventBegDate = date


    def setClientSex(self, clientSex):
        self.clientSex = clientSex

    def setContractId(self, contractId):
        self.contractId = contractId

    def setExecDate(self, execDate):
        self.execDate = execDate if execDate else QDate.currentDate()

    def setEventTypeId(self, eventTypeId):
        self.eventTypeId = eventTypeId

    def setAdditionalCriteria(self, criteriaList):
        self.criteriaList = criteriaList

    def setFractions(self, fractions):
        self.fractions = fractions

    def setClientAge(self, baseDate, clientBirthDate, clientAge, clientAgePrevYearEnd, clientAgeCurrYearEnd):
        self.baseDate = baseDate
        self.clientBirthDate = clientBirthDate
        self.clientAge = clientAge
        self.clientAgePrevYearEnd = clientAgePrevYearEnd
        self.clientAgeCurrYearEnd = clientAgeCurrYearEnd


    def getClientAgeSex(self):
        return (self.baseDate, self.clientBirthDate, self.clientAge, self.clientAgePrevYearEnd, self.clientAgeCurrYearEnd, self.clientSex)


    def setEventProfile(self, eventProfileId):
        self.eventProfileId = eventProfileId


    def setMESCodeTemplate(self, mesCodeTemplate):
        self.mesCodeTemplate = mesCodeTemplate


    def setMESNameTemplate(self, mesNameTemplate):
        self.mesNameTemplate = mesNameTemplate


    def setMESServiceTemplate(self, mesServiceTemplate):
        self.mesServiceTemplate = mesServiceTemplate


    def setSpeciality(self, specialityId):
        self.specialityId = specialityId


    def setMKB(self, MKB):
        self.MKB = MKB


    def setAssociatedMKB(self, MKB):
        self.AssociatedMKB = MKB


    def setComplicationMKB(self, MKB):
        self.ComplicationMKB = MKB


    def setMKBEx(self, MKBEx):
        self.MKBEx = MKBEx


    def showPopup(self):
        if not self._popup:
            self._popup = CMESComboBoxPopup(self)
            self.connect(self._popup, SIGNAL('MESSelected(int)'), self.setValue)
        pos = self.mapToGlobal(self.rect().bottomLeft())
        size = self._popup.sizeHint()
        width= max(size.width(), self.width())
        size.setWidth(width)
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()
        self._popup.setup(self.baseDate, self.clientSex, self.clientBirthDate, self.clientAge,
                          self.clientAgePrevYearEnd, self.clientAgeCurrYearEnd, self.eventProfileId,
                          self.mesCodeTemplate, self.mesNameTemplate, self.mesServiceTemplate,
                          self.specialityId, self.MKB, self.AssociatedMKB, self.ComplicationMKB, self.MKBEx, self.value(), self.eventBegDate,
                          self.contractId, self.execDate, self.eventTypeId, self.criteriaList, self.fractions)


#    def setValue(self, mesId):
#        self.mesId = mesId


#    def value(self):
#        return self.mesId


#    @staticmethod
#    def getText(mesId):
#        if mesId:
#            db = QtGui.qApp.db
#            table = db.table('mes.MES')
#            record = db.getRecordEx(table, ['code','name'], [table['id'].eq(mesId), table['deleted'].eq(0)])
#            if record:
#                code = forceString(record.value('code'))
#                name = forceString(record.value('name'))
#                text = code + ' | ' + name
#            else:
#                text = '{%s}' % mesId
#        else:
#            text = ''
#        return text


#    def updateText(self):
#        self.setEditText(self.getText(self.mesId))


    def compileFilter(self):
        db = QtGui.qApp.db
        tableMES = db.table('mes.MES')
        tableMESService = db.table('mes.MES_service')
        tableMESRBService = db.table('mes.mrbService')
        queryTable = tableMES
        cond  = [tableMES['deleted'].eq(0)]
        if self.eventProfileId:
            tableMESGroup = db.table('mes.mrbMESGroup')
            tableEventProfile = db.table('rbEventProfile')
            queryTable = queryTable.leftJoin(tableMESGroup, tableMESGroup['id'].eq(tableMES['group_id']))
            queryTable = queryTable.leftJoin(tableEventProfile, tableEventProfile['regionalCode'].eq(tableMESGroup['code']))
            cond.append(db.joinOr([tableEventProfile['id'].eq(self.eventProfileId), tableMESGroup['id'].isNull(), '''TRIM(mes.mrbMESGroup.code) = '' ''']))
        if self.mesCodeTemplate:
            cond.append(tableMES['code'].regexp(self.mesCodeTemplate))
        if self.mesNameTemplate:
            cond.append(tableMES['name'].regexp(self.mesNameTemplate))
        if self.eventBegDate:
            cond.append(db.joinOr([tableMES['endDate'].isNull(), tableMES['endDate'].ge(self.eventBegDate)]))
        if self.clientSex or self.clientAge:
            tableMESLimitedBySexAge = db.table('mes.MES_limitedBySexAge')
            queryTable = queryTable.leftJoin(tableMESLimitedBySexAge, tableMESLimitedBySexAge['master_id'].eq(tableMES['id']))
            sexStr = ''
            ageStr = ''
            if self.clientSex:
                sexStr = u''' AND mes.MES_limitedBySexAge.sex = %d'''%(self.clientSex)
            if self.clientAge:
                clientAge = self.clientAge[3]
                clientAgeMonths = self.clientAge[2]
                if clientAge == 0:
                    clientAge = round(clientAgeMonths / 12.0, 2)
                if self.clientAgePrevYearEnd is None:
                    self.clientAgePrevYearEnd = self.clientAgeCurrYearEnd
                    if self.baseDate and self.clientBirthDate:
                        self.clientAgeCurrYearEnd = calcAgeTuple(self.clientBirthDate, QDate(self.baseDate.year(), 12, 31))
                clientAgeCurrYearEnd = self.clientAgeCurrYearEnd[3]
                clientAgeMonthsCurrYear = self.clientAgeCurrYearEnd[2]
                if clientAgeCurrYearEnd == 0:
                    clientAgeCurrYearEnd = round(clientAgeMonthsCurrYear / 12.0, 2)
                clientAgePrevYearEnd = self.clientAgePrevYearEnd[3]
                clientAgeMonthsPrevYear = self.clientAgePrevYearEnd[2]
                if clientAgePrevYearEnd == 0:
                    clientAgePrevYearEnd = round(clientAgeMonthsPrevYear / 12.0, 2)
                ageStr = u''' AND mes.MES_limitedBySexAge.minimumAge <= (
                IF(mes.MES_limitedBySexAge.begAgeUnit = 1,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.begAgeUnit = 2,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.begAgeUnit = 3,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.begAgeUnit = 4,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)))))))
                AND mes.MES_limitedBySexAge.maximumAge >= (
                IF(mes.MES_limitedBySexAge.endAgeUnit = 1,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.endAgeUnit = 2,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.endAgeUnit = 3,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.endAgeUnit = 4,
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s)),
                IF(mes.MES_limitedBySexAge.controlPeriod = 1, %s, IF(mes.MES_limitedBySexAge.controlPeriod = 2, %s, %s))
                )))))
                '''%(u'%.2f'%(self.clientAgeCurrYearEnd[0]), u'%.2f'%(self.clientAgePrevYearEnd[0]), u'%.2f'%(self.clientAge[0]),
                u'%.2f'%(self.clientAgeCurrYearEnd[1]), u'%.2f'%(self.clientAgePrevYearEnd[1]), u'%.2f'%(self.clientAge[1]),
                u'%.2f'%(self.clientAgeCurrYearEnd[2]),u'%.2f'%(self.clientAgePrevYearEnd[2]),u'%.2f'%(self.clientAge[2]),
                u'%.2f'%(self.clientAgeCurrYearEnd[3]), u'%.2f'%(self.clientAgePrevYearEnd[3]), u'%.2f'%(self.clientAge[3]),
                u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge),
                u'%.2f'%(self.clientAgeCurrYearEnd[0]), u'%.2f'%(self.clientAgePrevYearEnd[0]), u'%.2f'%(self.clientAge[0]),
                u'%.2f'%(self.clientAgeCurrYearEnd[1]), u'%.2f'%(self.clientAgePrevYearEnd[1]), u'%.2f'%(self.clientAge[1]),
                u'%.2f'%(self.clientAgeCurrYearEnd[2]),u'%.2f'%(self.clientAgePrevYearEnd[2]),u'%.2f'%(self.clientAge[2]),
                u'%.2f'%(self.clientAgeCurrYearEnd[3]), u'%.2f'%(self.clientAgePrevYearEnd[3]), u'%.2f'%(self.clientAge[3]),
                u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge)
                )
            sexAgeStr = u'''NOT EXISTS(SELECT MES_limitedBySexAge.id FROM mes.MES_limitedBySexAge AS MES_limitedBySexAge
                  WHERE mes.MES.`id` = MES_limitedBySexAge.`master_id` AND MES_limitedBySexAge.`master_id` IS NOT NULL AND MES_limitedBySexAge.deleted = 0
                  LIMIT 1) OR (mes.MES_limitedBySexAge.deleted = 0%s%s)'''%(sexStr, ageStr)
            cond.append(sexAgeStr)
        if self.specialityId:
            regionalCode = db.translate('rbSpeciality', 'id', self.specialityId, 'regionalCode')
            tableMESVisit      = db.table('mes.MES_visit')
            tableMESSpeciality = db.table('mes.mrbSpeciality')
            tableMESVisitType  = db.table('mes.mrbVisitType')
            subTable = tableMESVisit.leftJoin(tableMESVisitType,  tableMESVisitType['id'].eq(tableMESVisit['visitType_id']))
            subTable = subTable.leftJoin(tableMESSpeciality, tableMESSpeciality['id'].eq(tableMESVisit['speciality_id']))
            tableMESVisitType
            subCond  = [tableMESVisit['master_id'].eq(tableMES['id']),
                        tableMESVisit['deleted'].eq(0),
                        tableMESSpeciality['regionalCode'].eq(regionalCode)
                       ]
            cond.append(db.joinOr([db.existsStmt(subTable, subCond),
                                   'NOT '+db.existsStmt(tableMESVisit, tableMESVisit['master_id'].eq(tableMES['id']))
                                  ]))
        if self.mesServiceTemplate:
            queryTable = queryTable.innerJoin(tableMESService, tableMESService['master_id'].eq(tableMES['id']))
            queryTable = queryTable.innerJoin(tableMESRBService, tableMESRBService['id'].eq(tableMESService['service_id']))
            joinOr = []
            for mesService in self.mesServiceTemplate:
                joinOr.append(u'''mes.mrbService.code LIKE '%s' '''%(mesService))
            cond.append(db.joinOr(joinOr))
            cond.append(tableMESService['deleted'].eq(0))
            cond.append(tableMESRBService['deleted'].eq(0))
        if self.MKB:
            tableMESMkb  = db.table('mes.MES_mkb')
            # строгое соответствие
            subCond = tableMESMkb['mkb'].inlist([self.MKB])
            subCond  = [ tableMESMkb['master_id'].eq(tableMES['id']),
                         tableMESMkb['deleted'].eq(0),
                         subCond
                       ]
            cond.append(db.existsStmt(tableMESMkb, subCond))
        cond.append(tableMES['active'].eq(1))
        return db.joinAnd(cond)


    def updateFilter(self):
        v = self.value()
        CRBComboBox.setTable(self, self._tableName, self._addNone, self.compileFilter(), self._order)
        self.setValue(v)


    def lookup(self):
        i, self._searchString = self._model.searchCodeEx(self._searchString)
        if i>=0 and i!=self.currentIndex():
            self.setCurrentIndex(i)
            rowIndex = self.currentIndex()
            self.mesId = self._model.getId(rowIndex)

