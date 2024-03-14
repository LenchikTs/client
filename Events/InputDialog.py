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

from PyQt4              import QtGui
from PyQt4.QtCore       import SIGNAL, QDate, QDateTime, QTime, QVariant

from library.DialogBase import CDialogBase
from library.Utils      import forceDate, forceDateTime, forceString, forceTime

from Ui_InputDialog     import Ui_InputDialog


class CExceptionMixin:
    def raiseException(self, methodName):
        raise Exception, u'%s не имеет метода %s' % (str(self), methodName)



class CInputDialog(CExceptionMixin, CDialogBase, Ui_InputDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)

        self.setupUi(self)

        self.setWindowTitle(u'Введите данные')

        self.edtTime.setTime(QTime.currentTime())

        self.setDateTimeVisible(True)
        self.setPersonVisible(True)
        self.setPresetDateTimeVisible(False)
        self.setOrgStructureVisible(False)
        self.setExecPersonVisible(False)
        self.setCourseVisible(False)


    def setCourseVisible(self, value):
        self._courseVisible = value
        self.cmbCourse.setVisible(value)
        self.lblCourse.setVisible(value)


    def setExecPersonVisible(self, value):
        self._orgStructureVisible = value
        self.cmbExecPerson.setVisible(value)
        self.lblExecPerson.setVisible(value)


    def setOrgStructureVisible(self, value):
        self._orgStructureVisible = value
        self.cmbOrgStructure.setVisible(value)
        self.lblOrgStructure.setVisible(value)


    def setPresetDateTimeVisible(self, value):
        self._presetDateTimeVisible = value
        self.cmbPresetDateTime.setVisible(value)


    def setPersonVisible(self, value):
        self._personVisible = value
        self.cmbPerson.setVisible(value)
        self.lblPerson.setVisible(value)


    def setDateTimeVisible(self, value):
        self.lblDateTime.setVisible(value)
        self.setDateVisible(value)
        self.setTimeVisible(value)


    def setDateVisible(self, value):
        self._dateVisible = value
        self.edtDate.setVisible(value)


    def setTimeVisible(self, value):
        if value:
            self.lblDateTime.setText(u"Дата и время")
        else:
            self.lblDateTime.setText(u"Дата")
        self._timeVisible = value
        self.edtTime.setVisible(value)


    def date(self):
        return self.edtDate.date()


    def time(self):
        return self.edtTime.time()


    def dateTime(self):
        result = QDateTime()
        result.setDate(self.date())
        result.setTime(self.time())
        return result


    def execPerson(self):
        return self.cmbExecPerson.value()


    def execCourse(self):
        return self.cmbCourse.currentIndex()


    def setExecPerson(self, execPersonId):
        self.cmbExecPerson.setValue(execPersonId)


    def person(self):
        return self.cmbPerson.value()


    def setPerson(self, personId):
        self.cmbPerson.setValue(personId)

    def orgStructure(self):
        return self.cmbOrgStructure.value()


#    @pyqtSignature('int')
#    def on_cmbPresetDateTime_currentIndexChanged(self, index):
#        self.edtDate.setEnabled(bool(index))
#        self.edtTime.setEnabled(bool(index))


class CDateTimeInputDialog(CInputDialog):
    def __init__(self, parent=None, timeVisible=True, isCourseVisible=False):
        CInputDialog.__init__(self, parent)
        self.setPersonVisible(False)
        self.setCourseVisible(isCourseVisible)
        self.minimumDate = QDate()
        self.setTimeVisible(timeVisible)
        self.isCurrentDate = False


    def setCurrentDate(self, isCurrentDate = False):
        self.isCurrentDate = isCurrentDate
        self.edtDate.setCurrentDate(self.isCurrentDate)


    def person(self):
        self.raiseException('person')


    def orgStructure(self):
        self.raiseException('orgStructure')


    def setMaximumDate(self, date):
        self.edtDate.setMaximumDate(date)


    def setMinimumDate(self, date):
        self.edtDate.setMinimumDate(date)
        self.minimumDate = date


    @classmethod
    def getDateTime(cls, wgt=None, minimumDate = None):
        if wgt is None:
            if QtGui.QApplication.activeWindow():
                wgt = QtGui.QApplication.activeWindow()
            elif hasattr(QtGui.qApp, 'mainWindow') and QtGui.qApp.mainWindow is not None:
               wgt = QtGui.qApp.mainWindow
        result = CDateTimeInputDialog(wgt)
        if minimumDate:
            result.setMinimumDate(minimumDate)
        if result.exec_():
            return result.dateTime()
        return QDateTime()


