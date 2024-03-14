# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re
from PyQt4 import QtGui,  QtCore

try:
    import library.hunspell as hunspell
    gSpellCheckAvailable = True
except:
    gSpellCheckAvailable = False



class CSpellCheckTextEdit(QtGui.QTextEdit):

    def __init__(self,  parent):
        QtGui.QTextEdit.__init__(self,  parent)

        self.format = self.getFormatForSpellCheck()
        self.baseDictIsAvailable = False
        pathToDictionary = QtGui.qApp.getPathToDictionary()
        if gSpellCheckAvailable and QtGui.qApp.showingSpellCheckHighlight():
            try:
                self.dict = hunspell.DictWithPWL(u'ru_RU', pathToDictionary)
                self.baseDictIsAvailable = True
                self.highlighter = CSpellCheckHighlighter(self.document(),  self.format)
                self.highlighter.setDict(self.dict)
            except hunspell.ENoDictionaryFound:
                #QtGui.qApp.logCurrentException()
                self.baseDictIsAvailable = False
                pass



    def getFormatForSpellCheck(self):
        format = QtGui.QTextCharFormat()
        format.setUnderlineColor(QtGui.QColor('red'))
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        return format


#    def mousePressEvent(self, event):
#        if event.button() == QtCore.Qt.RightButton:
#            # По нажатию правой кнопки мыши курсор перемещается в позицию, где находится укзатель мыши
#            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(),
#                QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
#        QtGui.QTextEdit.mousePressEvent(self, event)


    def contextMenuEvent(self,  event):
        # По нажатию правой кнопки мыши курсор перемещается в позицию, где находится укзатель мыши
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(),
               QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QTextEdit.mousePressEvent(self, event)

        popup_menu = self.createStandardContextMenu()
        if gSpellCheckAvailable and self.baseDictIsAvailable and QtGui.qApp.showingSpellCheckHighlight():
            cursor = self.textCursor()
            startPos = cursor.position()
            #cursor.select(QtGui.QTextCursor.WordUnderCursor)
            if not cursor.hasSelection():
                # Выделить слово под курсором для последующего поиска его в словаре
                newCursor = self.selectWord(cursor)
                self.setTextCursor(newCursor)
                text = unicode(self.textCursor().selectedText())
                
                check_text = text
                if len(check_text.split()) == 1:
                    text = text.replace(" ", "")

                # Снять выделение слова, т.к. изначально слово не было выделено
                clearCursor = self.textCursor()
                clearCursor.clearSelection()
                clearCursor.setPosition(startPos)
                self.setTextCursor(clearCursor)
            else:
                text = unicode(self.textCursor().selectedText())
                check_text = text

                if len(check_text.split()) == 1:
                    text = text.replace(" ", "")

            #if gSpellCheckAvailable and QtGui.qApp.showingSpellCheckHighlight():
            # Проверяем, правильно ли написано слово, и, если нет, предлагаем варианты исправления
            try:
                if not self.dict.check(text) and ' ' not in text:
                    spellMenu = QtGui.QMenu(u'Варианты исправления слова')
                    for word in self.dict.suggest(text):
                        action = CSpellAction(word, spellMenu)
                        action.correct.connect(self.correctWord)
                        spellMenu.addAction(action)
                    recordWord = CRecordCorrectWord(text, u'Внести в словарь', spellMenu)
                    if QtGui.qApp.getPathToDictionary() is None:
                        recordWord.setDisabled(True)
                    else:
                        recordWord.setCorrect.connect(self.wrapperForAddWord)
                    spellMenu.addAction(recordWord)
                    spellMenu.insertSeparator(spellMenu.actions()[-1])
                    #  Предлагаем варианты исправления слова в том случае, если они есть
                    if len(spellMenu.actions()) != 0:
                        popup_menu.insertSeparator(popup_menu.actions()[0])
                        popup_menu.insertMenu(popup_menu.actions()[0], spellMenu)
            except UnicodeEncodeError:
                QtGui.qApp.logCurrentException()

        #popup_menu.exec_(self.text.mousePressEvent(Qt.RightButton).globalPos())
        popup_menu.exec_(event.globalPos())


    def wrapperForAddWord(self, word):
        if gSpellCheckAvailable:
            self.dict.add(unicode(word))
            self.highlighter.rehighlight()


    def selectWord(self,  cursor):
        #pattern = re.compile(ur'[a-zA-Zа-яА-Я0-9\-\']')
        pattern = re.compile(r'(?iu)[\w\-\']+')

        # Находим начало слова
        cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
        while pattern.search(unicode(cursor.selectedText())):
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.NoMove, QtGui.QTextCursor.MoveAnchor)
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
        cursor.clearSelection()
        if not cursor.atStart():
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor)
        cursorPositionStart = cursor.position()

        # Находим конец слова
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        while pattern.search(unicode(cursor.selectedText())):
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.NoMove, QtGui.QTextCursor.MoveAnchor)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        cursor.clearSelection()
        if not cursor.atEnd():
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor)
        cursorPositionEnd = cursor.position()

        # Выделяем слово от начала и до конца слова
        cursor.setPosition(cursorPositionStart,  QtGui.QTextCursor.MoveAnchor)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        while cursor.position() != cursorPositionEnd:
            if cursorPositionStart >= cursorPositionEnd:
                break
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        return cursor


    def correctWord(self, word):
        cursor = self.textCursor()
        newCursor = self.selectWord(cursor) if not cursor.hasSelection() else cursor
        self.setTextCursor(newCursor)
        self.textCursor().beginEditBlock()

        self.textCursor().removeSelectedText()
        self.textCursor().insertText(word)

        self.textCursor().endEditBlock()


class CSpellCheckHighlighter(QtGui.QSyntaxHighlighter):
    #words = r'(?iu)w\+'
    #words = r'(?iu)[\w\-\']+'
    words = r'(?iu)[\w\-\']+[^\s\-\.,!?:;()]+'

    def __init__(self, text,  format):
        super(CSpellCheckHighlighter, self).__init__(text)
        self.format = format
        self.text = text


    def setDict(self, dict):
        self.dict = dict


    def highlightBlock(self, text):
        if gSpellCheckAvailable:
            text = unicode(text)

            for word in re.finditer(self.words, text):
                if not self.dict.check(word.group()):
                    self.setFormat(word.start(), word.end() - word.start(), self.format)


class CSpellAction(QtGui.QAction):

    correct = QtCore.pyqtSignal(unicode)

    def __init__(self, *args):
        QtGui.QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))


class CRecordCorrectWord(QtGui.QAction):

    setCorrect = QtCore.pyqtSignal(unicode)

    def __init__(self, word, *args):
        QtGui.QAction.__init__(self, *args)
        self.word = word
        self.triggered.connect(lambda x: self.setCorrect.emit(self.word))
