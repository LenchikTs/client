# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re
import shutil
import tempfile

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from library.dbfpy.dbf import *
from library.Utils     import *

from Ui_SimpleProgress import Ui_SimpleProgress


class CSnilsImportDialog(QtGui.QDialog, Ui_SimpleProgress):
    startWork = pyqtSignal()
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.startWork.connect(self.work, Qt.QueuedConnection)
        
        
    def exec_(self):
        self.startWork.emit()
        return QtGui.QDialog.exec_(self)
        
        
    def work(self):
        startedImport = False
        self.canceled = False
        self.working = True
        tempDirectory = None
        dbfRegistr = None
        dbfLgota = None
        try:
            rarFileName = forceString(self.parent().edtSnilsFileName.text())
            
            process = QProcess()
            process.start(u'rar lb "%s"' % rarFileName)
            if not process.waitForStarted():
                raise Exception(u'не удалось запустить rar: %s' % process.errorString())

            process.waitForFinished()
            rarContents = str(process.readAllStandardOutput()).split()
            
            registrFileName = None
            lgotaFileName = None
            
            for fileName in rarContents:
                if re.match(r'^R_.+\.dbf$', fileName):
                    registrFileName = fileName
                elif re.match(r'^L_.+\.dbf$', fileName):
                    lgotaFileName = fileName
                    
            if not registrFileName or not lgotaFileName:
                raise Exception('в архиве не найдены необходимые файлы')
            
            tempDirectory = tempfile.mkdtemp()
            
            process.start(u'rar x -idcd -y "%s" "%s" "%s" "%s"' % (rarFileName, registrFileName, lgotaFileName, tempDirectory))
            if not process.waitForStarted():
                raise Exception(u'не удалось распаковать архив: %s' % process.errorString())
            
            lastPercentage = 0
            self.progressInitialize(u'Распаковка архива', 100)
            
            QtGui.qApp.processEvents()
            while not process.waitForFinished(100):
                QtGui.qApp.processEvents()
                if self.canceled:
                    process.kill()
                    process.waitForFinished()
                    shutil.rmtree(tempDirectory)
                    self.working = False
                    self.reject()
                    return
                output = str(process.readAllStandardOutput())
                match = re.search(r'(\d{1,2})%', output)
                if match:
                    currentPercentage = int(match.group(1))
                    if currentPercentage > lastPercentage:
                        self.progressStep(False, currentPercentage - lastPercentage, 1)
                        lastPercentage = currentPercentage
            
            self.progressInitialize(u'Загрузка таблиц', 2)
            
            dbfRegistr = Dbf(os.path.join(tempDirectory, registrFileName), readOnly=True, encoding='cp866', enableFieldNameDups=True)
            self.progressStep()
            
            dbfLgota = Dbf(os.path.join(tempDirectory, lgotaFileName), readOnly=True, encoding='cp866', enableFieldNameDups=True)
            self.progressStep()

            QtGui.qApp.db.transaction()
            startedImport = False

            QtGui.qApp.db.query("delete from SNILS.Lgota")
            QtGui.qApp.db.query("delete from SNILS.Registr")
            
            self.progressInitialize(u'Импорт льготников', dbfRegistr.recordCount)
            countRegistr, countRegistrErrors = self.importDbf(dbfRegistr, "SNILS.Registr", self.validateRegistr)
            
            self.progressInitialize(u'Импорт документов', dbfLgota.recordCount)
            countLgota, countLgotaErrors = self.importDbf(dbfLgota, "SNILS.Lgota", self.validateLgota)
            
            countErrors = countRegistrErrors + countLgotaErrors
            if not self.canceled:
                countRegistrText = agreeNumberAndWord(countRegistr, (u'добавлен %d человек', u'добавлено %d человека', u'добавлено %d человек')) % countRegistr
                countLgotaText = agreeNumberAndWord(countLgota, (u'%d документ', u'%d документа', u'%d документов')) % countLgota
                countErrorsText = agreeNumberAndWord(countErrors, (u'%d ошибка', u'%d ошибки', u'%d ошибок')) % countErrors
                self.progressDone(u'Импорт завершен')
                self.logInfo(u'Импорт завершен: %s и %s, %s' % (countRegistrText, countLgotaText, countErrorsText))
                
                QtGui.qApp.db.commit()
                self.working = False
                self.btnCancel.setText(u'Закрыть')
            else:
                QtGui.qApp.db.rollback()
                self.working = False
                self.reject()
        except Exception as e:
            self.logError(unicode(e) or repr(e))
            if startedImport:
                QtGui.qApp.db.rollback()
            self.working = False
            self.btnCancel.setText(u'Закрыть')
        if dbfRegistr and not dbfRegistr.closed:
            dbfRegistr.close()
        if dbfLgota and not dbfLgota.closed:
            dbfLgota.close()
        if tempDirectory:
            shutil.rmtree(tempDirectory)
            
            
    def progressInitialize(self, caption, maxCount = 1):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(maxCount)
        self.prbProgress.setValue(0)
        self.lblElapsed.setVisible(True)
        self.lblElapsed.setText(u'Текущая операция: ??? зап/с, окончание в ??:??:??')
        self.time = QTime()
        self.time.start()
        self.totalTime = QTime()
        self.totalTime.start()
        self.startPos = 0
        self.oldSpeed = 0
        
        
    def progressStep(self, showSpeed = False, stepBy = 1, minimumDifference = 1):
        self.prbProgress.setValue(self.prbProgress.value() + stepBy)
                
        elapsed = self.time.elapsed()
        difference = self.prbProgress.value() - self.startPos
        if elapsed != 0 and (difference >= minimumDifference):
            self.startPos = self.prbProgress.value()
            self.oldSpeed = difference * 1000 / elapsed
            newSpeed = (self.oldSpeed + difference * 1000 / elapsed) / 2
            if newSpeed != 0:
                totalElapsed = self.totalTime.elapsed()
                partRemaining = float(self.prbProgress.maximum()) / self.prbProgress.value() - 1
                
                finishTime = QTime.currentTime().addSecs(totalElapsed * partRemaining / 1000)
                if showSpeed:
                    self.lblElapsed.setText(u'Текущая операция: %01.f зап/с, окончание в %s' % (newSpeed, finishTime.toString('hh:mm:ss')))
                else:
                    self.lblElapsed.setText(u'Текущая операция: окончание в %s' % finishTime.toString('hh:mm:ss'))
                self.time.restart()
                
        
    def progressDone(self, caption):
        self.lblProgress.setText(caption)
        self.prbProgress.setMaximum(1)
        self.prbProgress.setValue(1)
        self.lblElapsed.setVisible(False)
        
    def logInfo(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(text)
        else:
            for str in text:
                self.txtLog.append(str)
        self.txtLog.append('')
        
        
    def logError(self, text):
        if isinstance(text, basestring):
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text)
        else:
            self.txtLog.append(u'<b><font color=red>Ошибка:</font></b> %s' % text[0])
            for str in text[1:]:
                self.txtLog.append(str)
        self.txtLog.append('')


    def importDbf(self, dbf, tableName, validator):
        countAdded = 0
        countErrors = 0
        
        for dbfRecord in dbf:
            QtGui.qApp.processEvents()
            if self.canceled:
                return countAdded, countErrors
            error = validator(dbfRecord)
            if error:
                countErrors += 1
                self.logError(error)
            else:
                self.importDbfRecord(dbfRecord, tableName)
                countAdded += 1
            self.progressStep(True, 1, 100)
        return countAdded, countErrors

        
    def importDbfRecord(self, dbfRecord, tableName):
        table = QtGui.qApp.db.table(tableName)
        record = table.newRecord()
        for fieldName, value in dbfRecord.asDict().iteritems():
            record.setValue(fieldName, toVariant(value))
        QtGui.qApp.db.insertRecord(table, record)
        
        
    def validateRegistr(self, dbfRecord):
        ss = dbfRecord['SS']
        
        if not ss:
            fam = forceString(dbfRecord['FAM'])
            im = forceString(dbfRecord['IM'])
            ot = forceString(dbfRecord['OT'])
            
            return u'Не удалось добавить: %s %s %s; пустое поле "SS"' % (fam, im, ot)
        else:
            return None
        
    def validateLgota(self, dbfRecord):
        ss = dbfRecord['SS']
        
        if not ss:
            name = forceString(dbfRecord['NAME_DL'])
            sn = forceString(dbfRecord['SN_DL'])
            
            return u'Не удалось добавить документ: %s %s; пустое поле "SS"' % (name, sn)
        else:
            return None


    @pyqtSignature("")
    def on_btnCancel_clicked(self):
        if self.working:
            self.canceled = True
        else:
            self.accept()
            
