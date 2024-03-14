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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QAbstractTableModel, QEvent, QVariant

from Events.Action import CAction
from Events.Utils       import inMedicalDiagnosis, getActionTypeIdListByFlatCode

from library.TableModel import CCol
from library.Utils      import forceString, forceStringEx, getPref, setPref, toVariant


from Ui_MedicalDiagnosisComboBoxExPopup import Ui_MedicalDiagnosisComboBoxExPopup


class CMedicalDiagnosisComboBoxPopup(QtGui.QFrame, Ui_MedicalDiagnosisComboBoxExPopup):
    __pyqtSignals__ = ('medicalDiagnosisSelected(QString)',
                      )

    def __init__(self, parent = None, eventId = None, date = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CMedicalDiagnosisTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblMedicalDiagnosis.setModel(self.tableModel)
        self.tblMedicalDiagnosis.setSelectionModel(self.tableSelectionModel)
        self.tblMedicalDiagnosis.installEventFilter(self)
        self.eventId = eventId
        self.date = date
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CMedicalDiagnosisComboBoxExPopup', {})
        self.tblMedicalDiagnosis.loadPreferences(preferences)
        self._parent = parent
        self._customFilter = None
        self.tableModel.loadData(self.eventId, self.date, self._customFilter)


    def addNotSetValue(self):
        self.tableModel.addNotSetValue()


    def setFilter(self, filter):
        if self._customFilter != filter:
            self._customFilter = filter
            self.tableModel.loadData(self.eventId, self.date, self._customFilter)


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblMedicalDiagnosis.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CMedicalDiagnosisComboBoxExPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblMedicalDiagnosis:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblMedicalDiagnosis.currentIndex()
                self.tblMedicalDiagnosis.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    def getCurrentMedicalDiagnosis(self):
        currentIndex = self.tblMedicalDiagnosis.currentIndex()
        if currentIndex and currentIndex.isValid():
            row = currentIndex.row()
            if row is not None and row >= 0 and row < self.tableModel.rowCount():
                item = self.tableModel.items[row]
                return item[0][0] if item else u''
        return u''


    def getMedicalDiagnosis(self, result):
        self.emit(SIGNAL('medicalDiagnosisSelected(QString)'), result)
        self.close()


    @pyqtSignature('QModelIndex')
    def on_tblMedicalDiagnosis_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                medicalDiagnosis = self.getCurrentMedicalDiagnosis()
                self.getMedicalDiagnosis(forceStringEx(medicalDiagnosis))


class CMedicalDiagnosisTableModel(QAbstractTableModel): # почему такой базовый класс?
    column        = [u'Врачебная формулировка']
    nameDiagnosis = [u'основной', u'осложнения', u'сопутствующие']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.items = []
        self._cols = []


    def cols(self):
        self._cols = [CCol(u'Врачебная формулировка',['medicalDiagnosis'], 20, 'l'),]
        return self._cols


    def columnCount(self, index = None):
        return 1


    def rowCount(self, index = None):
        return len(self.items)


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if row >= 0 and row < self.rowCount():
                item = self.items[row]
                return toVariant(item[column])
        return QVariant()


    def loadData(self, eventId, date, customFilter):
        db = QtGui.qApp.db
        self.eventId = eventId
        self.date = date
        self._customFilter = customFilter
        self.items = []
        if self.eventId:
            actionTypeIdList = getActionTypeIdListByFlatCode(u'medicalDiagnosis%')
            if actionTypeIdList:
                table = db.table('Action')
                tableAT = db.table('ActionType')
                queryTable = table.innerJoin(tableAT, tableAT['id'].eq(table['actionType_id']))
                filter = [table['event_id'].eq(self.eventId),
                          tableAT['deleted'].eq(0),
                          table['deleted'].eq(0),
                          table['actionType_id'].inlist(actionTypeIdList)
                          ]
                if self.date:
                    filter.append(table['endDate'].le(self.date))
                if self._customFilter:
                    filter.append(self._customFilter)
                order = ['Action.endDate DESC']
                records = db.getRecordList(queryTable, u'Action.*', filter, order)
                for record in records:
                    action = CAction(record=record)
                    if action:
                        actionType = action.getType()
                        properties = []
                        for name, propertyType in actionType._propertiesByName.items():
                            if propertyType.inMedicalDiagnosis and inMedicalDiagnosis[propertyType.inMedicalDiagnosis].lower() in CMedicalDiagnosisTableModel.nameDiagnosis:
                                properties.append((propertyType, action[name]))
                        properties.sort(key=lambda prop:prop[0].idx)
                        self.items.append(['\n'.join(((properti[0].name + u'. ' + forceString(properti[1])) if properti[1] else u'') for properti in properties)])
            if not self.items:
                stmt = u'''SELECT APS.value
                           FROM Action
                                INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = Action.actionType_id
                                INNER JOIN ActionProperty AS AP ON AP.type_id = APT.id
                                INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
                           WHERE Action.event_id = %s
                                AND Action.deleted = 0
                                %s
                                AND APT.inMedicalDiagnosis > 0
                                AND AP.action_id = Action.id
                                AND APT.deleted = 0
                                %s
                           ORDER BY Action.endDate DESC '''%(self.eventId, (u' AND DATE(Action.endDate) <= %s'%db.formatDate(self.date)) if self.date else u'', (u' AND %s'%self._customFilter) if self._customFilter else u'')
                query = db.query(stmt)
                while query.next():
                    record = query.record()
                    self.items.append([forceString(record.value('value'))])
        self.reset()
