#!/usr/bin/env python
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

import os.path
import stat
import mimetypes
import smtplib
import hashlib
import email.utils

from smtplib                import ( SMTPAuthenticationError,
                                     SMTPConnectError,
                                     SMTPDataError,
                                     SMTPException,
                                     SMTPHeloError,
                                     SMTPRecipientsRefused,
                                     SMTPResponseException,
                                     SMTPSenderRefused,
                                     SMTPServerDisconnected,
                                   )

from email.header           import Header
from email.mime.multipart   import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.audio       import MIMEAudio
from email.mime.image       import MIMEImage
from email.mime.text        import MIMEText

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QAbstractTableModel, QModelIndex, QVariant

from library.DialogBase import CDialogBase
from library.Utils import anyToUnicode, forceBool, forceInt, forceString, forceStringEx, toVariant

from Ui_SendMailDialog import Ui_SendMailDialog


DefaultSMTPPorts = (25, 587, 465)

def sendMail(parent, recipient, subject, text, attach=[]):
    dialog = CSendMailDialog(parent)
    dialog.edtRecipient.setText(recipient)
    dialog.edtSubject.setText(subject)
    dialog.edtText.setText(text)
    dialog.setAttach(attach)
    dialog.exec_()


def getMailPrefs(params={}):
    global DefaultSMTPPorts

    appPrefs = QtGui.qApp.preferences.appPrefs
    result = {}
    result['SMTPServer']     = forceString(params.get('SMTPServer', appPrefs.get('SMTPServer', 'localhost')))
    encryption = forceInt(params.get('SMTPEncryption', appPrefs.get('SMTPEncryption', 0)))
    result['SMTPEncryption'] = encryption
    port = forceInt(params.get('SMTPPort', appPrefs.get('SMTPPort', 0)))
    result['SMTPPort'] = port if port>0 else DefaultSMTPPorts[encryption]
    result['mailAddress'] = forceString(params.get('mailAddress', appPrefs.get('mailAddress', '')))
    result['SMTPAuthentification'] = forceBool(params.get('SMTPAuthentification', appPrefs.get('SMTPAuthentification', False)))
    result['SMTPLogin'] = forceString(params.get('SMTPLogin', appPrefs.get('SMTPLogin', '')))
    result['SMTPPassword'] = forceString(params.get('SMTPPassword', appPrefs.get('SMTPPassword', '')))
    return result


def prepareMail(sender, recipient, subject, text, attach):
        encoding = 'utf-8'
        encodingErrors = 'replace'
        encodedText = text.encode(encoding, encodingErrors)
        message = MIMEMultipart()
        message['From']    = Header(sender, encoding, errors=encodingErrors)
        message['To']      = Header(recipient, encoding, errors=encodingErrors)
        message['Subject'] = Header(subject.encode(encoding, encodingErrors), encoding, errors=encodingErrors)
        message['Date']    = email.utils.formatdate(localtime=True)
        checksum = hashlib.md5()
        checksum.update(email.utils.formatdate(localtime=True))
        checksum.update(encodedText)
        message['Message-ID'] = checksum.hexdigest()

        message.add_header(u'X-Mailer', u'SAMSON v.2.5')
        message.preamble = 'This is a multi-part message in MIME format. '      \
                           'If you see this message, your mail client is not '  \
                           'capable of displaying the attachments.'
        message.epilogue = ''
        textPart = MIMEText(encodedText,
                            _subtype='html',
                            _charset=encoding)
        message.attach(textPart)

        for fileData in attach:
            if isinstance(fileData, tuple):
                fileStream, fileName = fileData
                attachment = MIMEApplication(fileStream.getvalue(), 'octet-stream', name=fileName)
                fileStream.close()
                attachment.add_header('Content-Disposition', 'attachment', filename = fileName)
                message.attach(attachment)
                continue
            fileName = fileData
            attachFileName = os.path.basename(fileName)
            attachFileName = str(Header(attachFileName.encode(encoding, encodingErrors), encoding, errors=encodingErrors))
            ctype, encoding = mimetypes.guess_type(fileName)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                attachment = MIMEText(open(fileName, 'rb').read(), _subtype = subtype)
            elif maintype == 'image':
                attachment = MIMEImage(open(fileName, 'rb').read(), _subtype = subtype)
            elif maintype == 'audio':
                attachment = MIMEAudio(open(fileName, 'rb').read(), _subtype = subtype)
            else:
                attachment = MIMEApplication(open(fileName, 'rb').read(), 'octet-stream', name=attachFileName)
