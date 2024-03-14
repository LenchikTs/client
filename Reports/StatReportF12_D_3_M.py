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
from PyQt4.QtCore import QDate, QXmlStreamWriter

from library.database     import addDateInRange
from library.DialogBase   import CDialogBase
from library.MapCode      import createMapCodeToRowIdx
from library.Utils        import anyToUnicode, forceBool, forceDate, forceInt, forceString, getPref, getPrefInt

from Reports.Report     import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable
from Reports.StatReport1NPUtil  import havePermanentAttach

from Reports.Ui_ReportF12_D_3_MSetup import Ui_ReportF12_D_3_MSetupDialog


Rows = [
        (u'Туберкулез',                                               '1', 'A15-A19'),
        (u'Злокачественные новообразования:',                         '',  'C15-C97'),
        (u'органов пищеварения',                                      '2', 'C15-C26'),
        (u'трахеи, бронхов, легкого',                                 '3', 'C33-C34'),
        (u'кожи',                                                     '4', 'C43-C44'),
        (u'молочной железы',                                          '5', 'C50'),
        (u'женских половых органов',                                  '6', 'C50-C58'),
        (u'предстательной железы',                                    '7', 'C61'),
        (u'лимфатической и кроветворной ткани',                       '8', 'C81-C96'),
        (u'Анемия',                                                   '9', 'D50-D64'),
        (u'Сахарный диабет',                                          '10','E10-E14'),
        (u'Ожирение',                                                 '11','E66'),
        (u'Нарушения обмена липопротеидов',                           '12','E78'),
        (u'Болезни, характеризующиеся повышенным кровяным давлением', '13','I10-I15'),
        (u'Ишемические болезни сердца',                               '14','I20-I25'),
        (u'Повышенное содержание глюкозы в крови' ,                   '15','R73'),
        (u'Отклонения от нормы, выявленные при получении диагностического изображения в ходе исследования легких','16','R91'),
        (u'Отклонения от нормы, выявленные при получении диагностического изображения в ходе исследования молочной железы','17','R92'),
        (u'Отклонения от нормы, выявленные при проведении функциональных исследований сердечно-сосудистой системы','18','R94.3'),
       ]


def countByGroups(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate):
    db = QtGui.qApp.db
    stmt='''
        SELECT
            IF(Event.payStatus > 0 AND Event.execDate IS NOT NULL AND Event.execDate>=%s AND Event.execDate<=%s, 1, 0) as `done`,
            rbHealthGroup.code as `group`,
            COUNT(Event.id) as cnt
        FROM
            Event
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN Diagnostic    ON (     Diagnostic.event_id = Event.id
                                         AND Diagnostic.diagnosisType_id = (SELECT id FROM rbDiagnosisType WHERE code = '1')
                                       )
            LEFT JOIN rbHealthGroup ON rbHealthGroup.id = Diagnostic.healthGroup_id
            LEFT JOIN Account_Item  ON ( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL)
                                       )
        WHERE
            %s
        GROUP BY
            `done`, `group`
    '''
    tableEvent = db.table('Event')
    cond = []
    cond.append(db.joinOr([db.joinAnd([tableEvent['execDate'].isNotNull(), tableEvent['execDate'].ge(begDate), tableEvent['execDate'].le(endDate)]),
                db.joinAnd([tableEvent['execDate'].isNull(), tableEvent['setDate'].isNotNull(), tableEvent['setDate'].ge(begDate), tableEvent['setDate'].le(endDate)])]))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if onlyPayedEvents:
        cond.append('isEventPayed(Event.id)')
        tableAccountItem = db.table('Account_Item')
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
    return db.query(stmt % (db.formatDate(begDate), db.formatDate(endDate), db.joinAnd(cond)))


