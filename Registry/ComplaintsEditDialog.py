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
from PyQt4.QtCore import Qt, QVariant, pyqtSignature

from library.DialogBase import CDialogBase
from library.TreeModel  import CDBTreeItem, CDBTreeModel
from library.Utils      import forceRef, forceString

from Ui_ComplaintsEditDialog import Ui_ComplaintsEditDialog



class CComplaintsEditDialog(CDialogBase, Ui_ComplaintsEditDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('Complains', CComplaintsModel(self))
        self.setupUi(self)
        self.setModels(self.treeTypicalComplaints, self.modelComplains,  self.selectionModelComplains)
        self.treeTypicalComplaints.expandAll()


    def disableCancel(self):
        button = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        if button:
            button.setEnabled(False)


    def setComplaints(self,text):
        self.edtComplaints.setPlainText(text)


    def getComplaints(self):
        return unicode(self.edtComplaints.toPlainText())


    @pyqtSignature('QModelIndex')
    def on_treeTypicalComplaints_doubleClicked(self, index):
        parts = []
        item = index.internalPointer()
        while item and item.id():
            parts.append(unicode(item.name()))
            item = item.parent()
        parts.reverse()
        text = ': '.join(parts)
        cursor = self.edtComplaints.textCursor()

        if cursor.hasSelection():
            pos = cursor.selectionStart()
            cursor.removeSelectedText()
            cursor.setPosition(pos)
        elif not cursor.atBlockStart():
            cursor.movePosition(QtGui.QTextCursor.EndOfWord)
            cursor.insertText(', ')
        cursor.insertText(text)



class CComplaintsModel(CDBTreeModel):
    def __init__(self, parent):
        CDBTreeModel.__init__(self, parent, 'rbComplain', 'id', 'group_id', 'name', 'code')
        self.setRootItemVisible(False)


    def loadChildrenItems(self, group):
        result = []
        db = QtGui.qApp.db
        table = db.table(self.tableName)
        cond = [table[self.groupColName].eq(group._id),
                table['deleted'].eq(0)]
        for record in db.getRecordList(table, [self.idColName, self.nameColName], cond, self.order):
            id   = forceRef(record.value(0))
            name = forceString(record.value(1))
            result.append(CDBTreeItem(group, name, id, self))
        return result


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if section == 0 and orientation == Qt.Horizontal and role==Qt.DisplayRole:
            return QVariant(u'Типичные жалобы')
        else:
            return QVariant()
