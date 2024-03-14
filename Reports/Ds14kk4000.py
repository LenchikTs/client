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

from PyQt4 import QtGui
from PyQt4.QtCore import *
from Reports.Report     import CReport
from Reports.ReportBase import *
from Reports.Ds14kk1000 import CDs14kkHelpers
from Ui_Ds14kkSetupDialog import Ui_ds14kkSetupDialog
from library.Utils import forceString, forceInt, forceDouble
from Reports.Ds14kk1000 import CDs14kkSetupDialog


class CReportDs14kk4000(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Направлены в райвоенкомат')

    def getSetupDialog(self, parent):
        result = CDs14kkSetupDialog(parent)
        #self.stationaryF14DCSetupDialog = result
        return result

    def selectData(self, params):
        stmt = u'''
select count(distinct Client.id) as cnt from Event
inner join Action on Action.id = (select max(a.id) from Action a
								 left join ActionType at on at.id = a.actionType_id
                                 where a.event_id = Event.id and at.flatcode like 'voenkom' and at.name like 'Направление в райвоенкомат'
                                 )
left join Client on Client.id = Event.client_id
left join Person on Person.id = Action.person_id
left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = (
    select ActionProperty_HospitalBed.value
    from Action as HospitalAction
    left join ActionPropertyType on ActionPropertyType.name = 'койка'
    and ActionPropertyType.actionType_id = HospitalAction.actionType_id and ActionPropertyType.deleted = 0
    left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id
        and ActionProperty.action_id = HospitalAction.id and ActionProperty.deleted = 0
    left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
    where HospitalAction.id = (SELECT MAX(A.id) FROM Action A
                WHERE A.event_id = Event.id AND A.deleted = 0 AND A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                                    AND AT.deleted = 0)
                                )

)
left join OrgStructure on OrgStructure_HospitalBed.master_id = OrgStructure.id
left join rbHospitalBedShedule on rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
left join Contract on  Contract.id = Event.contract_id
where
rbHospitalBedShedule.code = 2 and Event.deleted = 0 and %(cond)s

        '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params, 2)}
        return db.query(st)


    def build(self, params):
        report = [0]
        def processQuery(query):
            while query.next():
                record = query.record()
                report[0] += forceInt(record.value("cnt"))


        processQuery(self.selectData(params))
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'4. Направлены в райвоенкомат')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        CDs14kkHelpers.splitTitle(cursor, u'(4000)', u'Коды по ОКЕИ: человек - 792')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(
            u'Из общего числа выписанных (гр. 4 и 7 таблиц 3000 и 3500)')
        cursor.insertText(u'\r\nнаправлены райвоенкоматом: %d' % report[0])
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(4100)', u'Коды по ОКЕИ: человек - 792')
        cursor.insertText(
            u'Лица, госпитализированные для обследования и оказавшиеся здоровыми:')
        cursor.insertText(u'\r\nвзрослые: -')
        cursor.insertText(u'\r\nиз них призывники: -')
        cursor.insertText(u'\r\nдети: -')
        cursor.insertText(u'\r\nиз них призывники: -')
        cursor.insertBlock()
        CDs14kkHelpers.writeFooter(cursor)
        return doc
