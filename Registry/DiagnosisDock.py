# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QAbstractTableModel, QDate, QSize, QVariant, pyqtSignature, SIGNAL

from library.DialogBase                import CConstructHelperMixin
from library.DockWidget                import CDockWidget
from library.ICDUtils                  import getMKBName
from library.PreferencesMixin          import CContainerPreferencesMixin, CPreferencesMixin
from library.TableModel import CTableModel, CRefBookCol, CDateCol, CEnumCol
from library.Utils                     import forceBool, forceDate, forceInt, forceRef, forceString, formatBool, getPref, setPref, toVariant

from DataCheck.LocalLogicalControlDiagnosisLUD import CLocalLogicalControlDiagnosisLUD
from RefBooks.TempInvalidState         import CTempInvalidState
from Registry.ChangeMKBEditDialog      import CChangeMKBEditDialog
from Registry.ChangePeriodDiagnosisLUD import CChangePeriodDiagnosisLUD
from Registry.ChangeDispanserBegDateLUD import CChangeDispanserBegDateLUD
from Registry.Utils                    import deleteTempInvalid, getRightEditTempInvalid

from Surveillance.ChangeDispanserPerson import CChangeDispanserPerson

from Users.Rights                      import urChangeDiagnosis, urChangeMKB, urLocalControlLUD, urChangePeriodDiagnosis

from Registry.Ui_DignosisDockContent   import Ui_Form


class CDiagnosisDockWidget(CDockWidget):
    def __init__(self, parent):
        CDockWidget.__init__(self, parent)
        self.setWindowTitle(u'ЛУД')
        self.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.content = None
        self.contentPreferences = {}
        self.connect(QtGui.qApp, SIGNAL('dbConnectionChanged(bool)'), self.onConnectionChanged)


    def loadPreferences(self, preferences):
        self.contentPreferences = getPref(preferences, 'content', {})
        CDockWidget.loadPreferences(self, preferences)
        if isinstance(self.content, CPreferencesMixin):
            self.content.loadPreferences(self.contentPreferences)


    def savePreferences(self):
        result = CDockWidget.savePreferences(self)
        self.updateContentPreferences()
        setPref(result,'content',self.contentPreferences)
        return result


    def updateContentPreferences(self):
        if isinstance(self.content, CPreferencesMixin):
            self.contentPreferences = self.content.savePreferences()


    def onConnectionChanged(self, value):
        if value:
            self.onDBConnected()
        else:
            self.onDBDisconnected()


    def onDBConnected(self):
        self.setWidget(None)
        if self.content:
            self.content.setParent(None)
            self.content.deleteLater()
        self.content = CDiagnosisDockContent(self)
        self.content.loadPreferences(self.contentPreferences)
        self.setWidget(self.content)
        self.emit(SIGNAL('contentCreated(QDockWidget*)'), self)


    def onDBDisconnected(self):
        self.setWidget(None)
        if self.content:
            self.updateContentPreferences()
            self.content.setParent(None)
            self.content.deleteLater()
        self.content = QtGui.QLabel(u'необходимо\nподключение\nк базе данных', self)
        self.content.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.content.setDisabled(True)
        self.setWidget(self.content)
        self.emit(SIGNAL('contentDestroyed(QDockWidget*)'), self)


class CDiagnosisDockContent(QtGui.QWidget, Ui_Form, CConstructHelperMixin, CContainerPreferencesMixin):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        db = QtGui.qApp.db
        self.dtidBase = forceRef(db.translate('rbDiagnosisType', 'code', '2', 'id'))
        self.dtidAcomp = forceRef(db.translate('rbDiagnosisType', 'code', '9', 'id'))
        self.dtidModified = forceRef(db.translate('rbDiagnosisType', 'code', '99', 'id'))
        self.dtidPreliminary = forceRef(db.translate('rbDiagnosisType', 'code', '7', 'id'))
        self.dtidConcomitant = forceRef(db.translate('rbDiagnosisType', 'code', '11', 'id'))

        self.dcidAcute = forceRef(db.translate('rbDiseaseCharacter', 'code', '1', 'id'))
        self.dcidChronical = forceRef(db.translate('rbDiseaseCharacter', 'code', '3', 'id'))

        self.addModels('Chronical', CChronicalModel(self, self.dcidChronical))
        self.addModels('Acute', CAcuteModel(self, self.dcidAcute))
        self.addModels('ChronicalPreliminary', CChronicalPreliminaryModel(self, self.dcidChronical))
        self.addModels('AcutePreliminary', CAcutePreliminaryModel(self, self.dcidAcute))
        self.addModels('Factor', CFactorModel(self))
        self.addModels('TempInvalid', CTempInvalidModel(self, 0))
        self.addModels('Disability', CDisabilityModel(self, 1))
        self.addModels('VitalRestriction', CDisabilityModel(self, 2))
        self.addModels('AllergyBox', CAllergyBoxModel(self))
        self.addModels('IntoleranceMedicamentBox', CIntoleranceMedicamentBoxModel(self))
        self.addObject('actChronicalChangeMKB',  QtGui.QAction(u'Исправить шифр МКБ', self))
        self.addObject('actCronicalShowEvents',  QtGui.QAction(u'Показать обращения', self))
        self.addObject('actCronicalChangeDiagnosis', QtGui.QAction(u'Изменить диагноз', self))
        self.addObject('actChronicalCheck',  QtGui.QAction(u'Контроль ЛУД', self))
        self.addObject('actChronicalChangePeriod',  QtGui.QAction(u'Изменить период', self))
        self.addObject('actChronicalUpdDispanserDate', QtGui.QAction(u'Изменить дату постановки на учет', self))
        self.addObject('actChangePersonDN', QtGui.QAction(u'Изменить врача ДН', self))
        self.addObject('actAcuteChangeMKB',      QtGui.QAction(u'Исправить шифр МКБ', self))
        self.addObject('actAcuteShowEvents',     QtGui.QAction(u'Показать обращения', self))
        self.addObject('actAcuteChangeDiagnosis',QtGui.QAction(u'Изменить диагноз', self))
        self.addObject('actAcuteCheck',  QtGui.QAction(u'Контроль ЛУД', self))
        self.addObject('actAcuteChangePeriod',  QtGui.QAction(u'Изменить период', self))
        self.addObject('actTempInvalidFind',     QtGui.QAction(u'Найти документ', self))
        self.addObject('actTempInvalidDelete',   QtGui.QAction(u'Удалить документ', self))

