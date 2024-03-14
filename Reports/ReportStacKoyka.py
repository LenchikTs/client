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
        SELECT 
   hbp.name AS prof, t.cnt AS cn,COUNT(c.id) AS cl
  FROM rbHospitalBedProfile hbp
  LEFT JOIN OrgStructure_HospitalBed oshb ON oshb.profile_id = hbp.id
  LEFT JOIN OrgStructure ON oshb.master_id = OrgStructure.id AND OrgStructure.name IS NOT NULL AND OrgStructure.name!='' 
  left join OrgStructure as Parent1 on Parent1.id = OrgStructure.parent_id
                    left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
                    left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
                    left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
                    left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
  LEFT JOIN ActionProperty_HospitalBed aphb ON aphb.value = oshb.id
  LEFT JOIN ActionProperty ap ON ap.id = aphb.id
  LEFT JOIN Action a ON a.id = ap.action_id AND a.status=0 AND a.deleted=0 
  LEFT JOIN ActionType at ON a.actionType_id = at.id AND at.flatCode='moving'
  LEFT JOIN Event e ON a.event_id = e.id AND e.deleted=0
  LEFT JOIN Client c ON e.client_id = c.id AND c.deleted=0
  LEFT JOIN (SELECT COUNT(*) AS cnt, oshb.profile_id  
            FROM OrgStructure os
            LEFT JOIN OrgStructure_HospitalBed oshb ON os.id = oshb.master_id 
            GROUP by oshb.profile_id) t ON t.profile_id = hbp.id 
  WHERE t.cnt IS NOT NULL  
    %(str_org)s
  GROUP BY hbp.name
  ORDER BY prof;
        """
    if orgStructure_id:
        str_org = 'and %(orgStructure_id)d in (OrgStructure.id, Parent1.id, Parent2.id, Parent3.id, Parent4.id, Parent5.id)' % {'orgStructure_id': orgStructure_id}
    else:
        str_org = ''
    smt=stmt % {'str_org': str_org}
    return QtGui.qApp.db.query(smt)



class CAttachmentListDialog(QtGui.QDialog, Ui_AttachmentListDialog):
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


class CReportStacKoyka(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Информация о загруженности коечного фонда')

    def getSetupDialog(self, parent):
        result = CAttachmentListDialog(parent)
        result.setTitle(self.title())
        return result



    def build(self, params):
        orgStructureId = params.get('orgStructureId', None)

        

        secondTitle = u'Информация о загруженности коечного фонда'
        
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(secondTitle)
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('25%',  [ u'Профиль койки'], CReportBase.AlignLeft),
            ('25%',  [ u'Кол-во коек'], CReportBase.AlignLeft),
            ('25%',  [ u'В том числе', u'занято'], CReportBase.AlignLeft),
            ('25%',  [ u'', u'свободно'], CReportBase.AlignLeft)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        query = getQuery(orgStructureId)

        while query.next():
            record = query.record()
            prof = forceString(record.value('prof'))
            cl = forceInt(record.value('cl'))
            cn = forceInt(record.value('cn'))
            row = table.addRow()
            table.setText(row, 0, prof)
            table.setText(row, 1, cn)
            table.setText(row, 2, cl)
            table.setText(row, 3, cn-cl) 
            
        return doc
