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
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.DialogBase import CDialogBase
from library.Utils import forceRef
from Ui_SurveillanceRemovedDialog     import Ui_SurveillanceRemovedDialog


class CExceptionMixin:
    def raiseException(self, methodName):
        raise Exception(u'%s не имеет метода %s' % (str(self), methodName))


class CSurveillanceRemovedDialog(CExceptionMixin, CDialogBase, Ui_SurveillanceRemovedDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Снять с ДН в МО')
        self.cmbDispanser.setTable('rbDispanser', False, filter=u'''rbDispanser.name LIKE '%снят%' ''')
        self.cmbRemoveReason.setTable('rbSurveillanceRemoveReason', False)


    def saveData(self):
        result = True
        result = result and (self.cmbDispanser.value() or self.checkInputMessage(u'Диспансерное наблюдение', False, self.cmbDispanser))
        result = result and (self.edtRemoveReasonDate.date() or self.checkInputMessage(u'Дату снятия', False, self.edtRemoveReasonDate))
        result = result and (self.cmbRemoveReason.value() or self.checkInputMessage(u'Причину снятия', False, self.cmbRemoveReason))
        return result


    def getRemoveReasonDate(self):
        return self.edtRemoveReasonDate.date()


    def getDispanserId(self):
        return self.cmbDispanser.value()


    def getRemoveReasonId(self):
        return self.cmbRemoveReason.value()


    @pyqtSignature('int')
    def on_cmbDispanser_currentIndexChanged(self, index):
        removeReasonIdList = []
        dispanserId = self.cmbDispanser.value()
        removeReasonId = self.cmbRemoveReason.value()
        if dispanserId:
            db = QtGui.qApp.db
            table = db.table('rbSurveillanceRemoveReason')
            removeReasonIdList = db.getDistinctIdList(table, [table['id']], [table['dispanser_id'].eq(dispanserId)])
            if not removeReasonIdList:
                removeReasonIdList = db.getDistinctIdList(table, [table['id']], [table['dispanser_id'].isNull()])
            self.cmbRemoveReason.setTable('rbSurveillanceRemoveReason', False, filter=u'''rbSurveillanceRemoveReason.id IN (%s)'''%(u','.join(str(removeReasonId) for removeReasonId in removeReasonIdList if removeReasonId)))
            if len(removeReasonIdList) == 1:
                self.cmbRemoveReason.setValue(removeReasonIdList[0])
            elif removeReasonId in removeReasonIdList:
                self.cmbRemoveReason.setValue(removeReasonId)
            else:
                self.cmbRemoveReason.setValue(None)
        else:
            self.cmbRemoveReason.setTable('rbSurveillanceRemoveReason', False)
            self.cmbRemoveReason.setValue(removeReasonId)


    @pyqtSignature('int')
    def on_cmbRemoveReason_currentIndexChanged(self, index):
        dispanserId = None
        removeReasonId = self.cmbRemoveReason.value()
        if removeReasonId:
            db = QtGui.qApp.db
            table = db.table('rbDispanser')
            tableRR = db.table('rbSurveillanceRemoveReason')
            record = db.getRecordEx(tableRR.innerJoin(table, table['id'].eq(tableRR['dispanser_id'])), [tableRR['dispanser_id']], [tableRR['id'].eq(removeReasonId), table['name'].like(u'снят%%')])
            dispanserId = forceRef(record.value('dispanser_id')) if record else None
            if dispanserId:
                self.cmbDispanser.setValue(dispanserId)
