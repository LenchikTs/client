# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import Qt, QDate, pyqtSignature

from library.DialogBase import CDialogBase

from Registry.Ui_SimplifiedClientSearch import Ui_SimplifiedClientSearchDialog



class CSimplifiedClientSearch(CDialogBase, Ui_SimplifiedClientSearchDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.edtKey.setFocus(Qt.OtherFocusReason)


    def getParsedKey(self):
        return self.parseKey(unicode(self.edtKey.text()))


    def parseKey(self, key):
        # возвращает (ok, nameParts, date)
        ok   = True
        nameParts = []
        date = None

        alpha  = ''.join( c if not c.isdigit() else ' ' for c in key)
        alpha  = ''.join(alpha.split())
        digits = ''.join( c for c in key if c.isdigit() )

        alpha = alpha.replace('*', '%')
        if alpha.find(' ') >= 0:
            nameParts = alpha.rsplit(' ', 2)
        else:
            if len(alpha)<=3:
                nameParts = list(alpha)
            else:
                nameParts = alpha[:-2], alpha[-2:-1], alpha[-1:]
        nameParts = [ (part + '%' if part and not part.endswith('%') else part).replace('%', '...')
                      for part in nameParts
                    ]

        if len(digits) == 0:
            date = None
        elif len(digits) == 6:
            date = QDate.fromString(digits, 'ddMMyy')
            if date:
                datePlus100Years = date.addYears(100)
                if datePlus100Years<=QDate.currentDate():
                    date = datePlus100Years
            else:
                ok = False
        elif len(digits) == 8:
            date = QDate.fromString(digits, 'ddMMyyyy')
            if not date:
                ok = False
        else:
            ok = False

        return ok, nameParts, date


    @pyqtSignature('const QString &')
    def on_edtKey_textChanged(self, text):
        ok, nameParts, date = self.parseKey(unicode(text))
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(ok)