#        self.timer = QTimer(self)
#        self.timer.setObjectName('timer')
#        self.timer.setInterval(60*1000) # раз в минуту

        self.setupUi(self)

        self.setModels(self.tblChronical,   self.modelChronical,   self.selectionModelChronical)
        self.setModels(self.tblAcute,       self.modelAcute,       self.selectionModelAcute)
        self.setModels(self.tblChronicalPreliminary, self.modelChronicalPreliminary, self.selectionModelChronicalPreliminary)
        self.setModels(self.tblAcutePreliminary, self.modelAcutePreliminary, self.selectionModelAcutePreliminary)
        self.setModels(self.tblFactor,      self.modelFactor,      self.selectionModelFactor)
        self.setModels(self.tblTempInvalid, self.modelTempInvalid, self.selectionModelTempInvalid)
        self.setModels(self.tblDisability,  self.modelDisability,  self.selectionModelDisability)
        self.setModels(self.tblVitalRestriction,  self.modelVitalRestriction,  self.selectionModelVitalRestriction)
        self.setModels(self.tblAllergyBox,  self.modelAllergyBox,  self.selectionModelAllergyBox)
        self.setModels(self.tblIntoleranceMedicamentBox,  self.modelIntoleranceMedicamentBox,  self.selectionModelIntoleranceMedicamentBox)

        self.cmbFactorFilterSpeciality.setTable('rbSpeciality', order='name')
        self.cmbFactorFilterMKB.setTable('vrbMKBZ', order='code')
        self.cmbFactorFilterSpeciality.setValue(0)
        self.cmbFactorFilterMKB.setValue(0)
        self.filterFactorSpeciality = None
        self.filterFactorMKB = None
        self.tblChronical.createPopupMenu([  self.actChronicalChangeMKB,
                                             self.actCronicalShowEvents,
                                             self.actCronicalChangeDiagnosis,
                                             self.actChronicalCheck,
                                             self.actChronicalChangePeriod,
                                             self.actChronicalUpdDispanserDate,
                                             self.actChangePersonDN])
        self.tblAcute.createPopupMenu(      [self.actAcuteChangeMKB,
                                             self.actAcuteShowEvents,
                                             self.actAcuteChangeDiagnosis,
                                             self.actAcuteCheck,
                                             self.actAcuteChangePeriod])
        self.tblTempInvalid.createPopupMenu([self.actTempInvalidFind,
                                             '-',
                                             self.actTempInvalidDelete])
#        self.timer.start()
        self.connect(QtGui.qApp, SIGNAL('currentClientIdChanged()'), self.updateTables)
        self.connect(QtGui.qApp, SIGNAL('currentClientInfoChanged()'), self.updateTables)


    def sizeHint(self):
        return QSize(10, 10)


    def updateTables(self):
        if not QtGui.qApp.db.isOpen():
            return
        self.clientId = QtGui.qApp.currentClientId()
        self.updateTablesDiagnosis()
        self.updateTablesPreliminaryDiagnosis()
        self.updateTablesFactor()
        self.modelTempInvalid.loadData(self.clientId)
        self.modelDisability.loadData(self.clientId)
        self.modelVitalRestriction.loadData(self.clientId)
        self.updateBloodType(self.clientId)
        self.modelAllergyBox.loadData(self.clientId)
        self.modelIntoleranceMedicamentBox.loadData(self.clientId)


    def updateTablesDiagnosis(self):
        showAccomp   = self.chkShowAccomp.isChecked()
        showModified = self.chkShowModified.isChecked()
        self.modelChronical.loadData(self.clientId, showAccomp, showModified)
        self.modelAcute.loadData(self.clientId, showAccomp, showModified)


    def updateTablesPreliminaryDiagnosis(self):
        showAccomp   = self.chkShowAccompPreliminary.isChecked()
        self.modelChronicalPreliminary.loadData(self.clientId, showAccomp)
        self.modelAcutePreliminary.loadData(self.clientId, showAccomp)


    def updateTablesFactor(self):
        self.modelFactor.loadData(self.clientId,  self.filterFactorSpeciality, self.filterFactorMKB, self.cmbFactorFilterMKB.code())


    def updateBloodType(self, clientId):
        if clientId:
            db = QtGui.qApp.db
            tableClient = db.table('Client')
            tableBloodType = db.table('rbBloodType')
            queryTable = tableClient.leftJoin(tableBloodType, tableBloodType['id'].eq(tableClient['bloodType_id']))
            records = db.getRecordList(queryTable, tableBloodType['name'].name(), tableClient['id'].eq(clientId))
        else:
            records = []
        bloodTypeName = forceString(records[0].value('name')) if records else ''
        self.lblBloodTypeBox.setText(bloodTypeName if bloodTypeName else u'не указано')


    def changeMKB(self, diagnosisId):
        if diagnosisId:
            dialog = CChangeMKBEditDialog(self)
            dialog.load(diagnosisId)
            if dialog.exec_():
                self.updateTables()


    def changeDiagnosis(self, diagnosisId):
        self.updateTables()


    def setEventFilterByDiagnosis(self, diagnosisId):
        if diagnosisId:
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            tableDiagnostic = db.table('Diagnostic')
            tableEvent = db.table('Event')
            queryTable = tableDiagnosis.leftJoin(tableDiagnostic, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
            queryTable = queryTable.leftJoin(tableEvent, tableDiagnostic['event_id'].eq(tableEvent['id']))
            eventIdList = db.getDistinctIdList(queryTable,  tableEvent['id'].name(), tableDiagnosis['id'].eq(diagnosisId), ['Event.execDate DESC', 'Event.id'])
            QtGui.qApp.setEventList(eventIdList)


    @pyqtSignature('int')
    def on_cmbFactorFilterSpeciality_currentIndexChanged(self, index):
        self.filterFactorSpeciality = self.cmbFactorFilterSpeciality.value()
        self.clientId = QtGui.qApp.currentClientId()
        if self.clientId:
            self.modelFactor.loadData(self.clientId, self.filterFactorSpeciality, self.filterFactorMKB)


    @pyqtSignature('int')
    def on_cmbFactorFilterMKB_currentIndexChanged(self, index):
        self.filterFactorMKB = self.cmbFactorFilterMKB.value()
        self.clientId = QtGui.qApp.currentClientId()
        if self.clientId:
            self.modelFactor.loadData(self.clientId, self.filterFactorSpeciality, self.filterFactorMKB, self.cmbFactorFilterMKB.code())


    @pyqtSignature('bool')
    def on_chkShowAccomp_toggled(self, checked):
        self.updateTablesDiagnosis()


    @pyqtSignature('bool')
    def on_chkShowAccompPreliminary_toggled(self, checked):
        self.updateTablesPreliminaryDiagnosis()


    @pyqtSignature('bool')
    def on_chkShowModified_toggled(self, checked):
        self.updateTablesDiagnosis()


#    def popupMenuTblChronicalAboutToShow(self):
    @pyqtSignature('')
    def on_tblChronical_popupMenuAboutToShow(self):
        row = self.tblChronical.currentIndex().row()
        self.actChronicalChangeMKB.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangeMKB))
        self.actCronicalShowEvents.setEnabled(row>=0 and QtGui.qApp.canFindEvent())
        self.actCronicalChangeDiagnosis.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangeDiagnosis))
        self.actChronicalCheck.setEnabled(row>=0 and QtGui.qApp.userHasRight(urLocalControlLUD))
        self.actChronicalChangePeriod.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangePeriodDiagnosis))
        self.actChronicalUpdDispanserDate.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangePeriodDiagnosis))
        self.actChangePersonDN.setEnabled(row >= 0 and QtGui.qApp.userHasRight(urChangePeriodDiagnosis))


