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
from PyQt4.QtCore import Qt, pyqtSignature, QVariant

from Accounting.CCAlgorithm  import CCCAlgorithm
from library.DialogBase      import CDialogBase
from library.InDocTable      import (
                                      CInDocTableModel,
                                      CEnumInDocTableCol,
                                      CFloatInDocTableCol,
                                      CInDocTableCol,
                                      CRBInDocTableCol,
                                    )
from library.interchange     import (
                                      getLineEditValue,
                                      getTextEditValue,
                                      setLineEditValue,
                                      setTextEditValue,
                                    )
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CTextCol
from library.Utils           import (
                                      exceptionToUnicode,
                                      forceBool,
                                      forceInt,
                                      forceRef,
                                      forceString,
                                      toVariant,
                                    )


from RefBooks.Tables import rbCode, rbName

from .Ui_RBContractCoefficientType import Ui_RBContractCoefficientType
from .Ui_ContractCoefficientTestDialog import Ui_ContractCoefficientTestDialog

SexList = ['', u'М', u'Ж']


class CRBContractCoefficientTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',          [rbCode], 20),
            CTextCol(u'Региональный код', ['regionalCode'], 20),
            CTextCol(u'Федеральный код', ['federalCode'], 20),
            CTextCol(u'Наименование', [rbName], 40),
            ], 'rbContractCoefficientType', [rbCode, rbName])
        self.setWindowTitleEx(u'Типы тарифных коэффициентов')


    def getItemEditor(self):
        return CRBContractCoefficientTypeEditor(self)

#
# ##########################################################################
#

class CRBContractCoefficientTypeEditor(CItemEditorBaseDialog, Ui_RBContractCoefficientType):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbContractCoefficientType')
        self.addModels('Signs', CSignsModel(self))
        self.setupUi(self)
        self.setWindowTitleEx(u'Тип тарифного коэффициента')
        self.tblSigns.setModel(self.modelSigns)
        self.setupDirtyCather()
        self.tblSigns.addMoveRow()
        self.tblSigns.popupMenu().addSeparator()
        self.tblSigns.addPopupDelRow()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode,         record, rbCode)
        setLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        setLineEditValue(self.edtFederalCode,  record, 'federalCode')
        setLineEditValue(self.edtName,         record, rbName)
        setTextEditValue(self.edtAlgorithm,    record, 'algorithm')
        itemId = self.itemId()
        self.modelSigns.loadItems(itemId)


    def checkDataEntered(self):
        result = CItemEditorBaseDialog.checkDataEntered(self)
        if result:
            algorithm = unicode(self.edtAlgorithm.toPlainText()).strip()
            if algorithm:
                result = CCCAlgorithm.isOk(algorithm) or self.checkInputMessage(u'алгоритм расчёта', True, self.edtAlgorithm)
        return result


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtCode,         record, rbCode)
        getLineEditValue(self.edtRegionalCode, record, 'regionalCode')
        getLineEditValue(self.edtFederalCode,  record, 'federalCode')
        getLineEditValue(self.edtName,         record, rbName)
        getTextEditValue(self.edtAlgorithm,    record, 'algorithm')
        return record


    def saveInternals(self, id):
        self.modelSigns.saveItems(id)


    @pyqtSignature('')
    def on_btnTestAlgorithm_clicked(self):
        dlg = CContractCoefficientTestDialog(self)
        dlg.setAlgorithm(self.edtAlgorithm.toPlainText())
        if dlg.exec_():
            self.edtAlgorithm.setPlainText(dlg.getAlgorithm())


class CLocResultInDocTableCol(CRBInDocTableCol):
    def toString(self, val, record):
        if forceRef(val):
            return CRBInDocTableCol.toString(self, val, record)
        else:
            return toVariant(u'не задано')


    def setEditorData(self, editor, value, record):
        eventPurposeId = forceRef(record.value('eventPurpose_id'))
        if eventPurposeId:
            editor.setFilter('eventPurpose_id = %d' % eventPurposeId)
        editor.setValue(forceInt(value))


class CSignsModel(CInDocTableModel):
    # В этой модели есть такое "украшение".
    # Записи rbContractCoefficientType_Sign используются
    # "по ИЛИ" если они находятся в разных группах
    # и по "И" если они находятся в одной группе.
    # Найдена возможность реализовать более привычную запись - с И и ИЛИ
    # этому посвящены поля junction и "волшебство" в flags/data/loadItems/...
    #
    # логика группировки скопирована из RefBooks/RBJobPurpose.py
    # будет использовата третий раз - нужно будет выносить в отдельный класс (миксин?)
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbContractCoefficientType_Sign', 'id', 'master_id', parent)
        self.addExtCol(CEnumInDocTableCol(u'Связка', 'junction', 5, (u'или', u'и')), QVariant.Int)
        self.addCol(CEnumInDocTableCol( u'Пол',            'sex',  5, SexList))
        self.addCol(CInDocTableCol(     u'Возраст',        'age',  12))
        self.addCol(CRBInDocTableCol(   u'Социальный статус', 'socStatusType_id', 15, 'rbSocStatusType'))
        self.addCol(CInDocTableCol(     u'Шаблон кода МЭС','mesCodeRegExp', 32))
        self.addCol(CRBInDocTableCol(   u'Особенность выполнения МЭС', 'mesSpecification_id', 15, 'rbMesSpecification'))
        self.addCol(CInDocTableCol(     u'Шаблон кода КСГ','csgCodeRegExp', 32))
        self.addCol(CRBInDocTableCol(   u'Особенность выполнения КСГ', 'csgSpecification_id', 15, 'rbMesSpecification'))
        self.addCol(CRBInDocTableCol(   u'Тип диагноза', 'diagnosisType_id', 15, 'rbDiagnosisType'))
        self.addCol(CInDocTableCol(     u'Шаблон кода МКБ','mkbRegExp',  32))
        self.addCol(CInDocTableCol(     u'Шаблон кода услуги','serviceCodeRegExp',  32))
        self.addExtCol(CRBInDocTableCol(u'Назначение типа события', 'eventPurpose_id', 32, 'rbEventTypePurpose'),
                       QVariant.Int)
        self.addCol(CLocResultInDocTableCol(   u'Результат обращения', 'result_id', 15, 'rbResult'))
        self.addCol(CEnumInDocTableCol(u'Срочность',  'urgency', 5, (u'-', u'срочно', u'не срочно')))
        self.addCol(CRBInDocTableCol(u'Особенности выполнения действий',  'actionSpecification_id', 15, 'rbActionSpecification'))
        self.addCol(CFloatInDocTableCol(u'Минимальное количество',  'minAmount', 15, low=0, precision=2))
        self.addCol(CFloatInDocTableCol(u'Максимальное количество', 'maxAmount', 15, low=0, precision=2))
