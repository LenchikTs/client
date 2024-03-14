# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки деревьев
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.Utils import forceInt, toVariant

from Ui_TreesPage import Ui_treesPage


class CTreesPage(Ui_treesPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        treeOrgStrExpand = forceInt(props.get('treeOrgStructureExpand',  0))
        self.cmbTreeOrgStructureExpand.setCurrentIndex(treeOrgStrExpand)
        if treeOrgStrExpand == 2:
            self.edtTreeOrgStructureExpand.setVisible(True)
            self.edtTreeOrgStructureExpand.setValue(forceInt(props.get('treeOrgStructureExpandLevel')))
        else:
            self.edtTreeOrgStructureExpand.setVisible(False)

        treeActionTypeExpand = forceInt(props.get('actionTypeTreeExpand',  0))
        self.cmbActionTypeTreeExpand.setCurrentIndex(treeActionTypeExpand)
        if treeActionTypeExpand == 2:
            self.edtActionTypeTreeExpand.setVisible(True)
            self.edtActionTypeTreeExpand.setValue(forceInt(props.get('actionTypeTreeExpandLevel')))
        else:
            self.edtActionTypeTreeExpand.setVisible(False)

        treeProbesExpand = forceInt(props.get('probesTreeExpand',  0))
        self.cmbProbesTreeExpand.setCurrentIndex(treeProbesExpand)
        if treeProbesExpand == 2:
            self.edtProbesTreeExpand.setVisible(True)
            self.edtProbesTreeExpand.setValue(forceInt(props.get('probesTreeExpandLevel')))
        else:
            self.edtProbesTreeExpand.setVisible(False)

        treeActionTemplateExpand = forceInt(props.get('actionTemplateTreeExpand',  0))
        self.cmbActionTemplateTreeExpand.setCurrentIndex(treeActionTemplateExpand)
        if treeActionTemplateExpand == 2:
            self.edtActionTemplateTreeExpand.setVisible(True)
            self.edtActionTemplateTreeExpand.setValue(forceInt(props.get('actionTemplateTreeExpandLevel')))
        else:
            self.edtActionTemplateTreeExpand.setVisible(False)

        treeContractsExpand = forceInt(props.get('treeContractsExpand', 0))
        self.cmbContractsTreeExpand.setCurrentIndex(treeContractsExpand)
        if treeContractsExpand == 2:
            self.edtContractsTreeExpand.setVisible(True)
            self.edtContractsTreeExpand.setValue(forceInt(props.get('treeContractsExpandLevel')))
        else:
            self.edtContractsTreeExpand.setVisible(False)


    def getProps(self, props):
        props['treeOrgStructureExpand'] = toVariant(self.cmbTreeOrgStructureExpand.currentIndex())
        props['treeOrgStructureExpandLevel'] = toVariant(self.edtTreeOrgStructureExpand.value())
        props['actionTypeTreeExpand'] = toVariant(self.cmbActionTypeTreeExpand.currentIndex())
        props['actionTypeTreeExpandLevel'] = toVariant(self.edtActionTypeTreeExpand.value())
        props['probesTreeExpand'] = toVariant(self.cmbProbesTreeExpand.currentIndex())
        props['probesTreeExpandLevel'] = toVariant(self.edtProbesTreeExpand.value())
        props['actionTemplateTreeExpand'] = toVariant(self.cmbActionTemplateTreeExpand.currentIndex())
        props['actionTemplateTreeExpandLevel'] = toVariant(self.edtActionTemplateTreeExpand.value())
        props['treeContractsExpand'] = toVariant(self.cmbContractsTreeExpand.currentIndex())
        props['treeContractsExpandLevel'] = toVariant(self.edtContractsTreeExpand.value())


    @pyqtSignature('int')
    def on_cmbTreeOrgStructureExpand_currentIndexChanged(self, index):
        if index == 2:
            self.edtTreeOrgStructureExpand.setVisible(True)
        else:
            self.edtTreeOrgStructureExpand.setVisible(False)


    @pyqtSignature('int')
    def on_cmbActionTypeTreeExpand_currentIndexChanged(self, index):
        if index == 2:
            self.edtActionTypeTreeExpand.setVisible(True)
        else:
            self.edtActionTypeTreeExpand.setVisible(False)


    @pyqtSignature('int')
    def on_cmbProbesTreeExpand_currentIndexChanged(self, index):
        if index == 2:
            self.edtProbesTreeExpand.setVisible(True)
        else:
            self.edtProbesTreeExpand.setVisible(False)


    @pyqtSignature('int')
    def on_cmbActionTemplateTreeExpand_currentIndexChanged(self, index):
        if index == 2:
            self.edtActionTemplateTreeExpand.setVisible(True)
        else:
            self.edtActionTemplateTreeExpand.setVisible(False)

    @pyqtSignature('int')
    def on_cmbContractsTreeExpand_currentIndexChanged(self, index):
        if index == 2:
            self.edtContractsTreeExpand.setVisible(True)
        else:
            self.edtContractsTreeExpand.setVisible(False)
