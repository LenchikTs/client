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

from PyQt4         import QtGui
from PyQt4.QtCore  import QDate, pyqtSignature

from library.DialogBase import CDialogBase
from library.InDocTable import CRecordListModel, CBoolInDocTableCol, CDateTimeInDocTableCol, CInDocTableCol, CRBInDocTableCol
from library.Utils      import firstYearDay

from Orgs.Utils         import getOrgStructureDescendants
from Registry.Utils     import getClientBanner

from Registry.Ui_VisitsBySchedules import Ui_VisitsBySchedules


class CVisitsBySchedulesDialog(CDialogBase, Ui_VisitsBySchedules):
    def __init__(self,  parent, clientId, orgStructureId = None, specialityId = None, personId = None):
        CDialogBase.__init__(self, parent)
        self.addModels('VisitsBySchedules', CVisitsBySchedulesModel(self))
        self.addObject('btnPrint',  QtGui.QPushButton(u'Печать', self))
        self.addObject('btnCreate', QtGui.QPushButton(u'Создать', self))

        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', order='name')
        self.setModels(self.tblSchedules, self.modelVisitsBySchedules, self.selectionModelVisitsBySchedules)
        self.buttonBox.addButton(self.btnCreate, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnPrint,  QtGui.QDialogButtonBox.ActionRole)

        self.clientId = clientId
        self.setup(orgStructureId, specialityId, personId)


    def setup(self, orgStructureId, specialityId, personId):
        yesterday = QDate.currentDate().addDays(-1)
        self.edtBegDate.setDate(firstYearDay(yesterday))
        self.edtEndDate.setDate(yesterday)
        self.cmbOrgStructure.setValue(orgStructureId)
        self.cmbSpeciality.setValue(specialityId)
        self.cmbPerson.setValue(personId)
        self.txtClient.setHtml(getClientBanner(self.clientId))


    @pyqtSignature('')
    def on_btnCreate_clicked(self):
        if self.clientId:
            beginDate = self.edtBegDate.date()
            endDate   = self.edtEndDate.date()
            orgStructureId = self.cmbOrgStructure.value()
            specialityId = self.cmbSpeciality.getValue()
            personId = self.cmbPerson.getValue()
            self.modelVisitsBySchedules.loadData(self.chkShowQueueWithoutVisit.isChecked(),
                                            self.clientId,
                                            beginDate,
                                            endDate,
                                            orgStructureId,
                                            specialityId,
                                            personId)


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        if self.clientId and self.modelVisitsBySchedules.rowCount() > 0:
            self.tblSchedules.setReportHeader(u'Протокол обращений пациента по предварительной записи')
            self.tblSchedules.setReportDescription(getClientBanner(self.clientId))
            mask = [True]*(self.modelVisitsBySchedules.columnCount())
            self.tblSchedules.printContent(mask)


#    @pyqtSignature('')
#    def on_btnCancelVisitBeforeRecordClient_clicked(self):
#        self.tblSchedules.setModel(None)
#        self.close()


class CVisitsBySchedulesModel(CRecordListModel):
    def __init__(self,  parent):
        CRecordListModel.__init__(self, parent)
        self.addCol(CBoolInDocTableCol(u'Выполнено', 'event_id', 6)).setReadOnly()
        self.addCol(CDateTimeInDocTableCol(u'Дата и время приема', 'date', 20)).setReadOnly()
        self.addCol(CInDocTableCol(u'Каб',          'office', 6)).setReadOnly()
        self.addCol(CRBInDocTableCol(u'Специалист', 'person_id', 20, 'vrbPersonWithSpeciality')).setReadOnly()
        self.addCol(CRBInDocTableCol(u'Записал',    'createPerson_id', 20, 'vrbPersonWithSpeciality')).setReadOnly()
        self.addCol(CInDocTableCol(u'Примечания',   'note', 6)).setReadOnly()


    def loadData(self, showQueueWithoutVisit, clientId, begDate, endDate, orgStructureId, specialityId, personId):
        if clientId:
            db   = QtGui.qApp.db
            stmt =  'SELECT '                                                                       \
                    ' vVisitExt.event_id,'                                                          \
                    ' IFNULL(vVisitExt.date,      Schedule_Item.time) AS date,'                     \
                    ' IFNULL(vVisitExt.person_id, Schedule.person_id) AS person_id,'                \
                    ' Schedule.office,'                                                             \
                    ' Schedule_Item.recordPerson_id,'                                               \
                    ' Schedule_Item.complaint '                                                     \
                    'FROM'                                                                          \
                    ' Schedule_Item'                                                                \
                    ' LEFT JOIN Schedule     ON Schedule.id      = Schedule_Item.master_id'         \
                    ' LEFT JOIN Person       ON Person.id        = Schedule.person_id'              \
                    ' LEFT JOIN vVisitExt    ON vVisitExt.client_id = Schedule_Item.client_id '     \
                                              ' AND Person.speciality_id=vVisitExt.speciality_id'   \
                                              ' AND DATE(vVisitExt.date) = Schedule.date'           \
                    ' WHERE Schedule_Item.client_id =%(clientId)d'                                  \
                      ' AND %(cond)s'                                                               \
                    ' ORDER BY date'
            tableSchedule = db.table('Schedule')
            tablePerson   = db.table('Person')
            tableVisit    = db.table('vVisitExt')
            cond = [ 'Schedule_Item.deleted=0',
                     'Schedule.deleted=0',
                   ]
            if not showQueueWithoutVisit:
                cond.append('vVisitExt.event_id IS NOT NULL')
            if begDate:
                cond.append(tableSchedule['date'].ge(begDate))
            if endDate:
                cond.append(tableSchedule['date'].le(endDate))
            if orgStructureId:
                cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
            if specialityId:
                cond.append(tablePerson['speciality_id'].eq(specialityId))
            if personId:
                cond.append(db.joinOr([tableSchedule['person_id'].eq(personId),
                                       tableVisit['person_id'].eq(personId)
                                      ]
                                     )
                           )
            query = db.query(stmt%dict(clientId  = clientId,
                                       cond      = db.joinAnd(cond)
                                      )
                            )
            items = []
            while query.next():
                items.append(query.record())
            self.setItems(items)
        else:
            self.clearItems()
