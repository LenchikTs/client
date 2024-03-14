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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QObject

from library.TableModel  import CTableModel, CBoolCol, CCol
from library.crbcombobox import CRBComboBox, CRBModelDataCache
from library.Utils       import forceInt, forceRef, forceString, toVariant, trim, formatNum
from library.AgeSelector import checkAgeSelector, parseAgeSelector
from library.PreferencesMixin import CDialogPreferencesMixin

from Ui_F088AddActions29Dialog import Ui_F088AddActions30Dialog


class CF088AddActions30Dialog(QtGui.QDialog, CDialogPreferencesMixin, Ui_F088AddActions30Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CF088AddActions30TableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.tblF088AddActions30.setModel(self.tableModel)
        self.tblF088AddActions30.setSelectionModel(self.tableSelectionModel)
        self.tblF088AddActions30.installEventFilter(self)
        self.edtFindByCode.installEventFilter(self)
        self.showRowList = []
        self.isFindByCode = False
        self.actionsCacheByCode = {}
        self.actionsCodeCacheByName = {}
        self._parent = parent
        self.clientId  = None
        self.clientSex = None
        self.clientAge = None
        self.MKB = None
        self.MKBList = []
        self.addActions30IdList = []
        self.actionTypeIdList = []
        self.basicAdditionalDict = []
        self.actionTypeMKBList = {}
        self.eventTypeId = None


    def exec_(self):
        self.loadDialogPreferences()
        result = QtGui.QDialog.exec_(self)
        return result


    def done(self, result):
        self.saveDialogPreferences()
        QtGui.QDialog.done(self, result)


    def setEventTypeId(self, eventTypeId):
        self.eventTypeId = eventTypeId


    def updateSelectedCount(self):
        n = len(self.tblF088AddActions30.model().getSelectedIdList())
        if n == 0:
            msg = u'ничего не выбрано'
        else:
            msg = u'выбрано '+formatNum(n, [u'действие', u'действия', u'действий'])
        self.lblSelectedCount.setText(msg)


    def loadData(self):
        self.edtFindByCode.setText('')
        self.actionTypeIdList, self.basicAdditionalDict, self.actionTypeMKBList = self.setActions30List()
        self.tblF088AddActions30.model().setIdList(self.actionTypeIdList)
        self.tblF088AddActions30.model().setActionTypeMKBList(self.actionTypeMKBList)


    def setClientInfo(self, clientId, clientSex, clientAge):
        self.clientId  = clientId
        self.clientSex = clientSex
        self.clientAge = clientAge


    def setMKBList(self, MKBList):
        self.MKB = None
        self.MKBList = MKBList
        if MKBList and len(MKBList) > 0:
            self.MKB = MKBList[0][0]


    def setActions30List(self):
        self.actionsCacheByCode.clear()
        self.actionsCodeCacheByName.clear()
        actionTypeIdList = []
        actionTypeMKBList = {}
        basicAdditionalDict = {}
        self.tblF088AddActions30.model().enableIdList = []
        self.getBasicAdditional()
        isMKB = True
        MKBList = []
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        tableEventType = db.table('EventType')
        tableETA = db.table('EventType_Action')
        tableActionTypeIdentification = db.table('ActionType_Identification')
        tableActionTypeIdentification2 = db.table('ActionType_Identification').alias('ATI2')
        tableRBAccountingSystem = db.table('rbAccountingSystem')
        tableRBAccountingSystem2 = db.table('rbAccountingSystem').alias('rbAccountingSystem2')
        tableEGISZ = db.table('rbMedicalExaminationsMSE').alias('tableEGISZ')
        queryTable = tableEventType.innerJoin(tableETA, tableETA['eventType_id'].eq(tableEventType['id']))
        queryTable = queryTable.innerJoin(tableActionType, tableActionType['id'].eq(tableETA['actionType_id']))
        queryTable = queryTable.innerJoin(tableActionTypeIdentification, tableActionTypeIdentification['master_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBAccountingSystem, tableRBAccountingSystem['id'].eq(tableActionTypeIdentification['system_id']))
        queryTable = queryTable.innerJoin(tableEGISZ, tableEGISZ['NMU_code'].eq(tableActionTypeIdentification['value']))
        queryTable = queryTable.innerJoin(tableActionTypeIdentification2, tableActionTypeIdentification2['master_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableRBAccountingSystem2, tableRBAccountingSystem2['id'].eq(tableActionTypeIdentification2['system_id']))
        cols = [tableActionType['id'],
                tableActionType['code'].alias('codeAT'),
                tableActionType['name'].alias('nameAT'),
                tableETA['sex'].alias('sexETA'),
                tableETA['age'].alias('ageETA'),
                tableEGISZ['BASIC_ADDITIONAL'],
                tableEGISZ['MKB']
               ]
        if self.chkAdditional.isChecked():
            cols.append(u'''(SELECT ATI.value
                    FROM ActionType_Identification AS ATI
                    INNER JOIN rbAccountingSystem AS rbAS ON rbAS.id = ATI.system_id
                    WHERE ATI.master_id = ActionType.id AND rbAS.urn = 'urn:oid:1.2.643.5.1.13.13.99.2.857*'
                    AND ATI.deleted = 0 AND ATI.value = 2
                    LIMIT 1) AS additional''')
        else:
            cols.append(u'''(SELECT ATI.value
                    FROM ActionType_Identification AS ATI
                    INNER JOIN rbAccountingSystem AS rbAS ON rbAS.id = ATI.system_id
                    WHERE ATI.master_id = ActionType.id AND rbAS.urn = 'urn:oid:1.2.643.5.1.13.13.99.2.857*'
                    AND ATI.deleted = 0 AND ATI.value != 2
                    ORDER BY ATI.value DESC
                    LIMIT 1) AS additional''')
        cond = [tableActionType['deleted'].eq(0),
                tableEventType['deleted'].eq(0),
                tableActionTypeIdentification['deleted'].eq(0),
                tableRBAccountingSystem['urn'].eq(u'urn:oid:1.2.643.5.1.13.13.99.2.857'),
                tableActionTypeIdentification2['deleted'].eq(0),
                tableRBAccountingSystem2['urn'].eq(u'urn:oid:1.2.643.5.1.13.13.99.2.857**'),
                tableEGISZ['CODE'].eq(tableActionTypeIdentification2['value'])
               ]
        if self.chkAdditional.isChecked():
            cond.append(tableEGISZ['BASIC_ADDITIONAL'].eq(2))
            cond.append(u'''EXISTS(SELECT ATI.master_id
            FROM ActionType_Identification AS ATI
            INNER JOIN rbAccountingSystem AS rbAS ON rbAS.id = ATI.system_id
            WHERE ATI.master_id = ActionType.id AND rbAS.urn = 'urn:oid:1.2.643.5.1.13.13.99.2.857*'
            AND ATI.deleted = 0 AND ATI.value = 2)''')
        else:
            cond.append(tableEGISZ['BASIC_ADDITIONAL'].ne(2))
            cond.append(u'''NOT EXISTS(SELECT ATI.master_id
            FROM ActionType_Identification AS ATI
            INNER JOIN rbAccountingSystem AS rbAS ON rbAS.id = ATI.system_id
            WHERE ATI.master_id = ActionType.id AND rbAS.urn = 'urn:oid:1.2.643.5.1.13.13.99.2.857*'
            AND ATI.deleted = 0 AND ATI.value = 2)''')
        if self.eventTypeId:
            cond.append(tableEventType['id'].eq(self.eventTypeId))
        else:
            eventTypeIdList = db.getDistinctIdList(tableEventType, [tableEventType['id']], [tableEventType['context'].like(u'inspection%'), tableEventType['deleted'].eq(0)], 'EventType.id DESC')
            if eventTypeIdList:
                cond.append(tableEventType['id'].inlist(eventTypeIdList))
        if self.chkCheckAge.isChecked():
            years = self.clientAge[3] if (self.clientAge and len(self.clientAge) == 4) else None
            if years is not None:
                if years >= 18:
                    cond.append(tableEGISZ['SECTION'].eq(1))
                else:
                    cond.append(tableEGISZ['SECTION'].eq(2))
        if self.chkCheckMKB.isChecked():
            if self.MKBList:
                MKBList = self.MKBList[self.cmbCheckMKB.currentIndex()]
                condMKB = []
                for MKB in MKBList:
                    condMKB.append(tableEGISZ['MKB'].contain(MKB))
                    condMKB.append(tableEGISZ['MKB'].contain(MKB[:3] if len(MKB) >= 3 else MKB))
                condMKB.extend([tableEGISZ['MKB'].eq(''), tableEGISZ['MKB'].position('-')])
                cond.append(db.joinOr(condMKB))
        records = db.getRecordList(queryTable, cols,
                                       where = cond,
                                       order = u'ActionType.code ASC, ActionType.name ASC')
        actionTypeList = {}
        for record in records:
            isAgeSexETA = True
            ageETA = forceString(record.value('ageETA'))
            if ageETA and self.clientAge:
                ageSelector = parseAgeSelector(ageETA)
                if not checkAgeSelector(ageSelector, self.clientAge):
                    isAgeSexETA = False
            sexETA = forceInt(record.value('sexETA'))
            if sexETA and self.clientSex and self.clientSex != sexETA:
                isAgeSexETA = False
            if isAgeSexETA:
                mkbRecord = forceString(record.value('MKB'))
                if self.chkCheckMKB.isChecked():
                    mkbList = mkbRecord.split(';')
                    for MKB in MKBList:
                        if len(mkbList) >= 1:
                            for diagList in mkbList:
                                isMKB = False
                                diagSplit = diagList.split('-')
                                if len(diagSplit) == 2:
                                    if trim(diagSplit[0]) <= MKB and MKB <= trim(diagSplit[1]):
                                        isMKB = True
                                        break
                                    elif len(MKB) >= 3:
                                        if (len(trim(diagSplit[0])) <= 3 and trim(diagSplit[0]) <= MKB[:3]) or (len(trim(diagSplit[0])) > 3 and trim(diagSplit[0]) <= MKB):
                                            if (len(trim(diagSplit[1])) <= 3 and MKB[:3] <= trim(diagSplit[1])) or (len(trim(diagSplit[1])) > 3 and MKB <= trim(diagSplit[1])):
                                                isMKB = True
                                                break
                                elif len(diagSplit) == 1:
                                    if MKB in trim(diagSplit[0]):
                                        isMKB = True
                                        break
                                    elif len(MKB) >= 3 and len(trim(diagSplit[0])) <= 3:
                                        if MKB[:3] in trim(diagSplit[0]):
                                            isMKB = True
                                            break
                        else:
                            isMKB = True
                        if isMKB:
                            break
                if isMKB:
                    actionTypeId = forceRef(record.value('id'))
                    if actionTypeId and actionTypeId not in actionTypeIdList:
                        actionTypeIdList.append(actionTypeId)
                        if self.chkCheckMKB.isChecked() and MKBList:
                            actionTypeMKBList[actionTypeId] = MKB
                        else:
                            actionTypeMKBList[actionTypeId] = mkbRecord
                        basicAdditional = forceInt(record.value('BASIC_ADDITIONAL'))
                        if not basicAdditional:
                            basicAdditional = forceInt(record.value('additional'))
                        basicAdditionalDict[actionTypeId] = basicAdditional
                        codeAT = forceString(record.value('codeAT')).upper()
                        nameAT = forceString(record.value('nameAT')).upper()
                        actionTypeList[actionTypeId] = (codeAT, nameAT)
        for row, id in enumerate(actionTypeIdList):
            actionTypeLine = actionTypeList.get(id, None)
            if actionTypeLine:
                codeAT, nameAT = actionTypeLine
                existCodeRows= self.actionsCacheByCode.get(codeAT, [])
                if row not in existCodeRows:
                    existCodeRows.append(row)
                    self.actionsCacheByCode[codeAT] = existCodeRows
                existName = self.actionsCodeCacheByName.get(nameAT, None)
                if existName is None:
                    self.actionsCodeCacheByName[nameAT] = codeAT
        return actionTypeIdList, basicAdditionalDict, actionTypeMKBList


    @pyqtSignature('QString')
    def on_edtFindByCode_textChanged(self, text):
        self.on_btnSelectClearAll_clicked()
        self.showRowList = []
        self.isFindByCode = True
        if text:
            self.findByCode(text)
            for row, actionTypeId in enumerate(self.actionTypeIdList):
                if row >= 0:
                    if row not in self.showRowList:
                        self.tblF088AddActions30.hideRow(row)
                    elif row in self.showRowList:
                        self.tblF088AddActions30.showRow(row)
        else:
            for row, actionTypeId in enumerate(self.actionTypeIdList):
                if row >= 0:
                    self.tblF088AddActions30.showRow(row)
        self.tblF088AddActions30.clearSelection()
        self.tblF088AddActions30.setCurrentRow(0)


    def findByCode(self, value):
        uCode = unicode(value).upper()
        codes = self.actionsCacheByCode.keys()
        codes.sort()
        for c in codes:
            if unicode(c).startswith(uCode):
                rows = self.actionsCacheByCode[c]
                for row in rows:
                    if row not in self.showRowList:
                        self.showRowList.append(row)
        self.findByName(value)


    def findByName(self, name):
        uName = unicode(name).upper()
        names = self.actionsCodeCacheByName.keys()
        for n in names:
            if uName in n:
                code = self.actionsCodeCacheByName[n]
                rows =  self.actionsCacheByCode.get(code, None)
                for row in rows:
                    if row not in self.showRowList:
                        self.showRowList.append(row)


    @pyqtSignature('bool')
    def on_chkCheckAge_toggled(self, checked):
        self.loadData()


    @pyqtSignature('bool')
    def on_chkCheckMKB_toggled(self, checked):
        self.loadData()


    @pyqtSignature('int')
    def on_cmbCheckMKB_currentIndexChanged(self, value):
        if self.chkCheckMKB.isChecked():
            self.loadData()


    @pyqtSignature('bool')
    def on_chkAdditional_toggled(self, checked):
        self.loadData()


    @pyqtSignature('')
    def on_btnSave_clicked(self):
        self.getAddActions30List()


    @pyqtSignature('')
    def on_btnSelectAll_clicked(self):
        self.addActions30IdList = []
        self.tblF088AddActions30.model().setSelectedAll(self.showRowList, self.isFindByCode)
        self.updateSelectedCount()


    @pyqtSignature('')
    def on_btnSelectClearAll_clicked(self):
        self.addActions30IdList = []
        self.tblF088AddActions30.model().setSelectedClearAll()
        self.updateSelectedCount()


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.addActions30IdList = []
        self.close()


    def getAddActions30List(self):
        self.addActions30IdList = self.tblF088AddActions30.model().getSelectedIdList()
        self.close()


    def getBasicAdditional(self):
        return self.basicAdditionalDict


    def values(self):
        return self.addActions30IdList


    def setValue(self, addActions30IdList):
        self.addActions30IdList = addActions30IdList


class CF088AddActions30TableModel(CTableModel):
    class CEnableCol(CBoolCol):
        def __init__(self, title, fields, defaultWidth, selector):
            CBoolCol.__init__(self, title, fields, defaultWidth)
            self.selector = selector

        def checked(self, values):
            id = forceRef(values[0])
            if self.selector.isSelected(id):
                return CBoolCol.valChecked
            else:
                return CBoolCol.valUnchecked

    class CMKBCol(CCol):
        def __init__(self, title, fields, defaultWidth, obj, alignment='l'):
            CCol.__init__(self, title, fields, defaultWidth, alignment)
            self.obj = obj

        def format(self, values):
            id = forceRef(values[0])
            if id and self.obj and self.obj.actionTypeMKBList:
                return toVariant(self.obj.actionTypeMKBList.get(id, u''))
            else:
                return CCol.invalid

    class CActionTypeCol(CCol):
        def __init__(self, title, defaultWidth, showFields=CRBComboBox.showCodeAndName, alignment='l'):
            CCol.__init__(self, title, ['id'], defaultWidth, alignment)
            self.data = CRBModelDataCache.getData('ActionType', True, '')
            self.showFields = showFields

        def format(self, values):
            id = forceRef(values[0])
            if id:
                return toVariant(self.data.getStringById(id, self.showFields))
            else:
                return CCol.invalid

    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.enableIdList = []
        self.includeItems = {}
        self.actionTypeMKBList = {}
        self.addColumn(CF088AddActions30TableModel.CEnableCol(u'Выбрать', ['id'], 5, self))
        self.addColumn(CF088AddActions30TableModel.CMKBCol(u'МКБ', ['id'], 10, self))
        self.addColumn(CF088AddActions30TableModel.CActionTypeCol(u'Действие', 25))
        self.setTable('ActionType')


    def setActionTypeMKBList(self, actionTypeMKBList):
        self.actionTypeMKBList = actionTypeMKBList


    def flags(self, index):
        result = CTableModel.flags(self, index)
        if index.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        id = self._idList[row]
        if role == Qt.CheckStateRole and column == 0:
            id = self._idList[row]
            if id:
                self.setSelected(id, forceInt(value) == Qt.Checked)
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return CTableModel.setData(self, index, value, role)


    def setSelected(self, id, value):
        present = self.isSelected(id)
        if value:
            if not present:
                self.enableIdList.append(id)
                QObject.parent(self).updateSelectedCount()
        else:
            if present:
                self.enableIdList.remove(id)
                QObject.parent(self).updateSelectedCount()


    def isSelected(self, id):
        return id in self.enableIdList


    def getSelectedIdList(self):
        return self.enableIdList


    def setSelectedAll(self, showRowList=[], isFindByCode=False):
        value = toVariant(Qt.Checked)
        itemIdList = self.idList()
        for row, id in enumerate(itemIdList):
            if not self.isSelected(id) and ((isFindByCode and row in showRowList) or not isFindByCode):
                index = self.index(row, 0)
                self.setData(index, value, role=Qt.CheckStateRole)


    def setSelectedClearAll(self):
        value = toVariant(Qt.Unchecked)
        itemIdList = self.idList()
        for row, id in enumerate(itemIdList):
            if self.isSelected(id):
                index = self.index(row, 0)
                self.setData(index, value, role=Qt.CheckStateRole)