class CJobTiketDoneDateTimeInputWithPresetDialog(CDateTimeInputDialog):
    def __init__(self, parent=None, clientId=None):
        CDateTimeInputDialog.__init__(self, parent)
        self.setPresetDateTimeVisible(True)
        self._parent = parent
        self._clientId = clientId
        self.connect(self.edtDate, SIGNAL('dateChanged(QDate)'), self.on_dateChanged)
        self.on_dateChanged()


    def presetDateTimeValue(self):
        if self.cmbPresetDateTime.isEnabled():
            itemIndex = self.cmbPresetDateTime.currentIndex()
            if itemIndex:
                return self.cmbPresetDateTime.itemData(itemIndex)
        return None


    def date(self):
        result = self.presetDateTimeValue()
        if result is not None:
            return forceDate(result)
        return CInputDialog.date(self)


    def time(self):
        result = self.presetDateTimeValue()
        if result is not None:
            return forceTime(result)
        return CInputDialog.time(self)


    def dateTime(self):
        result = self.presetDateTimeValue()
        if result is not None:
            return forceDateTime(result)
        return CInputDialog.dateTime(self)


    def setPresetDateTimeValues(self, values):
        self.cmbPresetDateTime.clear()
        self.cmbPresetDateTime.setEnabled(bool(values))
        if values:
            self.cmbPresetDateTime.addItem(u'', QVariant(QDateTime()))
            for strValue, value in values:
                self.cmbPresetDateTime.addItem(strValue, QVariant(value))


    def on_dateChanged(self):
        presetValues = self.getPresetValues()
        self.setPresetDateTimeValues(presetValues)


    def getPresetValues(self):
        jobTicketIdList, jobTypeIdList = self._parent.getCondForDateTimeSearching()
        date = self.edtDate.date()
        clientId = self._clientId
        if jobTypeIdList and date and clientId:
            db = QtGui.qApp.db
            tableJobTicket = db.table('Job_Ticket')
            tableJob = db.table('Job')
            tableAPJT = db.table('ActionProperty_Job_Ticket')
            tableAP = db.table('ActionProperty')
            tableAction = db.table('Action')
            tableEvent = db.table('Event')
            tablePerson = db.table('vrbPersonWithSpeciality')
            queryTable = tableAPJT.leftJoin(tableAP, tableAP['id'].eq(tableAPJT['id']))
            queryTable = queryTable.leftJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
            queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
            queryTable = queryTable.leftJoin(tableJobTicket, tableJobTicket['id'].eq(tableAPJT['value']))
            queryTable = queryTable.leftJoin(tableJob, tableJob['id'].eq(tableJobTicket['master_id']))
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
            cond = [tableEvent['client_id'].eq(clientId),
                    tableJob['jobType_id'].inlist(jobTypeIdList),
                    tableAction['endDate'].dateEq(date)]
            fields = [tableAction['endDate'], tablePerson['name']]
            recordList = db.getRecordList(queryTable, fields, cond, tableAction['endDate'].name())
            result = []
            for record in recordList:
                personName = forceString(record.value('name'))
                endDate = forceDateTime(record.value('endDate'))
                strValue = personName + ' | ' + forceString(endDate)
                item = (strValue, endDate)
                if not item in result:
                    result.append(item)
            return result
        return []


class COrgStructureInputDialog(CInputDialog):
    def __init__(self, parent=None):
        CInputDialog.__init__(self, parent)
        self.setPersonVisible(False)
        self.setDateTimeVisible(False)
        self.setOrgStructureVisible(True)
        self.cmbOrgStructure.setExpandAll(True)

    def person(self):
        self.raiseException('person')

    def date(self):
        self.raiseException('date')

    def time(self):
        self.raiseException('time')

    def dateTime(self):
        self.raiseException('dateTime')

    def setFilter(self, filter):
        self.cmbOrgStructure.setFilter(filter)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    print CDateTimeInputDialog.getDateTime()
    app.exec_()

