# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import *

from library.Utils      import *
from library.database   import *
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Ui_AttachmentList import Ui_AttachmentListDialog

def getQuery(orgStructure_id):
    stmt = u"""
        select
          rbPolicyKind.name as policyType,
          soc_attachments.policySerial,
          soc_attachments.policyNumber,
          soc_attachments.lastName,
          soc_attachments.firstName,
          soc_attachments.patrName,
          upper(soc_attachments.sex) as sex,
          soc_attachments.birthDate,
          soc_attachments.attach_area,
          soc_attachments.attach_date,
          (SELECT OrgStructure_mo.name FROM OrgStructure as OrgStructure_mo WHERE OrgStructure_mo.bookkeeperCode = soc_attachments.attach_mo AND OrgStructure_mo.deleted = 0 LIMIT 1) as attach_mo
        from soc_attachments
            %(org_join)s
            left join rbPolicyKind on rbPolicyKind.regionalCode = soc_attachments.policyType
        where soc_attachments.serviceMethod = 1

        order by lastName, firstName
        """
    if orgStructure_id:
        query = QtGui.qApp.db.query("select areaType from OrgStructure where id = %d" % orgStructure_id)
        query.first()
        areaType = query.value(0).toInt()[0]
        if areaType == 0:
            org_join = u"""
                inner join (select OrgStructure.id, OrgStructure.bookkeeperCode
                            from OrgStructure
                              left join OrgStructure as Parent1 on Parent1.id = OrgStructure.parent_id
                              left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
                              left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
                              left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
                              left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
                            where %d in (OrgStructure.id, Parent1.id, Parent2.id, Parent3.id, Parent4.id, Parent5.id) limit 1
                           ) as OrgStructure on OrgStructure.bookkeeperCode = soc_attachments.attach_mo
                """ % orgStructure_id
        else:
            org_join = u"""
                inner join (select OrgStructure.id, OrgStructure.infisInternalCode
                           from OrgStructure
                             left join OrgStructure as Parent1 on Parent1.id = OrgStructure.parent_id
                             left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
                             left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
                             left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
                             left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
                           where %d in (OrgStructure.id, Parent1.id, Parent2.id, Parent3.id, Parent4.id, Parent5.id) limit 1
                          ) as OrgStructure on OrgStructure.infisInternalCode = soc_attachments.attach_area
                """ % orgStructure_id
    else:
        org_join = ''
    stmt = stmt % {'org_join': org_join}
    return QtGui.qApp.db.query(stmt)


class CDeAttachmentListDialog(QtGui.QDialog, Ui_AttachmentListDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))

    def params(self):
        result = { 'orgStructureId': self.cmbOrgStructure.value() }
        return result


class CDeAttachmentListReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Список открепившихся граждан')

    def exec_(self):
        query = QtGui.qApp.db.query(u'select count(*) from soc_attachments')
        if query.first() and query.value(0).toInt()[0] > 0:
            CReport.exec_(self)
        else:
            QtGui.QMessageBox.warning(None,
                                      u'Внимание!',
                                      u'Проведите синхронизацию с Регистром приписанного населения',
                                      QtGui.QMessageBox.Ok)


    def getSetupDialog(self, parent):
        result = CDeAttachmentListDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, params):
        orgStructureId = params.get('orgStructureId', None)

        query = getQuery(orgStructureId)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('5%',  [u'№ п/п'], CReportBase.AlignLeft),
            ('15%', [u'ФИО пациента'], CReportBase.AlignLeft),
            ('5%',  [u'Пол'], CReportBase.AlignLeft),
            ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
            ('10%', [u'Тип полиса'], CReportBase.AlignLeft),
            ('10%', [u'Серия полиса'], CReportBase.AlignLeft),
            ('15%', [u'Номер полиса'], CReportBase.AlignLeft),
            ('15%', [u'МО'], CReportBase.AlignLeft),
            ('5%', [u'Участок'], CReportBase.AlignLeft),
            ('10%', [u'Дата открепления'], CReportBase.AlignLeft),
        ]

        table = createTable(cursor, tableColumns)

        rowNumber = 0

        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1

            table.setText(row, 0, rowNumber)
            fullName = ' '.join([forceString(record.value('lastName')),
                                 forceString(record.value('firstName')),
                                 forceString(record.value('patrName'))])
            table.setText(row, 1, fullName)
            table.setText(row, 2, forceString(record.value('sex')))
            table.setText(row, 3, '' if record.isNull('birthDate') else forceDate(record.value('birthDate')).toString('dd.MM.yyyy'))
            table.setText(row, 4, forceString(record.value('policyType')))
            table.setText(row, 5, forceString(record.value('policySerial')))
            table.setText(row, 6, forceString(record.value('policyNumber')))
            table.setText(row, 7, forceString(record.value('attach_mo')))
            table.setText(row, 8, forceString(record.value('attach_area')))
            table.setText(row, 9, '' if record.isNull('attach_date') else forceDate(record.value('attach_date')).toString('dd.MM.yyyy'))
        return doc