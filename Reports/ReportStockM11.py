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
from PyQt4.QtCore import Qt, SIGNAL, QDateTime, QModelIndex, QVariant

from library.DialogBase import CConstructHelperMixin
from library.Utils      import forceDouble, forceString, forceStringEx, toVariant

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CReportViewDialog

from Ui_StockRequisitionList import Ui_StockRequisitionList


def selectData(invoiceId, type, numberList, numberListBool, unitName):
    db = QtGui.qApp.db
    colsQntToNumbers = u''
    colsSumToNumbers = u''
    if type:
        tableStock = db.table('StockRequisition')
        tableStockItem = db.table('StockRequisition_Item')
        stmt="""
            SELECT DISTINCT
                rbNomenclature.name AS nomenclatureName,
                rbNomenclature.originName,
                rbNomenclature.internationalNonproprietaryName,
                rbNomenclature.mnnLatin,
                rbNomenclature.code AS nomenclatureCode,
                rbNomenclature.id AS nomenclatureId,
                rbNomenclature.dosageValue,
                StockRequisition_Item.qnt,
                StockRequisition_Item.satisfiedQnt,
                rbLfForm.name AS lfFormName,
                rbUnit.code AS unitCode,
                rbUnit.name AS unitName,
                StockRequisition.number,
                StockRequisition.supplier_id,
                StockRequisition.recipient_id%s%s
            FROM StockRequisition
                INNER JOIN StockRequisition_Item ON StockRequisition_Item.master_id = StockRequisition.id
                LEFT JOIN  rbNomenclature        ON rbNomenclature.id = StockRequisition_Item.nomenclature_id
                LEFT JOIN  rbUnit                ON rbUnit.id = rbNomenclature.unit_id
                LEFT JOIN  rbLfForm              ON rbLfForm.id = rbNomenclature.lfForm_id
            WHERE %s
            ORDER BY %s
        """
        if numberListBool:
            numberStr = u','.join(u'\'%s\''%(forceString(number)) for number in numberList if number)
            if numberStr:
                colsQntToNumbers = u''', (SELECT SUM(SMI.qnt)
                    FROM StockMotion AS SM
                    INNER JOIN StockMotion_Item AS SMI ON SMI.master_id = SM.id
                    WHERE SM.number IN (%s)
                    AND SMI.nomenclature_id = StockRequisition_Item.nomenclature_id) AS qntToNumbers'''%(numberStr)
                colsSumToNumbers = u''', (SELECT SUM(SMI.sum)
                    FROM StockMotion AS SM
                    INNER JOIN StockMotion_Item AS SMI ON SMI.master_id = SM.id
                    WHERE SM.number IN (%s)
                    AND SMI.nomenclature_id = StockRequisition_Item.nomenclature_id) AS sumToNumbers'''%(numberStr)
    else:
        tableStock = db.table('StockMotion')
        tableStockItem = db.table('StockMotion_Item')
        stmt="""
            SELECT DISTINCT
                rbNomenclature.name AS nomenclatureName,
                rbNomenclature.originName,
                rbNomenclature.internationalNonproprietaryName,
                rbNomenclature.mnnLatin,
                rbNomenclature.code AS nomenclatureCode,
                rbNomenclature.id AS nomenclatureId,
                rbNomenclature.dosageValue,
                StockMotion_Item.qnt,
                StockMotion_Item.sum,
                rbLfForm.name AS lfFormName,
                rbUnit.code AS unitCode,
                rbUnit.name AS unitName,
                StockMotion.number,
                StockMotion.supplier_id,
                StockMotion.receiver_id%s%s
            FROM StockMotion
                INNER JOIN StockMotion_Item ON StockMotion_Item.master_id = StockMotion.id
                LEFT JOIN  rbNomenclature   ON rbNomenclature.id = StockMotion_Item.nomenclature_id
                LEFT JOIN  rbUnit           ON rbUnit.id = rbNomenclature.unit_id
                LEFT JOIN  rbLfForm         ON rbLfForm.id = rbNomenclature.lfForm_id
            WHERE %s
            ORDER BY %s
        """
        if numberListBool:
            numberStr = u','.join(u'\'%s\''%(forceString(number)) for number in numberList if number)
            if numberStr:
                colsQntToNumbers = u''', (SELECT SUM(SRI.qnt)
                    FROM StockRequisition AS SR
                    INNER JOIN StockRequisition_Item AS SRI ON SRI.master_id = SR.id
                    WHERE SR.number IN (%s)
                    AND SRI.nomenclature_id = StockMotion_Item.nomenclature_id) AS qntToNumbers'''%(numberStr)
    cond = [tableStock['id'].eq(invoiceId),
            tableStock['deleted'].eq(0)
            ]
    return db.query(stmt % (colsQntToNumbers, colsSumToNumbers, db.joinAnd(cond), ','.join([tableStockItem['idx'].name(), unitName, u'dosageValue', u'lfFormName', u'unitCode', u'unitName'])))