#            if encoding:
#                attachment.add_header('Content-Encoding', encoding)
            attachment.add_header('Content-Disposition', 'attachment', filename = attachFileName)
            message.attach(attachment)
        return message


def sendMailInt(recipient, subject, text, attach, params={}):
    try:
        prefs = getMailPrefs(params)
        sender = prefs['mailAddress']
        message = prepareMail(sender, recipient, subject, text, attach)
        serverClass = smtplib.SMTP_SSL if prefs['SMTPEncryption'] == 2 else smtplib.SMTP
        server = serverClass(prefs['SMTPServer'], prefs['SMTPPort'], timeout=30)
        ###server.set_debuglevel(1)
        if prefs['SMTPEncryption'] == 1:
            server.starttls()
        server.ehlo_or_helo_if_needed()
        if prefs['SMTPAuthentification'] and server.has_extn('auth'):
            server.login(prefs['SMTPLogin'], prefs['SMTPPassword'].encode('utf8'))
        server.sendmail(sender, recipient, message.as_string())
        server.quit()
        return (True, '')
    except SMTPSenderRefused, e:
        errorMessage = u'Сервер отверг адрес отправителя\n%s' % unicode(e)
    except SMTPAuthenticationError, e:
        errorMessage = u'Сервер отверг соединение с указанным именем и паролём\n%s' % unicode(e)
    except SMTPDataError, e:
        errorMessage = u'Сервер отверг передаваемые данные\n%s' % unicode(e)
    except SMTPConnectError, e:
        errorMessage = u'Ошибка установления соединения с сервером\n%s' % unicode(e)
    except SMTPHeloError, e:
        errorMessage = u'Сервер отверг сообщение "HELO"\n%s' % unicode(e)
    except SMTPResponseException, e:
        errorMessage = u'Сервер сообщил об ошибке\n%s' % unicode(e)
    except SMTPRecipientsRefused, e:
        errorMessage = u'Сервер отверг получателей\n%s' % unicode(e)
    except SMTPServerDisconnected, e:
        errorMessage = u'Неожиданный разрыв соединения с сервером\n%s' % unicode(e)
    except SMTPException, e:
        errorMessage = u'Ошибка взаимодействия с сервером\n%s' % unicode(e)
    except IOError, e:
        if hasattr(e, 'filename'):
            errorMessage = u'Ошибка ввода/вывода %s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
        else:
            errorMessage = u'Ошибка ввода/вывода\n[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
    except Exception, e:
        errorMessage = u'Ошибка\n%s' % unicode(e)
    QtGui.qApp.logCurrentException()
    return (False, errorMessage)


