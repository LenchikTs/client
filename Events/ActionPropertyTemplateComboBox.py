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

from library.TreeComboBox import CTreeComboBox, CTreeComboBoxGetIdSetIdMixin
from library.TreeModel import CTreeItemWithId, CTreeModel

from library.Utils import forceInt, forceString



class CActionPropertyTemplateTreeItem(CTreeItemWithId):
    def __init__(self, parent, id, name):
        CTreeItemWithId.__init__(self, parent, name, id)


    def loadChildren(self):
        result = []
        db = QtGui.qApp.db
        table = db.table('ActionPropertyTemplate')
        cond = [table['group_id'].eq(self._id)]
        query = db.query(db.selectStmt(table, 'id, name', where=cond, order='name'))
        while query.next():
            record = query.record()
            id   = forceInt(record.value('id'))
            name = forceString(record.value('name'))
            result.append(CActionPropertyTemplateTreeItem(self, id, name))
        return result



class CActionPropertyTemplateRootTreeItem(CActionPropertyTemplateTreeItem):
    def __init__(self):
        CActionPropertyTemplateTreeItem.__init__(self, None, None, u'-')



class CActionPropertyTemplateModel(CTreeModel):
    def __init__(self, parent=None):
        CTreeModel.__init__(self, parent, CActionPropertyTemplateRootTreeItem())


#    def headerData(self, section, orientation, role):
#        if role == Qt.DisplayRole:
#            return QVariant(u'Шаблоны свойств')
#        return QVariant()


class CActionPropertyTemplateComboBox(CTreeComboBoxGetIdSetIdMixin, CTreeComboBox):
    def __init__(self, parent):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self._model = CActionPropertyTemplateModel(self)
        self.setModel(self._model)