class CReportStockM11(CReport):
    def __init__(self, parent, invoiceId, type):
        CReport.__init__(self, parent)
        self.setTitle(u'Требование - Накладная')
        self.invoiceId = invoiceId
        self.parent = parent
        self.type = type


    def reportLoop(self):
        params = self.getDefaultParams()
        while True:
            setupDialog = self.getSetupDialog(self.parent)
            setupDialog.setParams(params)
            if not setupDialog.exec_():
                break
            params = setupDialog.params()
            preCheckData = getattr(self, 'preCheckData', None)
            if preCheckData is not None and not preCheckData(self.parent, params):
                continue

            self.saveDefaultParams(params)
            try:
                QtGui.qApp.setWaitCursor()
                reportResult = self.build(params)
            finally:
                QtGui.qApp.restoreOverrideCursor()
            viewDialog = CReportViewDialog(self.parent)
            if self.viewerGeometry:
                viewDialog.restoreGeometry(self.viewerGeometry)
            viewDialog.setWindowTitle(self.title())
            viewDialog.setRepeatButtonVisible()
            viewDialog.setText(reportResult)
            viewDialog.setOrientation(self.orientation)
            if self.pageFormat:
                viewDialog.setPageFormat(self.pageFormat)
            if self.lineWrapMode is not None:
                viewDialog.txtReport.setLineWrapMode(self.lineWrapMode)
            done = not viewDialog.exec_()
            self.viewerGeometry = viewDialog.saveGeometry()
            if done:
                break


    def dumpParams(self, cursor, params):
        description = []
        numberList = params.get('numberList', [])
        if numberList and (len(numberList) > 1 or (len(numberList) == 1 and numberList[0] != None)  and numberList[0] != ''):
            description.append(u'Номера требований: %s'%(u', '.join(number for number in numberList if number)))
        #description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getSetupDialog(self, parent):
        result = CStockRequisitionListDialog(parent, self.type)
        return result


    def build(self, params):
        numberList = params.get('numberList', [])
        numberListBool = numberList and (len(numberList) > 1 or (len(numberList) == 1 and numberList[0] != None)  and numberList[0] != '')
        unitNameTNRussian = params.get('unitNameTNRussian', 0)
        unitNameTNLatin = params.get('unitNameTNLatin', 0)
        unitNameMNNRussian = params.get('unitNameMNNRussian', 0)
        unitNameMNNLatin = params.get('unitNameMNNLatin', 0)
        unitNameSortList = []
        unitNameSortList = [(unitNameTNRussian,  u'nomenclatureName'),
                            (unitNameTNLatin,    u'originName'),
                            (unitNameMNNRussian, u'internationalNonproprietaryName'),
                            (unitNameMNNLatin,   u'mnnLatin')
                            ]
        unitNameSortBool = False
        if unitNameTNRussian or unitNameTNLatin or unitNameMNNRussian or unitNameMNNLatin:
            unitNameSortList.sort(key=lambda item: item[0])
            unitNameSortListTemp = unitNameSortList
            for i, unitNameSort in enumerate(unitNameSortListTemp):
                if unitNameSort[0] == 0:
                    unitNameSortList.pop(i)
            unitNameSortBool = True
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        numberInvoice = u''
        OSSupplierName = u''
        OSReceiverName = u''
        supplierPersonName = u''
        receiverPersonName = u''
        supplierPersonPost = u''
        receiverPersonPost = u''
        if self.invoiceId:
            db = QtGui.qApp.db
            tableOSSupplier = db.table('OrgStructure').alias('OSSupplier')
            tableOSReceiver = db.table('OrgStructure').alias('OSReceiver')
            if self.type:
                tableStock = db.table('StockRequisition')
                tableQuery = tableStock.leftJoin(tableOSSupplier, tableOSSupplier['id'].eq(tableStock['supplier_id']))
                tableQuery = tableQuery.leftJoin(tableOSReceiver, tableOSReceiver['id'].eq(tableStock['recipient_id']))
            else:
                tableStock = db.table('StockMotion')
                tableQuery = tableStock.leftJoin(tableOSSupplier, tableOSSupplier['id'].eq(tableStock['supplier_id']))
                tableQuery = tableQuery.leftJoin(tableOSReceiver, tableOSReceiver['id'].eq(tableStock['receiver_id']))
            cols = [tableStock['number'],
                    tableOSSupplier['name'].alias('OSSupplierName'),
                    tableOSReceiver['name'].alias('OSReceiverName'),
                   ]
            if self.type:
                pass
            else:
                cols.append(u'''(SELECT vrbPersonWithSpeciality.name FROM vrbPersonWithSpeciality WHERE vrbPersonWithSpeciality.id = StockMotion.supplierPerson_id) AS supplierPersonName''')
                cols.append(u'''(SELECT vrbPersonWithSpeciality.name FROM vrbPersonWithSpeciality WHERE vrbPersonWithSpeciality.id = StockMotion.receiverPerson_id) AS receiverPersonName''')
                cols.append(u'''(SELECT rbPost.name FROM Person INNER JOIN rbPost ON rbPost.id = Person.post_id WHERE Person.id = StockMotion.supplierPerson_id AND Person.deleted = 0) AS supplierPersonPost''')
                cols.append(u'''(SELECT rbPost.name FROM Person INNER JOIN rbPost ON rbPost.id = Person.post_id WHERE Person.id = StockMotion.receiverPerson_id AND Person.deleted = 0) AS receiverPersonPost''')

            record = db.getRecordEx(tableQuery, cols, [tableStock['id'].eq(self.invoiceId), tableStock['deleted'].eq(0)])
            if record:
                OSSupplierName = forceString(record.value('OSSupplierName'))
                OSReceiverName = forceString(record.value('OSReceiverName'))
                numberInvoice = forceString(record.value('number'))
                supplierPersonName = forceString(record.value('supplierPersonName'))
                receiverPersonName = forceString(record.value('receiverPersonName'))
                supplierPersonPost = forceString(record.value('supplierPersonPost'))
                receiverPersonPost = forceString(record.value('receiverPersonPost'))
        columns = [('30%', [u''], CReportBase.AlignLeft), ('55%', [], CReportBase.AlignLeft), ('8%', [], CReportBase.AlignLeft), ('7%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=6, border=0, cellPadding=2, cellSpacing=0)
        table.setText(0, 0, u'')
        table.setText(0, 1, u'')
        table.setText(0, 2, u'Типовая межотраслевая форма № М–11', blockFormat=CReportBase.AlignRight)
        table.setText(0, 3, u'', blockFormat=CReportBase.AlignRight)
        table.setText(1, 0, u'')
        table.setText(1, 1, u'')
        table.setText(1, 2, u'Утверждена постановлением Госкомстата России', blockFormat=CReportBase.AlignRight)
        table.setText(1, 3, u'', blockFormat=CReportBase.AlignRight)
        table.setText(2, 0, u'')
        table.setText(2, 1, u'')
        table.setText(2, 2, u'от 30.10.97 № 71а', blockFormat=CReportBase.AlignRight)
        table.setText(2, 3, u'', blockFormat=CReportBase.AlignRight)
        table.setText(3, 0, u'')
        boldChars = QtGui.QTextCharFormat()
        font = boldChars.font()
        font.setItalic(True)
        boldChars.setFont(font)
        boldChars.setProperty(QtGui.QTextFormat.FontSizeIncrement, QVariant(3))
        table.setText(3, 1, u'ТРЕБОВАНИЕ-НАКЛАДНАЯ №  %s'%(numberInvoice), charFormat=boldChars)
        table.setText(3, 2, u'')
        table.setText(3, 3, u'Коды', blockFormat=CReportBase.AlignCenter)
        table.setText(4, 0, u'')
        table.setText(4, 1, u'')
        table.setText(4, 2, u'Форма по ОКУД', blockFormat=CReportBase.AlignRight)
        table.setText(4, 3, u'315006', blockFormat=CReportBase.AlignCenter)
        bigChars = QtGui.QTextCharFormat()
        bigChars.setProperty(QtGui.QTextFormat.FontSizeIncrement, QVariant(2))
        table.setText(5, 0, u'Организация', charFormat=bigChars)
        currentOrgId = QtGui.qApp.currentOrgId()
        table.setText(5, 1, u'%s'%(forceString(QtGui.qApp.db.translate(u'Organisation', 'id', currentOrgId, u'shortName')) if currentOrgId else u''), charFormat=bigChars)
        table.setText(5, 2, u'по ОКПО', blockFormat=CReportBase.AlignRight)
        table.setText(5, 3, u'36279727', blockFormat=CReportBase.AlignCenter)
        table.mergeCells(0, 2, 1,  2)
        table.mergeCells(1, 2, 1,  2)
        table.mergeCells(2, 2, 1,  2)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
                          ('8%',    [ u'Дата составления',                                  u''], CReportBase.AlignLeft),
                          ('9%',    [ u'Код вида операции ',                                u''], CReportBase.AlignLeft),
                          ('12.5%', [ u'Отправитель',                                       u'структурное подразделение'], CReportBase.AlignLeft),
                          ('12.5%', [ u'',                                                  u'вид деятельности '], CReportBase.AlignLeft),
                          ('12.5%', [ u'Получатель',                                        u'структурное подразделение '], CReportBase.AlignLeft),
                          ('12.5%', [ u'',                                                  u'вид деятельности'], CReportBase.AlignLeft),
                          ('12.5%', [ u'Корреспондирующий счет',                            u'счет, субсчет'], CReportBase.AlignLeft),
                          ('12.5%', [ u'',                                                  u'код аналитичес-кого учета'], CReportBase.AlignLeft),
                          ('8%',    [ u'Учетная единица выпуска продукции (работ, услуг) ', u''], CReportBase.AlignLeft),
                       ]
        table = createTable(cursor, tableColumns, headerRowCount=3)
        table.mergeCells(0, 0, 2,  1)
        table.mergeCells(0, 1, 2,  1)
        table.mergeCells(0, 2, 1,  2)
        table.mergeCells(0, 4, 1,  2)
        table.mergeCells(0, 6, 1,  2)
        table.mergeCells(0, 8, 2,  1)
        table.setText(2, 0, forceString(QDateTime.currentDateTime()))
        table.setText(2, 2, OSSupplierName)
        table.setText(2, 4, OSReceiverName)
        table.setText(2, 8, u'')

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        columns = [('100%', [u''], CReportBase.AlignLeft)]
        table2 = createTable(cursor, columns, headerRowCount=2, border=0, cellPadding=2, cellSpacing=0)
        table2.setText(0, 0, u'Через кого____________________________________________________________________________________________________________________________________________________')
        table2.setText(1, 0, u'Затребовал__________________________________________________________________ Разрешил_______________________________________________________________________')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
                          ('9%', [ u'Корреспондирующий счет',                  u'счет, субсчет',             u'1' ], CReportBase.AlignLeft),
                          ('9%', [ u'',                                        u'код аналитического учета',  u'2' ], CReportBase.AlignLeft),
                          ('10%',[ u'Материальные ценности',                   u'наименование',              u'3' ], CReportBase.AlignLeft),
                          ('9%', [ u'',                                        u'номенклатурный номер',      u'4' ], CReportBase.AlignLeft),
                          ('9%', [ u'Единица измерения',                       u'код',                       u'5' ], CReportBase.AlignLeft),
                          ('9%', [ u'',                                        u'наименование',              u'6' ], CReportBase.AlignLeft),
                          ('9%', [ u'Количество',                              u'затребовано',               u'7' ], CReportBase.AlignRight),
                          ('9%', [ u'',                                        u'отпущено',                  u'8' ], CReportBase.AlignRight),
                          ('9%', [ u'Цена, руб. коп.',                         u'',                          u'9' ], CReportBase.AlignRight),
                          ('9%', [ u'Сумма без учета НДС, руб. коп.',          u'',                          u'10'], CReportBase.AlignRight),
                          ('9%', [ u'Порядковый номер по складской картотеке', u'',                          u'11'], CReportBase.AlignLeft),
                       ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1,  2)
        table.mergeCells(0, 2, 1,  2)
        table.mergeCells(0, 4, 1,  2)
        table.mergeCells(0, 6, 1,  2)
        table.mergeCells(0, 8, 2,  1)
        table.mergeCells(0, 9, 2,  1)
        table.mergeCells(0, 10, 2, 1)

        if self.invoiceId:
            query = selectData(self.invoiceId, self.type, numberList, numberListBool, unitNameSortList[0][1])
            while query.next():
                record = query.record()
                nomenclatureName    = forceString(record.value('nomenclatureName'))
                if unitNameSortBool:
                    for unitNameSort in unitNameSortList:
                        unitName = forceString(record.value(unitNameSort[1]))
                        if unitName:
                            nomenclatureName = unitName
                            break
                nomenclatureCode    = forceString(record.value('nomenclatureCode'))
                nomenclatureId      = forceString(record.value('nomenclatureId'))
                qnt                 = forceDouble(record.value('qnt'))
                sum                 = forceDouble(record.value('sum'))
                sumToNumbers        = forceDouble(record.value('sumToNumbers'))
                satisfiedQnt        = forceDouble(record.value('satisfiedQnt'))
                dosageValue         = forceString(record.value('dosageValue'))
                lfFormName          = forceString(record.value('lfFormName'))
                unitCode            = forceString(record.value('unitCode'))
                unitName            = forceString(record.value('unitName'))
                qntToNumbers        = forceDouble(record.value('qntToNumbers'))
                i = table.addRow()
                table.setText(i, 2, nomenclatureName + (u', %s'%lfFormName if lfFormName else u'') + (u', %s'%(dosageValue + u' ' + unitName) if dosageValue or unitName else u''))
                table.setText(i, 3, nomenclatureCode)
                table.setText(i, 4, unitCode)
                table.setText(i, 5, unitName)
                table.setText(i, 6, qnt if self.type else qntToNumbers)
                table.setText(i, 7, (qntToNumbers if (qntToNumbers and numberListBool) else (satisfiedQnt if (satisfiedQnt or numberListBool) else u'')) if self.type else qnt)
                qntNomenclature = (qntToNumbers if (qntToNumbers and numberListBool) else satisfiedQnt)
                table.setText(i, 8, ((sumToNumbers/qntNomenclature) if (qntNomenclature and numberListBool) else ('0.0' if numberListBool else u'')) if self.type else ((sum/qnt) if qnt else ('0.0' if numberListBool else u'')))
                table.setText(i, 9, (sumToNumbers if numberListBool else u'') if self.type else sum)
                table.setText(i, 10, nomenclatureId) # number)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        columns = [('12.5%', [u''], CReportBase.AlignCenter),
                   ('12.5%', [u''], CReportBase.AlignCenter),
                   ('12.5%', [u''], CReportBase.AlignCenter),
                   ('12,5%', [u''], CReportBase.AlignCenter),
                   ('12.5%', [u''], CReportBase.AlignCenter),
                   ('12.5%', [u''], CReportBase.AlignCenter),
                   ('12.5%', [u''], CReportBase.AlignCenter),
                   ('12,5%', [u''], CReportBase.AlignCenter)
                   ]
        table2 = createTable(cursor, columns, headerRowCount=4, border=0, cellPadding=2, cellSpacing=0)
        boldChars = QtGui.QTextCharFormat()
        font = boldChars.font()
        font.setUnderline(True)
        boldChars.setFont(font)
        if supplierPersonName:
            table2.setText(0, 0, u'')
            table2.setText(0, 1, u'')
            table2.setText(0, 2, u'Отпустил:')
            table2.setText(0, 3, supplierPersonPost, charFormat=boldChars)
            table2.setText(0, 4, u'___________________________________')
            table2.setText(0, 5, supplierPersonName, charFormat=boldChars)
            table2.setText(0, 6, u'')
            table2.setText(0, 7, u'')
            table2.setText(1, 0, u'')
            table2.setText(1, 1, u'')
            table2.setText(1, 2, u'')
            table2.setText(1, 3, u'(должность)')
            table2.setText(1, 4, u'(подпись)')
            table2.setText(1, 5, u'(расшифровка подписи)',)
            table2.setText(1, 6, u'')
            table2.setText(1, 7, u'')
        else:
            table2.setText(0, 0, u'')
            table2.setText(0, 1, u'')
            table2.setText(0, 2, u'Отпустил:')
            table2.setText(0, 3, u'___________________________________')
            table2.setText(0, 4, u'___________________________________')
            table2.setText(0, 5, u'___________________________________')
            table2.setText(0, 6, u'')
            table2.setText(0, 7, u'')
            table2.setText(1, 0, u'')
            table2.setText(1, 1, u'')
            table2.setText(1, 2, u'')
            table2.setText(1, 3, u'(должность)')
            table2.setText(1, 4, u'(подпись)')
            table2.setText(1, 5, u'(расшифровка подписи)')
            table2.setText(1, 6, u'')
            table2.setText(1, 7, u'')
        if receiverPersonName:
            table2.setText(2, 0, u'')
            table2.setText(2, 1, u'')
            table2.setText(2, 2, u'Получил:')
            table2.setText(2, 3, receiverPersonPost, charFormat=boldChars)
            table2.setText(2, 4, u'___________________________________')
            table2.setText(2, 5, receiverPersonName, charFormat=boldChars)
            table2.setText(2, 6, u'')
            table2.setText(2, 7, u'')
            table2.setText(3, 0, u'')
            table2.setText(3, 1, u'')
            table2.setText(3, 2, u'')
            table2.setText(3, 3, u'(должность)')
            table2.setText(3, 4, u'(подпись)')
            table2.setText(3, 5, u'(расшифровка подписи)')
            table2.setText(3, 6, u'')
            table2.setText(3, 7, u'')
        else:
            table2.setText(2, 0, u'')
            table2.setText(2, 1, u'')
            table2.setText(2, 2, u'Получил:')
            table2.setText(2, 3, u'___________________________________')
            table2.setText(2, 4, u'___________________________________')
            table2.setText(2, 5, u'___________________________________')
            table2.setText(2, 6, u'')
            table2.setText(2, 7, u'')
            table2.setText(3, 0, u'')
            table2.setText(3, 1, u'')
            table2.setText(3, 2, u'')
            table2.setText(3, 3, u'(должность)')
            table2.setText(3, 4, u'(подпись)')
            table2.setText(3, 5, u'(расшифровка подписи)')
            table2.setText(3, 6, u'')
            table2.setText(3, 7, u'')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        return doc


