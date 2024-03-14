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
from PyQt4.QtCore import Qt, QVariant
from library.TreeComboBox import CTreeComboBox, CTreeComboBoxGetIdSetIdMixin
from library.TreeModel import CTreeItemWithId, CTreeModel
from library.Utils import forceInt, forceString


__all__ = ( 'CPharmGroupComboBox',
          )

class CPharmGroupTreeItem(CTreeItemWithId):
    def __init__(self, parent, id, name):
        CTreeItemWithId.__init__(self, parent, name, id)


    def loadChildren(self):
        result = []
        db = QtGui.qApp.db
        table = db.table('rls.rlsPharmGroup')
        cond = [table['group_id'].eq(self._id)]
        query = db.query(db.selectStmt(table, 'id, name', where=cond, order='name'))
        while query.next():
            record = query.record()
            id   = forceInt(record.value('id'))
            name = forceString(record.value('name'))
            result.append(CPharmGroupTreeItem(self, id, name))
        return result


class CPharmGroupRootTreeItem(CPharmGroupTreeItem):
    def __init__(self, id=None):
        CPharmGroupTreeItem.__init__(self, None, '-', id)
        self.setId(id)


    def setId(self, id=None):
        if self._id != id:
            self._id = id
            self._items = None
            if self._id:
                self._name = forceString(QtGui.qApp.db.translate('rls.rlsPharmGroup', 'id', self._id, 'name'))
            else:
                self._name = u'-'



class CPharmGroupModel(CTreeModel):
    def __init__(self, id, parent=None):
        CTreeModel.__init__(self, parent, CPharmGroupRootTreeItem(id))


    def setId(self, id=None):
        self.getRootItem().setId(id)
        self.reset()


    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return QVariant(u'АТХ')
        return QVariant()



class CPharmGroupComboBox(CTreeComboBoxGetIdSetIdMixin, CTreeComboBox):
    def __init__(self, parent):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
#        self.__searchString = ''
        self._model = CPharmGroupModel(None, self)
        self.setModel(self._model)