class CSendMailDialog(CDialogBase, Ui_SendMailDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)

        self.mnuAttach = QtGui.QMenu(self)
        self.mnuAttach.setObjectName('mnuAttach')
        self.actAddAttach = QtGui.QAction(u'Добавить вложение', self)
        self.actAddAttach.setObjectName('actAddAttach')
        self.actDelAttach = QtGui.QAction(u'Удалить вложение', self)
        self.actDelAttach.setObjectName('actDelAttach')
        self.mnuAttach.addAction(self.actAddAttach)
        self.mnuAttach.addAction(self.actDelAttach)
        self.modelAttach = CAttachModel(self)
        self.btnSaveAsFile = QtGui.QPushButton(u'Сохранить как файл', self)
        self.btnSaveAsFile.setObjectName('btnSaveAsFile')
        self.setupUi(self)
        self.buttonBox.addButton(self.btnSaveAsFile, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(u'Отправить')
        self.tblAttach.setModel(self.modelAttach)
        self.tblAttach.setPopupMenu(self.mnuAttach)


    def setAttach(self, attach):
        self.modelAttach.setFiles(attach)


    def saveData(self):
        recipient = forceStringEx(self.edtRecipient.text())
        subject   = forceStringEx(self.edtSubject.text())
        text      = forceStringEx(self.edtText.document().toHtml('utf-8'))
        attach    = self.modelAttach.files()
        success, errorMessage = QtGui.qApp.callWithWaitCursor(self, sendMailInt, recipient, subject, text, attach)
        if success:
            QtGui.QMessageBox.information( self,
                                          u'Готово',
                                          u'Сообщение отправлено',
                                          QtGui.QMessageBox.Close)
#            CDialogBase.accept(self)
            return True
        QtGui.QMessageBox.critical( self,
                                    u'Ошибка',
                                    errorMessage,
                                    QtGui.QMessageBox.Close)
        return False


    def saveAsFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Выберите имя файла', QtGui.qApp.getSaveDir(), u'Почтовое сообщение (*.eml)')
        if fileName:
            QtGui.qApp.setSaveDir(fileName)
            recipient = forceStringEx(self.edtRecipient.text())
            subject   = forceStringEx(self.edtSubject.text())
            text      = forceStringEx(self.edtText.document().toHtml('utf-8'))
            attach    = self.modelAttach.files()
            message = prepareMail('', recipient, subject, text, attach)
            open(fileName, 'w+b').write(message.as_string())


    @pyqtSignature('')
    def on_mnuAttach_aboutToShow(self):
        currentRow = self.tblAttach.currentIndex().row()
        itemPresent = currentRow>=0
        self.actDelAttach.setEnabled(itemPresent)

    @pyqtSignature('')
    def on_actAddAttach_triggered(self):
#        currentRow = self.tblAttach.currentIndex().row()
#        if currentRow>=0:
#            dir = os.path.dirname( self.modelAttach.files()[currentRow] )
#        else:
#            dir = ''

        fileNames = QtGui.QFileDialog.getOpenFileNames(
            self, u'Выберите один или несколько файлов', QtGui.qApp.getSaveDir())
        if fileNames:
            QtGui.qApp.setSaveDir(fileNames[0])
            self.modelAttach.appendFiles(fileNames)
            self.tblAttach.setCurrentIndex( self.modelAttach.index(self.modelAttach.rowCount()-1, 0))


    @pyqtSignature('')
    def on_actDelAttach_triggered(self):
        self.tblAttach.removeCurrentRow()


    @pyqtSignature('')
    def on_btnSaveAsFile_clicked(self):
        QtGui.qApp.call(self, self.saveAsFile)
#        self.saveAsFile()


class CAttachModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.__fileInfos = []


    def setFiles(self, files):
        self.__fileInfos = []
        self.appendFiles(files)


    def appendFiles(self, files):
        for fileName in files:
            strFileName = forceString(fileName)
            baseName = os.path.basename(forceString(strFileName))
            fileStat = os.stat(strFileName)
            size = fileStat[stat.ST_SIZE]
            self.__fileInfos.append( (strFileName, baseName, size) )
        self.reset()


    def files(self):
        return [fileInfo[0] for fileInfo in self.__fileInfos]

    def columnCount(self, index = None):
        return 2

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def rowCount(self, index = None):
        return len(self.__fileInfos)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            column = index.column()
            row = index.row()
            return toVariant(self.__fileInfos[row][column+1])
        return QVariant()


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return toVariant(u'Файл')
                if section == 1:
                    return toVariant(u'Размер')
        return QVariant()


    def removeRow(self, row, parent = QModelIndex()):
        if 0<=row<len(self.__fileInfos):
            self.beginRemoveRows(parent, row, row)
            del self.__fileInfos[row]
            self.endRemoveRows()
            return True
        return False
