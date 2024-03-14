# -*- coding: utf-8 -*-
#############################################################################
##
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

from library.DbComboBox import CDbComboBox
from library.Utils import forceRef


class CVaccineIdentificationComboBox(CDbComboBox):
    def __init__(self, parent):
        CDbComboBox.__init__(self, parent)
        self.setNameField("CONCAT_WS(' | ', value, note)")
        self.setAddNone(True)
        self.setFilter('deleted = 0')
        self.setTable('rbVaccine_Identification')

    def setVaccineId(self, vaccineId):
        db = QtGui.qApp.db
        systemId = forceRef(db.translate('rbAccountingSystem', 'urn', 'urn:oid:1.2.643.5.1.13.13.11.1078', 'id'))
        table = db.table('rbVaccine_Identification')
        cond = [table['deleted'].eq(0),
                table['master_id'].eq(vaccineId),
                table['system_id'].eq(systemId),
                table['checkDate'].isNotNull()]
        self.setFilter(db.joinAnd(cond))


class CVaccinationProbeIdentificationComboBox(CDbComboBox):
    def __init__(self, parent):
        CDbComboBox.__init__(self, parent)
        self.setNameField("CONCAT_WS(' | ', value, note)")
        self.setAddNone(True)
        self.setFilter('deleted = 0')
        self.setTable('rbVaccinationProbe_Identification')

    def setVaccinationProbeId(self, vaccineId):
        db = QtGui.qApp.db
        systemId = forceRef(db.translate('rbAccountingSystem', 'urn', 'urn:oid:1.2.643.5.1.13.13.11.1078', 'id'))
        table = db.table('rbVaccinationProbe_Identification')
        cond = [table['deleted'].eq(0),
                table['master_id'].eq(vaccineId),
                table['system_id'].eq(systemId),
                table['checkDate'].isNotNull()]
        self.setFilter(db.joinAnd(cond))
