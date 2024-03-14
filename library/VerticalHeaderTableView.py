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
from PyQt4.QtCore import Qt, QString, QVariant, QSize

from library.TableView import CTableView


class CVHTableView(CTableView):
    titleWidth = 0

    def __init__(self, parent):
        CTableView.__init__(self, parent)
        h = self.fontMetrics().height()
        self._verticalHeader = CVerticalHeaderTableView(Qt.Vertical, self)
        self.setVerticalHeader(self._verticalHeader)
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.setWordWrap(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #self.verticalHeader().setCascadingSectionResizes(True)
        #self.verticalHeader().resizeSections(QtGui.QHeaderView.Interactive)
        self.resizeRowsToContents()


class CVerticalHeaderTableView(QtGui.QHeaderView):
    def __init__(self, orientation, parent=None):
        QtGui.QHeaderView.__init__(self, orientation, parent)

    def sectionSizeFromContents(self, logicalIndex):
        model = self.model()
        if model:
            orientation = self.orientation()
            opt = QtGui.QStyleOptionHeader()
            self.initStyleOption(opt)
            var = model.headerData(logicalIndex, orientation, Qt.FontRole)
            if var and var.isValid() and var.type() == QVariant.Font:
                fnt = var.toPyObject()
            else:
                fnt = self.font()
            opt.fontMetrics = QtGui.QFontMetrics(fnt)
            sizeText = QSize(4,4)
            opt.text = model.headerData(logicalIndex, orientation, Qt.DisplayRole).toString()
            sizeText = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeText, self)
            sizeFiller = QSize(4,4)
            opt.text = QString('x'*CVHTableView.titleWidth)
            sizeFiller = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeFiller, self)
            return QSize(max(sizeText.width(), sizeFiller.width()),
                         max(sizeText.height(), sizeFiller.height())
                        )
        else:
            return QtGui.QHeaderView.sectionSizeFromContents(self, logicalIndex)