#    def popupMenuTblAcuteAboutToShow(self):
    @pyqtSignature('')
    def on_tblAcute_popupMenuAboutToShow(self):
        row = self.tblAcute.currentIndex().row()
        self.actAcuteChangeMKB.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangeMKB))
        self.actAcuteShowEvents.setEnabled(row>=0 and QtGui.qApp.canFindEvent())
        self.actAcuteChangeDiagnosis.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangeDiagnosis))
        self.actAcuteCheck.setEnabled(row>=0 and QtGui.qApp.userHasRight(urLocalControlLUD))
        self.actAcuteChangePeriod.setEnabled(row>=0 and QtGui.qApp.userHasRight(urChangePeriodDiagnosis))


#    def popupMenuTblTempInvalidAboutToShow(self):
    @pyqtSignature('')
    def on_tblTempInvalid_popupMenuAboutToShow(self):
        row = self.tblTempInvalid.currentIndex().row()
        self.actTempInvalidFind.setEnabled(row>=0 and QtGui.qApp.canFindEvent())
        tempInvalidId = self.modelTempInvalid.getTempInvalidId(row) if row>=0 else None
        self.actTempInvalidDelete.setEnabled(row>=0 and getRightEditTempInvalid(tempInvalidId))


    @pyqtSignature('')
    def on_actChronicalChangeMKB_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        self.changeMKB(diagnosisId)


    @pyqtSignature('')
    def on_actChronicalCheck_triggered(self):
        CLocalLogicalControlDiagnosisLUD(self, True, False).exec_()


    @pyqtSignature('')
    def on_actChronicalChangePeriod_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        dialog = CChangePeriodDiagnosisLUD(self)
        dialog.load(diagnosisId)
        if dialog.exec_():
            self.updateTables()
            logicalControl = CLocalLogicalControlDiagnosisLUD(self, True, False)
            logicalControl.setCurrentDiagnosisId(diagnosisId)
            logicalControl.on_btnStartControlLocalLUD_clicked()
            logicalControl.exec_()


    @pyqtSignature('')
    def on_actChronicalUpdDispanserDate_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        dialog = CChangeDispanserBegDateLUD(self)
        dialog.load(diagnosisId)
        if dialog.exec_():
            self.updateTables()


    @pyqtSignature('')
    def on_actChangePersonDN_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        dialog = CChangeDispanserPerson(self)
        dialog.load(diagnosisId)
        if dialog.exec_():
            self.updateTables()


    @pyqtSignature('')
    def on_actCronicalShowEvents_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        self.setEventFilterByDiagnosis(diagnosisId)


    @pyqtSignature('')
    def on_actCronicalChangeDiagnosis_triggered(self):
        row = self.tblChronical.currentIndex().row()
        diagnosisId = self.modelChronical.getDiagnosisId(row)
        self.changeDiagnosis(diagnosisId)


    @pyqtSignature('')
    def on_actAcuteChangeMKB_triggered(self):
        row = self.tblAcute.currentIndex().row()
        diagnosisId = self.modelAcute.getDiagnosisId(row)
        self.changeMKB(diagnosisId)


    @pyqtSignature('')
    def on_actAcuteCheck_triggered(self):
        CLocalLogicalControlDiagnosisLUD(self, False, True).exec_()


    @pyqtSignature('')
    def on_actAcuteChangePeriod_triggered(self):
        row = self.tblAcute.currentIndex().row()
        diagnosisId = self.modelAcute.getDiagnosisId(row)
        dialog = CChangePeriodDiagnosisLUD(self)
        dialog.load(diagnosisId)
        if dialog.exec_():
            self.updateTables()
            logicalControl = CLocalLogicalControlDiagnosisLUD(self, False, True)
            logicalControl.setCurrentDiagnosisId(diagnosisId)
            logicalControl.on_btnStartControlLocalLUD_clicked()
            logicalControl.exec_()


    @pyqtSignature('')
    def on_actAcuteShowEvents_triggered(self):
        row = self.tblAcute.currentIndex().row()
        diagnosisId = self.modelAcute.getDiagnosisId(row)
        self.setEventFilterByDiagnosis(diagnosisId)


    @pyqtSignature('')
    def on_actAcuteChangeDiagnosis_triggered(self):
        row = self.tblAcute.currentIndex().row()
        diagnosisId = self.modelAcute.getDiagnosisId(row)
        self.changeDiagnosis(diagnosisId)


    @pyqtSignature('')
    def on_actTempInvalidFind_triggered(self):
        row = self.tblTempInvalid.currentIndex().row()
        tempInvalidId = self.modelTempInvalid.getTempInvalidId(row) if row>=0 else None
        if tempInvalidId:
            db = QtGui.qApp.db
            record = db.getRecord('TempInvalid', 'begDate, endDate', tempInvalidId)
            if record:
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                tableEvent = db.table('Event')
                cond = [tableEvent['execDate'].ge(begDate),
                        tableEvent['execDate'].lt(endDate.addDays(1)),
                        tableEvent['deleted'].eq(0),
                        tableEvent['client_id'].eq(self.clientId),
                       ]
                eventRecord = db.getRecordEx(tableEvent, 'id', cond, 'execDate DESC')
                if eventRecord:
                    eventId = forceRef(eventRecord.value('id'))
                    QtGui.qApp.findEvent(eventId)
            self.updateTables()


    @pyqtSignature('')
    def on_actTempInvalidDelete_triggered(self):
        row = self.tblTempInvalid.currentIndex().row()
        tempInvalidId = self.modelTempInvalid.getTempInvalidId(row) if row>=0 else None
        if getRightEditTempInvalid(tempInvalidId):
            if QtGui.QMessageBox.question(self,
                            u'Удаление документа', u'Вы действительно хотите удалить документ?',
                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                            QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                    QtGui.qApp.call(self, deleteTempInvalid, (self, tempInvalidId,))
                    self.updateTables()

#
# #####################################################################
#

class CChronicalModel(QAbstractTableModel):
    """Модель данных для раздела 'Хронические заболевания' панели ЛУД"""
    headerTextList = [u'Шифр', u'Установлен', u'Последнее', u'Д.Н.', u'Поставлен на учет', u'Врач по ДН']

    def __init__(self, parent, characterId):
        QAbstractTableModel.__init__(self, parent)
        self.headerText = self.headerTextList[:]
        if QtGui.qApp.defaultMorphologyMKBIsVisible():
            self.headerText.insert(1, u'Морф.')
            self.colAdd = 1
        else:
            self.colAdd = 0
        if QtGui.qApp.isExSubclassMKBVisible():
            self.colAdd += 1
            self.headerText.insert(self.colAdd, u'РСК')
        self.characterId = characterId
        self.items = []
        self.limitDate = False
        self.dtidBase = parent.dtidBase
        self.dtidAcomp = parent.dtidAcomp
        self.dtidModified = parent.dtidModified


    def columnCount(self, index=None):
        return len(self.headerText)


    def rowCount(self, index=None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        """
        Отображение данных в таблице 'Хронические заболевания' панели ЛУД

        :param index: индекс ячейки таблицы 'Хронические заболевания'
        :type index: QModelIndex
        :param role: DisplayRole
        :type role: int
        :return: Данные, соответствующие выбранной DisplayRole (см. докуменацию к Qt)
        :rtype: QVariant
        """
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return QVariant(item[column])
        elif role == Qt.FontRole:
            result = QtGui.QFont()
            item = self.items[row]
            isAccomp = item[8+self.colAdd]
            isModified = item[9+self.colAdd]
            if isAccomp or isModified:
                result = QtGui.QFont()
                if isAccomp:
                    result.setItalic(True)
                if isModified:
                    result.setStrikeOut(True)
            if QtGui.qApp.isDockDiagnosisAnalyzeSurveillance():
                isAnalyzeSurveillanceMKB = item[13 + self.colAdd]
                isAnalyzeSurveillancePeriod = item[14 + self.colAdd]
                if isAnalyzeSurveillanceMKB:
                    result.setBold(True)
                if isAnalyzeSurveillancePeriod:
                    result.setBold(True)
                    result.setItalic(True)
            return QVariant(result)
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[10+self.colAdd] is None:
                    MKB = item[6+self.colAdd]
                    MKBEx = item[7+self.colAdd]
                    item[10+self.colAdd] = calcMKBToolTip(MKB, MKBEx)
                return QVariant(item[10+self.colAdd])
        return QVariant()


    def loadData(self, clientId, showAccomp, showModified):
        """
        Загрузка данных из БД в модель
        Это надо переписать с использованием QSqlRecord или словаря в качестве item, а не list, иначе - жесть!!!

        :param clientId: id клиента
        :type clientId: int
        :param showAccomp: флаг, показывать ли сопутствующие диагнозы
        :type showAccomp: bool
        :param showModified: флаг, показывать ли изменённые диагнозы
        :type showModified: bool
        """
        self.items = []
        MKBProps = {}
        if clientId:
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            tableDispanser = db.table('rbDispanser')
            tablePersonWithSpeciality = db.table('vrbPersonWithSpeciality')

            table = tableDiagnosis.leftJoin(tableDispanser, tableDispanser['id'].eq(tableDiagnosis['dispanser_id']))
            table = table.leftJoin(tablePersonWithSpeciality, tablePersonWithSpeciality['id'].eq(tableDiagnosis['dispanserPerson_id']))
            cols = [tableDiagnosis['id'],
                    tableDiagnosis['MKB'],
                    tableDiagnosis['MKBEx'],
                    tableDiagnosis['morphologyMKB'],
                    tableDiagnosis['setDate'],
                    tableDiagnosis['endDate'],
                    tableDispanser['observed'],
                    tableDiagnosis['mod_id'],
                    tableDiagnosis['diagnosisType_id'],
                    tableDiagnosis['character_id'],
                    tableDiagnosis['dispanserBegDate'],
                    tablePersonWithSpeciality['name'],
                    tableDiagnosis['exSubclassMKB'],
                    tableDiagnosis['dispanser_id']
                    ]
            cond = [tableDiagnosis['client_id'].eq(clientId),
                    tableDiagnosis['character_id'].eq(self.characterId),
                    tableDiagnosis['deleted'].eq(0),
                    '''EXISTS(SELECT Diagnostic.id
                                  FROM Diagnostic
                                  LEFT JOIN Event ON Event.id = Diagnostic.event_id
                                  WHERE Diagnostic.diagnosis_id = Diagnosis.id 
                                  AND Diagnostic.deleted = 0
                                  AND Event.deleted = 0)''']
            dtIdList = [self.dtidBase]
            if showAccomp:
                dtIdList.append(self.dtidAcomp)
            if showModified:
                dtIdList.append(self.dtidModified)
            cond.append(tableDiagnosis['diagnosisType_id'].inlist(dtIdList))
            if not showModified:
                cond.append(tableDiagnosis['mod_id'].isNull())
#            if self.limitDate:
#                cond.append(tableDiagnosis['endDate'].ge(getLimitDate()))

            records = db.getRecordList(table, cols, cond, tableDiagnosis['endDate'].name() + ' DESC')
            for record in records:
                id = forceRef(record.value('id'))
                MKB = forceString(record.value('MKB'))
                MKBEx = forceString(record.value('MKBEx'))
                morphologyMKB = forceString(record.value('morphologyMKB'))
                setDate = forceDate(record.value('setDate'))
                endDate = forceDate(record.value('endDate'))
                observed = forceBool(record.value('observed'))
                modId = forceRef(record.value('mod_id'))
                diagnosisTypeId = forceRef(record.value('diagnosisType_id'))
                dispanserBegDate = forceDate(record.value('dispanserBegDate'))
                dispanserId = forceRef(record.value('dispanser_id'))
                namePerson = forceString(record.value('name'))
                item = [(MKB + '+' + MKBEx) if MKBEx else MKB,
                        forceString(setDate),
                        forceString(endDate),
                        formatBool(observed),
                        forceString(dispanserBegDate),
                        namePerson if forceBool(observed) else None,
                        MKB,
                        MKBEx,
                        diagnosisTypeId != self.dtidBase,
                        bool(modId) or diagnosisTypeId == self.dtidModified,
                        None,
                        id,
                        forceString(dispanserId)
                        ]
                if item[6]:
                    MKBProps[item[6]] = [0, True]
                if self.colAdd:
                    if QtGui.qApp.defaultMorphologyMKBIsVisible():
                        item.insert(1, morphologyMKB)
                    if QtGui.qApp.isExSubclassMKBVisible():
                        item.insert(self.colAdd, forceString(record.value('exSubclassMKB')))
                self.items.append(item)
            if QtGui.qApp.isDockDiagnosisAnalyzeSurveillance():
                # Добавляем в данные доп. атрибуты, если включен анализ ДН в настройках
                # Проверяем свойства МКБ
                tableMKB = db.table('MKB')
                cols = [tableMKB['DiagID'],
                        tableMKB['requiresFillingDispanser']]
                where = tableMKB['DiagID'].inlist(MKBProps.keys())
                records = db.getRecordList(tableMKB, cols, where)
                for record in records:
                    val, ok = record.value('requiresFillingDispanser').toInt()
                    if ok:
                        MKBProps[forceString(record.value('DiagID'))][0] = val
                # Проверяем условия постановки на учёт в диспансере
                tableProphylaxis = db.table('ProphylaxisPlanning')
                cols = [tableProphylaxis['id'],
                        tableProphylaxis['endDate'],
                        tableProphylaxis['MKB'],
                        tableProphylaxis['parent_id']]
                client = tableProphylaxis['client_id'].eq(clientId)
                MKBlist = tableProphylaxis['MKB'].inlist(MKBProps.keys())
                deleted = tableProphylaxis['deleted'].eq(0)
                where = db.joinAnd([client, MKBlist, deleted])
                records = db.getRecordList(tableProphylaxis, cols, where)
                dates = []
                currentDate = QDate.currentDate()
                # Сворачиваем данные из Prophylaxis, убираем потомков в диагнозах, устанавливаем самую позднюю дату
                tmprecords = {}
                # Сначала ищем родителей
                for record in records:
                    if record.isNull('parent_id'):
                        tmprecords[forceInt(record.value('id'))] = record
                        # records.remove(record)
                # Затем перезаписываем endDate родителя самой поздней датой потомков
                for record in records:
                    parentId = forceInt(record.value('parent_id'))
                    parent = tmprecords.get(parentId, None)
                    if parent:
                        oldDate = forceDate(parent.value('endDate'))
                        newDate = forceDate(record.value('endDate'))
                        if newDate > oldDate:
                            tmprecords[parentId].setValue('endDate', newDate)
                # Ищем записи без даты либо с устаревшей датой
                for id in tmprecords:
                    record = tmprecords[id]
                    date = forceDate(record.value('endDate'))
                    if date.isNull():
                        MKBProps[forceString(record.value('MKB'))][1] = True
                    elif currentDate > date:
                        MKBProps[forceString(record.value('MKB'))][1] = True
                    else:
                        MKBProps[forceString(record.value('MKB'))][1] = False
                    dates.append(date)

                for item in self.items:
                    # 1. Проверяем условие по коду МКБ для выделения жирным (dispanserId и dispanserBegDate)
                    if (item[12 + self.colAdd] == '') and (item[4 + self.colAdd] == ''):
                        item.append(bool(MKBProps[item[6 + self.colAdd]][0]))
                    else:
                        item.append(False)
                    # 2. Проверяем условие по постановке в планирование диспансеризации для выделения жирным курсивом
                    isDispancerId = True if (item[12 + self.colAdd] in ('1', '2')) else False
                    isDispancerBegDate = bool(item[4 + self.colAdd])
                    if (isDispancerId or isDispancerBegDate) and MKBProps[item[6 + self.colAdd]][1]:
                        item.append(True)
                    else:
                        item.append(False)

        self.reset()


    def getDiagnosisId(self, row):
        return self.items[row][11+self.colAdd] if 0 <= row < len(self.items) else None


class CAcuteModel(CChronicalModel):
    """Модель данных для раздела 'Острые заболевания' панели ЛУД"""
    headerText = [u'Шифр', u'Начало', u'Окончание', u'Д.Н.']

    def __init__(self, parent, characterId):
        CChronicalModel.__init__(self, parent, characterId)
#        self.limitDate = True
        self.limitDate = False

    def columnCount(self, index=None):
        return len(self.headerText)

    def data(self, index, role=Qt.DisplayRole):
        """
        Отображение данных в таблице 'Острые заболевания' панели ЛУД
        Метод перегружен по сравнению с оригинальным CChronicalModel.data(), т.к. решили убрать анализ диспансерного
        наблюдения для острых заболеваний.

        :param index: индекс ячейки таблицы 'Острые заболевания'
        :type index: QModelIndex
        :param role: DisplayRole
        :type role: int
        :return: Данные, соответствующие выбранной DisplayRole (см. докуменацию к Qt)
        :rtype: QVariant
        """
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return QVariant(item[column])
        elif role == Qt.FontRole:
            result = QtGui.QFont()
            item = self.items[row]
            isAccomp = item[7 + self.colAdd]
            isModified = item[8 + self.colAdd]
            if isAccomp or isModified:
                if isAccomp:
                    result.setItalic(True)
                if isModified:
                    result.setStrikeOut(True)
            return QVariant(result)
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[9 + self.colAdd] is None:
                    MKB = item[5 + self.colAdd]
                    MKBEx = item[6 + self.colAdd]
                    item[9 + self.colAdd] = calcMKBToolTip(MKB, MKBEx)
                return QVariant(item[9 + self.colAdd])
        return QVariant()


class CChronicalPreliminaryModel(QAbstractTableModel):
    headerTextList = [u'Шифр', u'Установлен', u'Последнее', u'Врач']

    def __init__(self, parent, characterId):
        QAbstractTableModel.__init__(self, parent)
        self.headerText = self.headerTextList[:]
        if QtGui.qApp.defaultMorphologyMKBIsVisible():
            self.headerText.insert(1, u'Морф.')
            self.colAdd = 1
        else:
            self.colAdd = 0
        if QtGui.qApp.isExSubclassMKBVisible():
            self.colAdd += 1
            self.headerText.insert(self.colAdd, u'РСК')
        self.characterId = characterId
        self.items = []
        self.limitDate = False
        self.dtidModified = parent.dtidModified
        self.dtidPreliminary = parent.dtidPreliminary
        self.dtidConcomitant = parent.dtidConcomitant


    def columnCount(self, index=None):
        return len(self.headerText)


    def rowCount(self, index=None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return QVariant(item[column])
        elif role == Qt.FontRole:
            item = self.items[row]
            isAccomp = item[6+self.colAdd]
            isModified = item[7+self.colAdd]
            if isAccomp or isModified:
                result = QtGui.QFont()
                if isAccomp:
                    result.setItalic(True)
                if isModified:
                    result.setStrikeOut(True)
                return QVariant(result)
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[8+self.colAdd] is None:
                    MKB = item[4+self.colAdd]
                    MKBEx = item[5+self.colAdd]
                    item[8+self.colAdd] = calcMKBToolTip(MKB, MKBEx)
                return QVariant(item[8+self.colAdd])
        return QVariant()


    def loadData(self, clientId, showAccomp):
        self.items = []
        if clientId:
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            tablePersonWithSpeciality = db.table('vrbPersonWithSpeciality')
            table = tableDiagnosis.leftJoin(tablePersonWithSpeciality, tablePersonWithSpeciality['id'].eq(tableDiagnosis['person_id']))
            cols = [tableDiagnosis['id'],
                    tableDiagnosis['MKB'],
                    tableDiagnosis['MKBEx'],
                    tableDiagnosis['morphologyMKB'],
                    tableDiagnosis['setDate'],
                    tableDiagnosis['endDate'],
                    tablePersonWithSpeciality['name'],
                    tableDiagnosis['mod_id'],
                    tableDiagnosis['diagnosisType_id'],
                    tableDiagnosis['character_id'],
                    tableDiagnosis['exSubclassMKB']
                    ]
            cond = [tableDiagnosis['client_id'].eq(clientId),
                    tableDiagnosis['character_id'].eq(self.characterId),
                    tableDiagnosis['deleted'].eq(0)
                    ]
            cond.append('''EXISTS(SELECT Diagnostic.id
                                  FROM Diagnostic
                                  LEFT JOIN Event ON Event.id = Diagnostic.event_id
                                  WHERE Diagnostic.diagnosis_id = Diagnosis.id 
                                  AND Diagnostic.deleted = 0
                                  AND Event.deleted = 0)''')
            dtIdList = [self.dtidPreliminary]
            if showAccomp:
                dtIdList.append(self.dtidConcomitant)
            cond.append(tableDiagnosis['diagnosisType_id'].inlist(dtIdList))
            cond.append(tableDiagnosis['mod_id'].isNull())
#            if self.limitDate:
#                cond.append(tableDiagnosis['endDate'].ge(getLimitDate()))
            records = db.getRecordList(table, cols, cond, tableDiagnosis['endDate'].name()+' DESC')
            for record in records:
                id = forceRef(record.value('id'))
                MKB = forceString(record.value('MKB'))
                MKBEx = forceString(record.value('MKBEx'))
                morphologyMKB = forceString(record.value('morphologyMKB'))
                setDate = forceDate(record.value('setDate'))
                endDate = forceDate(record.value('endDate'))
                namePerson = forceString(record.value('name'))
                modId   = forceRef(record.value('mod_id'))
                diagnosisTypeId = forceRef(record.value('diagnosisType_id'))
                item = [  (MKB + '+' + MKBEx) if MKBEx else MKB,
                          forceString(setDate),
                          forceString(endDate),
                          namePerson,
                          MKB,
                          MKBEx,
                          diagnosisTypeId not in dtIdList,
                          bool(modId) or diagnosisTypeId == self.dtidModified,
                          None,
                          id
                       ]
                if self.colAdd:
                    if QtGui.qApp.defaultMorphologyMKBIsVisible():
                        item.insert(1, morphologyMKB)
                    if QtGui.qApp.isExSubclassMKBVisible():
                        item.insert(self.colAdd, forceString(record.value('exSubclassMKB')))
                self.items.append(item)
        self.reset()


    def getDiagnosisId(self, row):
        return self.items[row][9+self.colAdd] if 0<=row<len(self.items) else None


class CAcutePreliminaryModel(CChronicalPreliminaryModel):
    headerText = [u'Шифр', u'Начало', u'Окончание', u'Врач']

    def __init__(self, parent, characterId):
        CChronicalPreliminaryModel.__init__(self, parent, characterId)
        self.limitDate = False

    def columnCount(self, index = None):
        return len(self.headerText)


class CFactorModel(QAbstractTableModel):
    headerText = [u'Шифр', u'Дата', u'Врач']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.items = []


    def columnCount(self, index = None):
        return 3


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return QVariant(item[column])
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[3] is None:
                    MKB = item[0]
                    item[3] = calcMKBToolTip(MKB)
                return QVariant(item[3])
        return QVariant()


    def loadData(self, clientId, filterSpeciality=None, filterBlockMKB=None, codeBlockMKB=None):
        self.items = []
        if clientId:
            db = QtGui.qApp.db
            tableDiagnosis = db.table('Diagnosis')
            tablePersonWithSpeciality = db.table('vrbPersonWithSpeciality')
            cols = [tableDiagnosis['MKB'],
                    tableDiagnosis['setDate'],
                    tablePersonWithSpeciality['name']
                   ]
            table = tableDiagnosis.leftJoin(tablePersonWithSpeciality, tablePersonWithSpeciality['id'].eq(tableDiagnosis['person_id']))
            cond = [tableDiagnosis['client_id'].eq(clientId),
                    tableDiagnosis['character_id'].isNull(),
                    tableDiagnosis['mod_id'].isNull()
                    ]
            cond.append('''EXISTS(SELECT Diagnostic.id
                                  FROM Diagnostic
                                  LEFT JOIN Event ON Event.id = Diagnostic.event_id
                                  WHERE Diagnostic.diagnosis_id = Diagnosis.id 
                                  AND Diagnostic.deleted = 0
                                  AND Event.deleted = 0)''')
            if filterSpeciality:
               cond.append(tablePersonWithSpeciality['speciality_id'].eq(filterSpeciality))
            if filterBlockMKB:
                if codeBlockMKB:
                    queryBlockMKB = re.compile(r"""\s*\(\s*([A-Z][0-9.]+)\s*-\s*([A-Z][0-9.]+)\s*\)\s*""",  re.IGNORECASE)
                    resValueBlockMKB = None
                    resValueBlockMKB = re.match(queryBlockMKB,  codeBlockMKB)
                    if resValueBlockMKB:
                        if len(resValueBlockMKB.groups()) == 2:
                            minValueBlockMKB = resValueBlockMKB.group(1)
                            maxValueBlockMKB = resValueBlockMKB.group(2)
                            cond.append(tableDiagnosis['MKB'].ge(minValueBlockMKB))
                            cond.append(tableDiagnosis['MKB'].le(maxValueBlockMKB))
            records = db.getRecordList(table, cols, cond, tableDiagnosis['endDate'].name()+' DESC')
            for record in records:
                MKB = forceString(record.value('MKB'))
                setDate = forceDate(record.value('setDate'))
                namePerson = forceString(record.value('name'))
                item = [  MKB,                                                                     # 0
                          forceString(setDate),                                                    # 1
                          namePerson,                                                              # 2
                          None                                                                     # 3
                       ]
                self.items.append(item)
        self.reset()


def getLimitDate():
    today = QDate.currentDate()
    return min([today.addMonths(-1), QDate(today.year(), 1, 1)])


class CTempInvalidModel(QAbstractTableModel):
    headerText = [u'Шифр', u'Начало', u'Конец', u'Состояние']

    def __init__(self, parent, type_):
        QAbstractTableModel.__init__(self, parent)
        self.items = []
        self.type_ = type_


    def columnCount(self, index = None):
        return 4


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return toVariant(item[column])
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[7] is None:
                    MKB = item[4]
                    MKBEx = item[5]
                    item[7] = calcMKBToolTip(MKB, MKBEx)
                return QVariant(item[7])
        return QVariant()


    def loadData(self, clientId):
        self.items = []
        if clientId:
            db = QtGui.qApp.db
            table = db.table('TempInvalid')
            tableDiagnosis = db.table('Diagnosis')
            cond = [table['deleted'].eq(0), table['client_id'].eq(clientId), table['type'].eq(self.type_)]
            cols = [table['id'], tableDiagnosis['MKB'], tableDiagnosis['MKBEx'], table['begDate'], table['endDate'], table['state']]
            cond.append('''EXISTS(SELECT Diagnostic.id
                                  FROM Diagnostic
                                  LEFT JOIN Event ON Event.id = Diagnostic.event_id
                                  WHERE Diagnostic.diagnosis_id = Diagnosis.id 
                                  AND Diagnostic.deleted = 0
                                  AND Event.deleted = 0)''')
            queryTable = table.leftJoin(tableDiagnosis, db.joinAnd([tableDiagnosis['id'].eq(table['diagnosis_id']), tableDiagnosis['deleted'].eq(0)]))
            for record in db.getRecordList(queryTable, cols, cond, 'endDate DESC'):
                MKB   = forceString(record.value('MKB'))
                MKBEx = forceString(record.value('MKBEx'))
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                state  = forceInt(record.value('state'))
                item = [  (MKB + '+' + MKBEx) if MKBEx else MKB,    # 0
                          forceString(begDate),                     # 1
                          forceString(endDate),                     # 2
                          CTempInvalidState.text(state),            # 3
                          MKB,                                      # 4
                          MKBEx,                                    # 5
                          forceRef(record.value('id')),             # 6
                          None                                      # 7
                       ]
                self.items.append(item)
        self.reset()


    def getTempInvalidId(self, row):
        return self.items[row][6]


## ######################################################################

class CDisabilityModel(QAbstractTableModel):
    headerText = [u'Тип', u'Начало', u'Конец', u'Режим', u'Статус']

    def __init__(self, parent, type_):
        QAbstractTableModel.__init__(self, parent)
        self.items = []
        self.type_ = type_


    def columnCount(self, index = None):
        return 4


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return toVariant(item[column])
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[6] is None:
                    codeDocRegime = item[0]
                    docName = item[4]
                    regimeName = item[5]
                    item[6] = codeDocRegime + ': ' + docName + ' - ' + regimeName
                return QVariant(item[6])
        return QVariant()


    def loadData(self, clientId):
        self.items = []
        if clientId:
            db = QtGui.qApp.db
            table = db.table('TempInvalid')
            tableInvalidPeriod = db.table('TempInvalid_Period')
            tableInvalidRegime = db.table('rbTempInvalidRegime')
            tableTempInvalidDocument = db.table('rbTempInvalidDocument')
            cond = [table['deleted'].eq(0), table['client_id'].eq(clientId), table['type'].eq(self.type_), table['endDate'].eq(tableInvalidPeriod['endDate'])]
            cols = [table['id'], tableInvalidRegime['code'], tableInvalidRegime['name'], tableTempInvalidDocument['code'].alias('docCode'), tableTempInvalidDocument['name'].alias('docName'), table['begDate'], table['endDate'], table['state'], table['serial'], table['number']]
            queryTable = tableInvalidPeriod.leftJoin(table, table['id'].eq(tableInvalidPeriod['master_id']))
            queryTable = queryTable.leftJoin(tableInvalidRegime, tableInvalidRegime['id'].eq(tableInvalidPeriod['regime_id']))
            queryTable = queryTable.leftJoin(tableTempInvalidDocument, tableTempInvalidDocument['id'].eq(table['doctype_id']))
            for record in db.getRecordList(queryTable, cols, cond, 'endDate DESC'):
                regimeCode = forceString(record.value('code'))
                regimeName = forceString(record.value('name'))
                docCode = forceString(record.value('docCode'))
                docName =  forceString(record.value('docName'))
                begDate = forceDate(record.value('begDate'))
                endDate = forceDate(record.value('endDate'))
                state   = forceInt(record.value('state'))
                item = [  (docCode + ' - ' + regimeCode),            # 0
                          forceString(begDate),                      # 1
                          forceString(endDate),                      # 2
                          CTempInvalidState.text(state),             # 3
                          docName,                                   # 4
                          regimeName,                                # 5
                          None                                       # 6
                       ]
                self.items.append(item)
        self.reset()


# WTF? у нас есть модели, позволяющие сделать это в 4 строки :(
class CAllergyBoxModel(QAbstractTableModel):
    headerText = [u'Наименование вещества', u'Дата установления', u'Степень']
    dataPower = [u'0 - не известно', u'1 - малая', u'2 - средняя', u'3 - высокая', u'4 - строгая']

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.items = []


    def columnCount(self, index = None):
        return 3


    def rowCount(self, index = None):
        return len(self.items)


    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            if column == 2:
                return QVariant(self.dataPower[item[column]])
            else:
                return QVariant(item[column])
        elif role == Qt.ToolTipRole:
            if column == 0:
                item = self.items[row]
                if item[3] is None:
                    nameSubstance = item[0]
                    item[3] = nameSubstance
                return QVariant(item[3])

        return QVariant()


    def loadData(self, clientId):
        self.items = []
        if clientId:
            db = QtGui.qApp.db
            tableClientAllergy = db.table('ClientAllergy')
            cols = [tableClientAllergy['nameSubstance'],
                    tableClientAllergy['createDate'],
                    tableClientAllergy['power']
                   ]
            cond = [tableClientAllergy['client_id'].eq(clientId)]
            records = db.getRecordList(tableClientAllergy, cols, cond)
            for record in records:
                nameSubstance = forceString(record.value('nameSubstance'))
                createDate = forceDate(record.value('createDate'))
                power = forceInt(record.value('power'))
                item = [  nameSubstance,
                          forceString(createDate),
                          power,
                          None
                       ]
                self.items.append(item)
        self.reset()


class CIntoleranceMedicamentBoxModel(CTableModel):
    def __init__(self, parent):
        powerNames = (u'0 - не известно', u'1 - малая', u'2 - средняя', u'3 - высокая', u'4 - строгая')
        cols = [
            CRefBookCol(u'Наименование медикамента', ['activeSubstance_id'], 'rbNomenclatureActiveSubstance', 40),
            CDateCol(u'Дата установления', ['createDate'], 20),
            CEnumCol(u'Степень', ['power'], powerNames, 20),
        ]
        CTableModel.__init__(self, parent, cols, 'ClientIntoleranceMedicament')


    def loadData(self, clientId):
        db = QtGui.qApp.db
        table = db.table('ClientIntoleranceMedicament')
        cond = [
            table['deleted'].eq(0),
            table['client_id'].eq(clientId),
        ]
        self.setIdList(db.getIdList(table, 'id', cond))



def calcMKBToolTip(MKB, MKBEx=''):
    result = []
    if MKB:
        result.append(MKB+': '+getMKBName(MKB))
    if MKBEx:
        result.append(MKBEx+': '+getMKBName(MKBEx))
    return u'\n'.join(result)