class CStockRequisitionListDialog(QtGui.QDialog, Ui_StockRequisitionList, CConstructHelperMixin):
    def __init__(self,  parent, type):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CStockRequisitionListModel(self, type)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.type = type
        self.tblStockRequisitionList.setModel(self.tableModel)
        self.tblStockRequisitionList.setSelectionModel(self.tableSelectionModel)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)


    def setParams(self, params):
        self.tableModel.setItems(params.get('numberList', []))
        self.edtUnitNameTNRussian.setValue(params.get('unitNameTNRussian', 0))
        self.edtUnitNameTNLatin.setValue(params.get('unitNameTNLatin', 0))
        self.edtUnitNameMNNRussian.setValue(params.get('unitNameMNNRussian', 0))
        self.edtUnitNameMNNLatin.setValue(params.get('unitNameMNNLatin', 0))


    def params(self):
        result = {}
        result['numberList'] = self.tableModel.items()
        result['unitNameTNRussian'] = self.edtUnitNameTNRussian.value()
        result['unitNameTNLatin'] = self.edtUnitNameTNLatin.value()
        result['unitNameMNNRussian'] = self.edtUnitNameMNNRussian.value()
        result['unitNameMNNLatin'] = self.edtUnitNameMNNLatin.value()
        return result


    def exec_(self):
        result = QtGui.QDialog.exec_(self)
        return result