#        self.addCol(CIntInDocTableCol(u'', 'maxAmount', 15, low=0, precision=2))
        self.addHiddenCol('grouping')

        self.colEventPurposeIdx = self.getColIndex('eventPurpose_id')
        self.colResultIdIdx = self.getColIndex('result_id')


    def _cellIsDisabled(self, index):
        row = index.row()
        column = index.column()
        if column == 0:
            if row == 0:
                return True
        elif column == self.colResultIdIdx:
            eventPurposeId = forceRef(self.value(row, 'eventPurpose_id'))
            return eventPurposeId is None
        return False


    def _findSimilarResult(self,  eventPurposeId, oldResultId):
        if oldResultId:
            db = QtGui.qApp.db
            tableResult = db.table('rbResult')
            resultName = forceString(db.translate(tableResult, 'id', oldResultId, 'name'))
            idList = db.getIdList(tableResult,
                                  'id',
                                   db.joinAnd([ tableResult['eventPurpose_id'].eq(eventPurposeId),
                                                tableResult['name'].eq(resultName)
                                              ]
                                             )
                                 )
            if idList:
                return idList[0]
        return None


    def flags(self, index):
        if self._cellIsDisabled(index):
            return Qt.ItemIsSelectable
        return CInDocTableModel.flags(self, index)


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self._cellIsDisabled(index):
                return QVariant()
        return CInDocTableModel.data(self, index, role)


    def setData(self, index, value, role=Qt.EditRole):
        column = index.column()
        result = CInDocTableModel.setData(self, index, value, role)
        if result and column == self.colEventPurposeIdx:
            row = index.row()
            eventPurposeId = forceRef(value)
            if eventPurposeId:
                resultId = self._findSimilarResult(eventPurposeId, forceRef(self.value(row, 'result_id')))
            else:
                resultId = None
            self.setValue(row, 'result_id', resultId)
        return result


    def loadItems(self, masterId):
        db = QtGui.qApp.db
        CInDocTableModel.loadItems(self, masterId)
        prevGrouping = -1
        for item in self._items:
            grouping = forceInt(item.value('grouping'))
            item.setValue('junction', grouping == prevGrouping) # True == «И»
            prevGrouping = grouping

            resultId = forceRef(item.value('result_id'))
            if resultId:
                eventPurposeId = db.translate('rbResult', 'id',  resultId,  'eventPurpose_id')
                item.setValue('eventPurpose_id', eventPurposeId)


    def saveItems(self, masterId):
        if self._items:
            grouping = -1
            for item in self._items:
                junction = forceBool(item.value('junction')) # True == «И»
                if grouping == -1 or not junction:
                    grouping = grouping+1
                item.setValue('grouping', grouping)

            grouping = -1
            for item in reversed(self._items):
                currGrouping = forceInt(item.value('grouping'))
                if grouping != currGrouping:
                    avail = forceInt(item.value('avail'))
                    grouping = currGrouping
                else:
                    item.setValue('avail', avail)

        CInDocTableModel.saveItems(self, masterId)



class CContractCoefficientTestDialog(Ui_ContractCoefficientTestDialog, CDialogBase):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addObject('btnEval', QtGui.QPushButton(u'В&ычислить', self))
        self.setupUi(self)
        self.buttonBox.addButton(self.btnEval, self.buttonBox.ActionRole)


    def setAlgorithm(self, code):
        self.edtAlgorithm.setPlainText(code)


    def getAlgorithm(self):
        return self.edtAlgorithm.toPlainText()


    @pyqtSignature('')
    def on_btnEval_clicked(self):
        code = self.edtAlgorithm.toPlainText()
        try:
            a = CCCAlgorithm(code)
            k = self.edtK.value()
            duration = self.edtDuration.value()
            minDuration = self.edtMinDuration.value()
            maxDuration = self.edtMaxDuration.value()
            avgDuration = self.edtAvgDuration.value()
            result = a(k, duration, minDuration, maxDuration, avgDuration)
            if isinstance(result, float):
                resultStr = '%s' % result
            else:
                resultStr = u'%r (внимание! получено значение типа %r)' % (result,  type(result))
        except ZeroDivisionError, e:
            resultStr = u'Ошибка деления на 0'
        except NameError, e:
            resultStr = u'Ошибка: '+ exceptionToUnicode(e)
        except SyntaxError, e:
            resultStr = u'Синтаксическая ошибка'
        except Exception, e:
            resultStr = u'Ошибка: '+ exceptionToUnicode(e)
        self.lblResult.setText(resultStr)
