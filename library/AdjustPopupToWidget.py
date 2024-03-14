# -*- coding: utf-8 -*-

#############################################################################
##
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


__all__ = [ 'adjustPopupToWidget',
          ]


def adjustPopupToWidget(widget, popup, resize=False, preferredWidth=None, preferredHeight=None):
    widgetRect = widget.rect()
    popupTop = popupLeft = 0
    screen = QtGui.qApp.desktop().availableGeometry(widget)    
    if resize:
        size = popup.sizeHint()
        size.setWidth(min(screen.width(), max(10, widgetRect.width(), size.width(), 0 if preferredWidth is None else preferredWidth)))
        size.setHeight(min(screen.height(), max(10, size.height(), 0 if preferredHeight is None else preferredHeight)))
        popup.resize(size)
    popupSize = popup.frameGeometry().size()
    popupWidth, popupHeight = popupSize.width(), popupSize.height() 
    below = widget.mapToGlobal(widgetRect.bottomLeft())
    above = widget.mapToGlobal(widgetRect.topLeft())
    if screen.bottom() - below.y() >= popupHeight:
        popupTop = below.y()
    elif above.y() - screen.y() >= popupHeight:
        popupTop = above.y()-popupHeight
    else:
        popupTop = max(screen.top(), screen.bottom()-popupHeight)
    if screen.right() - below.x() >= popupWidth:
        popupLeft = below.x()
    else:
        popupLeft = max(screen.left(), screen.right()-popupWidth)
    popup.move(popupLeft, popupTop)