def selectDiagnostics(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate):
    stmt='''
        SELECT
            Event.client_id AS client_id,
            Diagnosis.mkb AS mkb
        FROM
            Diagnostic
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
            LEFT JOIN Event     ON Event.id = Diagnostic.event_id
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
            LEFT JOIN rbDiseaseStage     ON rbDiseaseStage.id     = Diagnostic.stage_id
            LEFT JOIN rbHealthGroup      ON rbHealthGroup.id      = Diagnostic.healthGroup_id
            LEFT JOIN rbDispanser        ON rbDispanser.id        = Diagnostic.dispanser_id
            LEFT JOIN Client             ON Client.id             = Event.client_id
            LEFT JOIN Account_Item  ON ( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL)
                                       )
        WHERE
            rbDiseaseCharacter.code IN ('1', '2') AND
            %s
        GROUP BY
            Event.client_id, Diagnosis.mkb
    '''
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    cond = []
    cond.append(db.joinOr([db.joinAnd([tableEvent['execDate'].isNotNull(), tableEvent['execDate'].ge(begDate), tableEvent['execDate'].le(endDate)]),
                db.joinAnd([tableEvent['execDate'].isNull(), tableEvent['setDate'].isNotNull(), tableEvent['setDate'].ge(begDate), tableEvent['setDate'].le(endDate)])]))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if onlyPayedEvents:
        cond.append('isEventPayed(Event.id)')
        tableAccountItem = db.table('Account_Item')
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
    return db.query(stmt % (db.joinAnd(cond)))