class CStockRequisitionListModel(QtGui.QStringListModel):
    column = [u'Номер требования']

    def __init__(self, parent, type):
        QtGui.QStringListModel.__init__(self, parent)
        self.setColumnToType(type)
        self._items = []


    def setColumnToType(self, type):
        if type:
           self.column = [u'Номер накладной']
        else:
            self.column = [u'Номер требования']


    def items(self):
        return self._items


    def setItems(self, items):
        if items:
            self._items = items
        else:
            self._items = [None]
        self.reset()


    def columnCount(self, index = None):
        return 1


    def rowCount(self, index = None):
        return len(self._items)


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable|Qt.ItemIsEditable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if 0 <= row < len(self._items):
            if role == Qt.EditRole:
                return toVariant(self._items[row])
            if role == Qt.DisplayRole:
                return toVariant(self._items[row])
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if 0 <= row < len(self._items) and len(self._items) > 1:
                if value.isNull():
                    rootIndex = self.index(row, column)
                    self.beginRemoveRows(rootIndex, row, row+1)
                    self.removeRows(row, 1, rootIndex)
                    self.endRemoveRows()
                    self._items.pop(row)
                    self.emitRowsChanged(0, len(self._items)-1)
                    self.reset()
                    return True
            if row == len(self._items)-1:
                if value.isNull():
                    return False
                self._items.append('')
                count = len(self._items)
                rootIndex = QModelIndex()
                self.beginInsertRows(rootIndex, count, count)
                self.insertRows(count, 1, rootIndex)
                self.endInsertRows()
            self._items[row] = forceString(value)
            self.emitCellChanged(row, column)
            self.reset()
            return True
        return False


    def createEditor(self, index, parent):
        editor = QtGui.QLineEdit(parent)
        return editor


    def setEditorData(self,column, editor, value, record):
        editor.setText(forceStringEx(value))


    def getEditorData(self, column, editor):
        text = editor.text().trimmed()
        if text:
            return toVariant(text)
        else:
            return QVariant()


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitRowChanged(self, row):
        self.emitRowsChanged(row, row)


    def emitRowsChanged(self, begRow, endRow):
        index1 = self.index(begRow, 0)
        index2 = self.index(endRow, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def afterUpdateEditorGeometry(self, editor, index):
        pass