class CStatReportF12_D_3_M(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
#        self.setOwnershipVisible(True)
#        self.setWorkTypeVisible(True)
        self.setTitle(u'Сведения о дополнительной диспансеризации работающих граждан, Ф.№ 12-Д-3-M',
                      u'Сведения о дополнительной диспансеризации работающих граждан')


    def getSetupDialog(self, parent):
        result = CReportF12_D_3_MSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getDefaultParams(self):
        result = CReport.getDefaultParams(self)
        prefs = getPref(QtGui.qApp.preferences.reportPrefs, self._CReportBase__preferences, {})
        result['tbl1000Col3']     = getPrefInt(prefs, 'tbl1000Col3', 0)
        result['tbl1000Col4']     = getPrefInt(prefs, 'tbl1000Col4', 0)
        result['tbl1000Col5']     = getPrefInt(prefs, 'tbl1000Col5', 0)
        result['tbl1000Col6']     = getPrefInt(prefs, 'tbl1000Col6', 0)
        result['tbl1000Col7']     = getPrefInt(prefs, 'tbl1000Col7', 0)
        result['tbl1000Col8']     = getPrefInt(prefs, 'tbl1000Col8', 0)
        result['tbl2000Col3']     = getPrefInt(prefs, 'tbl2000Col3', 0)
        #result['NotComplete']     = getPrefInt(prefs, 'NotComplete', 0)
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventTypeId = params.get('eventTypeId', None)
        onlyPermanentAttach =  params.get('onlyPermanentAttach', False)
        onlyPayedEvents = params.get('onlyPayedEvents', False)
        begPayDate = params.get('begPayDate', QDate())
        endPayDate = params.get('endPayDate', QDate())

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        self.build1000(cursor, params)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        self.build2000(cursor, begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate, params)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        self.build3000(cursor, begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate)
        return doc

    def build1000(self,  cursor, params):
        cursor.insertText(u'(1000)')
        cursor.insertBlock()
        tableColumns = [
            ('5%', [u'',
                     '',
                     '',
                     '1'], CReportBase.AlignLeft),
            ('5%',  [u'№ строки',
                     '',
                     '',
                     '2'], CReportBase.AlignCenter),
            ('10%',  [u'Всего',
                     '',
                     '',
                     '3'], CReportBase.AlignRight),
            ('10%',  [u'из них',
                     u'в полном объеме собственными силами',
                     '',
                     '4'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'на договорной основе в связи с отсутствием',
                     u' необходимого диагностического оборудования ',
                     '5'], CReportBase.AlignRight),
            ('10%',  [u'',
                     '',
                     u'необходимых специалистов',
                     '6'], CReportBase.AlignRight),
            ('10%',  ['',
                     '',
                     u'необходимых специалистов и диагностического оборудования ',
                     '7'], CReportBase.AlignRight),
            ('10%',  [u'Число организаций, прикрепленных к учреждениям здравоохранения для прохождения дополнительной диспансеризации ',
                     '',
                     u'',
                     '8'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 1, 3)
        table.mergeCells(0, 7, 3, 1)
        i = table.addRow()

        table.setText(i, 0, u'Всего')
        table.setText(i, 1, '01')
        table.setText(i, 2, forceString(params.get('tbl1000Col3', u'-')))
        table.setText(i, 3, forceString(params.get('tbl1000Col4', u'-')))
        table.setText(i, 4, forceString(params.get('tbl1000Col5', u'-')))
        table.setText(i, 5, forceString(params.get('tbl1000Col6', u'-')))
        table.setText(i, 6, forceString(params.get('tbl1000Col7', u'-')))
        table.setText(i, 7, forceString(params.get('tbl1000Col8', u'-')))
        return {}


    def build2000(self, cursor, begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate, params):
        query = countByGroups(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate)
        totalDone = 0
        totalContinued = 0
        totalByGroup = [0]*5
        while query.next():
            record = query.record()
            done = forceBool(record.value('done'))
            group = forceInt(record.value('group'))
            cnt = forceInt(record.value('cnt'))
            if done:
                totalDone += cnt
                if 0<group<=5:
                    totalByGroup[group-1] += cnt
            else:
                totalContinued += cnt

        # now text
        cursor.insertText(u'(2000)')
        cursor.insertBlock()
        tableColumns = [
            ('5%', [u'',
                     '',
                     '1'], CReportBase.AlignLeft),
            ('5%',  [u'№ строки',
                     '',
                     '2'], CReportBase.AlignCenter),
            ('10%',  [u'Число граждан',
                     u'подлежащих дополнительной диспансеризации',
                     '3'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'прошедших дополнительную диспансеризацию за отчетный период (законченный случай)',
                     '4'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'проходящих дополнительную диспансеризацию в отчетном периоде (незаконченный случай)',
                     '5'], CReportBase.AlignRight),
            ('10%',  [u'Распределение граждан, прошедших дополнительную диспансеризацию, по группам состояния здоровья',
                     u'I группа - практически здоровые',
                     '6'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'II группа - риск развития заболеваний',
                     '7'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'III группа - нуждаются в дополнительном обследовании, лечении в амбулаторно- поликлинических условиях',
                     '8'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'IV группа - нуждаются в дополнительном обследовании, лечении в стационарах',
                     '9'], CReportBase.AlignRight),
            ('10%',  ['',
                     u'V группа - нуждаются в высокотехнологичной медицинской помощи (ВМП)',
                     '10'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 1, 5)
        i = table.addRow()

        table.setText(i, 0, u'Всего')
        table.setText(i, 1, '01')
        table.setText(i, 2, forceString(params.get('tbl2000Col3', u'-')))
        table.setText(i, 3, totalDone)
        table.setText(i, 4, totalContinued)
        for j in xrange(len(totalByGroup)):
            table.setText(i, 5+j, totalByGroup[j])
        return (totalDone, totalContinued, totalByGroup)


    def build3000(self, cursor, begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate):
        mapRows = createMapCodeToRowIdx( [row[2] for row in Rows] )
        reportRowSize = 1
        reportData = [ [0] * reportRowSize for row in Rows ]
        query = selectDiagnostics(begDate, endDate, eventTypeId, onlyPermanentAttach, onlyPayedEvents, begPayDate, endPayDate)

        while query.next():
            record = query.record()
#            clientId = forceInt(record.value('client_id'))
            mkb      = normalizeMKB(forceString(record.value('mkb')))

            diagRows = mapRows.get(mkb, [])
            for row in diagRows:
                reportData[row][0] += 1

        # now text
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Результаты дополнительной диспансеризации работающих граждан')
        cursor.insertBlock()
        cursor.insertText(u'(3000)')
        cursor.insertBlock()

        tableColumns = [
            ('50%', [u'Заболевания и отклонения от нормы, выявленные при клинических и лабораторных исследованиях',  '1'], CReportBase.AlignLeft),
            ('5%',  [u'№ строки',      u'2'], CReportBase.AlignCenter),
            ('5%',  [u'Код по МКБ-10', u'3'], CReportBase.AlignCenter),
            ('30%', [u'Число заболеваний, впервые выявленных у граждан во время дополнительной диспансеризации', u'4'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)

        result = {}
        for iRow, row in enumerate(Rows):
            i = table.addRow()
            for j in xrange(3):
                table.setText(i, j, row[j])
            for j in xrange(reportRowSize):
                table.setText(i, 3+j, reportData[iRow][j])
            result[row[2]] = reportData[iRow][0]
        return result


class CReportF12_D_3_MSetupDialog(CDialogBase, Ui_ReportF12_D_3_MSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.setTitle(u'Ф12-Д-3-М')

    def preSetupUi(self):
        pass

    def postSetupUi(self):
        self.cmbEventType.setTable('EventType', True)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.chkOnlyPermanentAttach.setChecked(params.get('onlyPermanentAttach', False))
        self.chkOnlyPayedEvents.setChecked(params.get('onlyPayedEvents', False))
        self.sbCol3.setValue(forceInt(params.get('tbl1000Col3', 0)))
        self.sbCol4.setValue(forceInt(params.get('tbl1000Col4', 0)))
        self.sbCol5.setValue(forceInt(params.get('tbl1000Col5', 0)))
        self.sbCol6.setValue(forceInt(params.get('tbl1000Col6', 0)))
        self.sbCol7.setValue(forceInt(params.get('tbl1000Col7', 0)))
        self.sbCol8.setValue(forceInt(params.get('tbl1000Col8', 0)))
        self.sbTable2000Col3.setValue(forceInt(params.get('tbl2000Col3', 0)))
        #self.sbNotComplete.setValue(forceInt(params.get('NotComplete', 0)))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['eventTypeId'] = self.cmbEventType.value()
        result['onlyPermanentAttach'] = self.chkOnlyPermanentAttach.isChecked()
        result['onlyPayedEvents'] = self.chkOnlyPayedEvents.isChecked()
        result['tbl1000Col3'] = self.sbCol3.value()
        result['tbl1000Col4'] = self.sbCol4.value()
        result['tbl1000Col5'] = self.sbCol5.value()
        result['tbl1000Col6'] = self.sbCol6.value()
        result['tbl1000Col7'] = self.sbCol7.value()
        result['tbl1000Col8'] = self.sbCol8.value()
        result['tbl2000Col3'] = self.sbTable2000Col3.value()
        #result['NotComplete'] = self.sbNotComplete.value()
        return result

class CMyXmlStreamWriter(QXmlStreamWriter):
    def __init__(self,  parent):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self.nameSpace = u'http://schemas.microsoft.com/office/infopath/2003/myXSD/2008-07-16T06:56:43'

    def writeTextElement(self, elementName, val, len=None):
        if val is None:
            text = ''
        elif not isinstance(val, basestring):
            text = unicode(val)
        else:
            text = val
        if len:
            text = val[:len]
        QXmlStreamWriter.writeTextElement(self, self.nameSpace, elementName, text)


    def formatDate(self, date):
        return forceDate(date).toString('dd.MM.yyyy') if date else ''


    def writeStartElement(self, str):
        return QXmlStreamWriter.writeStartElement(self, self.nameSpace, str)

    def writeAttribute(self, attrib,  val):
        return QXmlStreamWriter.writeAttribute(self, self.nameSpace, attrib,  val)

    def writeFile(self, device, params, t2000, t3000):
        try:
            self.setDevice(device)
            self.writeStartDocument()
            self.writeProcessingInstruction('mso-infoPathSolution',
                'name="urn:schemas-microsoft-com:office:infopath:S7e2m---4n0l--12-D-3-L:-myXSD-2008-07-16T06-56-43" ' \
                'solutionVersion="1.0.0.375" productVersion="12.0.0.0" PIVersion="1.0.0.0" ' \
                'href="http://portal.zdrav/dd/DocLib/Forms/template.xsn"')
            self.writeProcessingInstruction('mso-application', 'progid="InfoPath.Document"' \
                ' versionProgid="InfoPath.Document.2"')
            self.writeNamespace('http://www.w3.org/2001/XMLSchema-instance',  'xsi')
            self.writeNamespace('http://schemas.microsoft.com/office/infopath/2003/dataFormSolution' , 'dfs')
            self.writeNamespace('http://tempuri.org/' ,'tns')
            self.writeNamespace('http://schemas.microsoft.com/office/infopath/2003/changeTracking' , '_xdns0')
            self.writeNamespace('http://schemas.xmlsoap.org/soap/envelope/' ,  'soap')
            self.writeNamespace('urn:schemas-microsoft-com:xml-diffgram-v1' ,  'diffgr')
            self.writeNamespace('urn:schemas-microsoft-com:xml-msdata' ,  'msdata')
            self.writeNamespace('http://schemas.xmlsoap.org/wsdl/http/' , 'http')
            self.writeNamespace('http://schemas.xmlsoap.org/wsdl/soap12/' , 'soap12')
            self.writeNamespace('http://schemas.xmlsoap.org/wsdl/mime/' , 'mime')
            self.writeNamespace('http://schemas.xmlsoap.org/soap/encoding/' , 'soapenc')
            self.writeNamespace('http://microsoft.com/wsdl/mime/textMatching/' , 'tm')
            self.writeNamespace('http://schemas.xmlsoap.org/wsdl/soap/' , 'ns1')
            self.writeNamespace('http://schemas.xmlsoap.org/wsdl/' , 'wsdl')
            self.writeNamespace(self.nameSpace,'my')
            self.writeNamespace('http://schemas.microsoft.com/office/infopath/2003', 'xd')
#            self.writeNamespace('uuid:BDC6E3F0-6DA3-11d1-A2A3-00AA00C14882' ,  's')
#            self.writeNamespace('uuid:C2F41010-65B3-11d1-A29F-00AA00C14882' ,  'dt')
#            self.writeNamespace('urn:schemas-microsoft-com:rowset' ,  'rs')
#            self.writeNamespace('#RowsetSchema' , 'z')
            self.writeStartElement(u'form')
            self.writeAttribute(u'name', u'12-Д-М-3')
            self.writeAttribute(u'project', 'DD')
            self.writeAttribute(u'version', '4')
            QXmlStreamWriter.writeAttribute(self, u'xml:lang', 'en-US')

            miacCode = forceString(QtGui.qApp.db.translate('Organisation',
                'id', QtGui.qApp.currentOrgId(), 'miacCode'))

            if miacCode == '':
                QtGui.QMessageBox.warning(self.parent,
                    u'Экспорт 12-Д-3-М в XML',
                    u'Отсутствует код МИАЦ для вашего ЛПУ.\n'
                    u'Необходимо установить код в:\n'
                    u'"Справочники.Организации.Организаци".',
                    QtGui.QMessageBox.Close)

            email = forceString(QtGui.qApp.preferences.appPrefs.get('mailAddress', ''))

            if email == '':
                QtGui.QMessageBox.warning(self.parent,
                    u'Экспорт 12-Д-3-М в XML',
                    u'Отсутствует адрес электронной почты.\n'
                    u'Необходимо установить адрес в:\n'
                    u'"Настройки.Умолчания.e-mail".',
                    QtGui.QMessageBox.Close)

            countDone, countContinued, countByGroup = t2000

            self.writeStartElement(u'LPU')
            self.writeAttribute('lpu_id',  miacCode)
            self.writeAttribute('email',  email)
            self.writeEndElement() # LPU
            self.writeStartElement('data')
            self.writeAttribute('period', forceString(params.get('endDate', QDate()).month()))

            self.writeStartElement('DD1000')
            self.writeTextElement('Complete', forceString(params.get('tbl1000Col4', 0)))
            #self.writeTextElement('NotComplete', forceString(params.get('NotComplete', 0)))
            self.writeStartElement('ORDER_DD')
            self.writeTextElement('NoEquipment', forceString(params.get('tbl1000Col5', 0)))
            self.writeTextElement('NoExpert', forceString(params.get('tbl1000Col6', 0)))
            self.writeTextElement('NoEqNEx', forceString(params.get('tbl1000Col7', 0)))
            self.writeEndElement() # ORDER_DD
            self.writeTextElement('AttachedOrgs', forceString(params.get('tbl1000Col3', 0)))
            self.writeTextElement('Summary', forceString(params.get('tbl1000Col8', 0)))
            self.writeEndElement() # DD1000

            self.writeStartElement('DD2000')
            self.writeStartElement('citizen')
            self.writeTextElement('observable', forceString(params.get('tbl2000Col3', 0)))
            self.writeTextElement('observated_complete', forceString(countDone))
            self.writeTextElement('observated_incomplete', forceString(countContinued))
            self.writeEndElement() # citizen
            self.writeStartElement('groups')
            self.writeTextElement('healthy', forceString(countByGroup[0]))
            self.writeTextElement('risk_II', forceString(countByGroup[1]))
            self.writeTextElement('risk_III', forceString(countByGroup[2]))
            self.writeTextElement('risk_VI', forceString(countByGroup[3]))
            self.writeTextElement('risk_V', forceString(countByGroup[4]))
            self.writeEndElement() # groups
            self.writeEndElement() # DD2000

            self.writeStartElement('DD3000')
            self.writeTextElement('A15-A19', forceString(t3000['A15-A19']))
            self.writeStartElement('malignant')
            self.writeTextElement('C15-C26', forceString(t3000['C15-C26']))
            self.writeTextElement('C33-C34', forceString(t3000['C33-C34']))
            self.writeTextElement('C43-C44', forceString(t3000['C43-C44']))
            self.writeTextElement('C50', forceString(t3000['C50']))
            self.writeTextElement('C50-C58', forceString(t3000['C50-C58']))
            self.writeTextElement('C61', forceString(t3000['C61']))
            self.writeTextElement('C81', forceString(t3000['C81-C96']))
            self.writeTextElement('D50-D64', forceString(t3000['D50-D64']))
            self.writeTextElement('E10-E14', forceString(t3000['E10-E14']))
            self.writeTextElement('E66', forceString(t3000['E66']))
            self.writeTextElement('E78', forceString(t3000['E78']))
            self.writeTextElement('I10-I15', forceString(t3000['I10-I15']))
            self.writeTextElement('I20-I25', forceString(t3000['I20-I25']))
            self.writeTextElement('R73', forceString(t3000['R73']))
            self.writeTextElement('R91', forceString(t3000['R91']))
            self.writeTextElement('R92', forceString(t3000['R92']))
            self.writeTextElement('R94.3', forceString(t3000['R94.3']))
            self.writeEndElement() # malignant
            self.writeEndElement() # DD3000

            self.writeEndElement() # data
            self.writeEndElement() # form
            self.writeEndDocument()

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', unicode(e), QtGui.QMessageBox.Close)
            return False

        return True
