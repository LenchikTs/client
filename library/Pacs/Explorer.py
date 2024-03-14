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

import contextlib
#import locale
import os.path
import random
#import shlex
import shutil
import subprocess
import urllib
import zipfile

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QDate, QDir, QObject, QThread, QUrl

from library.DialogBase import CDialogBase
from library.Utils import forceString

from RestToolbox import getRequest, postRequest
from Ui_Explorer import Ui_ExplorerDialog


class CGarbageCollector(QThread):
    __pyqtSignals__ = ('finished()',
                      )
    def __init__(self, p, destinationDir, fileList):
        QObject.__init__(self, None)
        self.p = p
        self.destinationDir = destinationDir
        self.fileList = fileList

    def run(self):
        self.p.wait()
        shutil.rmtree(self.destinationDir)
        for file in self.fileList:
            os.remove(file)
        self.emit(SIGNAL('finished()'))
        self.quit()

class CPacsExplorer(CDialogBase, Ui_ExplorerDialog):
    def __init__(self, clientId, seriesIdList = [], parent = None, showDate = None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.showDate = showDate
        self.items = []
        self.idList = seriesIdList
        address = forceString(QtGui.qApp.preferences.appPrefs.get('pacsAddress', ''))
        port = forceString(QtGui.qApp.preferences.appPrefs.get('pacsPort', None))
        self.address = '%s:%s'%(address, port) if address else None
        if showDate and type(showDate) == tuple:
            self.lblTop.setText(u'Показаны снимки на %s - %s'%(forceString(showDate[0]), forceString(showDate[1])))
        if not self.idList and clientId:
            self.idList = self.getAllSeries(clientId)
            self.lblTop.setText(u'Показаны все снимки')
        if self.idList:
            self.loadSeries(self.idList)
        for x in xrange(self.listWidget.count()):
            self.listWidget.item(x).setSelected(True)

    def getAllSeries(self, clientId):
        imageIdList = []
        if self.address:
            try:
                patientSearchData = postRequest('http://%s/tools/lookup'%self.address, clientId)
                if len(patientSearchData) and patientSearchData[0].get('Type', '') == 'Patient':
                    patientData = getRequest('http://%s/patients/%s'%(self.address, patientSearchData[0]['ID']))
                    if patientData:
                        studiesIdList = patientData["Studies"]
                        for studyId in studiesIdList:
                            studyData = getRequest('http://%s/studies/%s'%(self.address, studyId))
                            if studyData:
                                imageIdList.extend(studyData['Series'])
            except Exception:
                self.lblTop.setText(u'Отсутствует связь с сервером изображений!')
            return imageIdList

    def loadSeries(self, idList):
        self.items = []
        if self.address:
            for id in idList:
                seriesInfo = getRequest('http://%s/series/%s'%(self.address, id))
                if seriesInfo:
                    if 'SeriesDescription' in seriesInfo['MainDicomTags']:
                        name = seriesInfo['MainDicomTags']['SeriesDescription']
                    elif 'AcquisitionDeviceProcessingDescription' in seriesInfo['MainDicomTags']:
                        name = seriesInfo['MainDicomTags']['AcquisitionDeviceProcessingDescription']
                    elif 'ProtocolName' in seriesInfo['MainDicomTags']:
                        name = seriesInfo['MainDicomTags']['ProtocolName']
                    else:
                        name = u'Неизвестно'
                    studyInfo = getRequest('http://%s/studies/%s'%(self.address, seriesInfo['ParentStudy']))
                    if studyInfo:
                        if 'StudyDescription' in studyInfo['MainDicomTags']:
                            name = '%s %s'%(studyInfo['MainDicomTags']['StudyDescription'], name)
                        elif 'AcquisitionDeviceProcessingDescription' in studyInfo['MainDicomTags']:
                            name = '%s %s'%(studyInfo['MainDicomTags']['AcquisitionDeviceProcessingDescription'], name)
                    if not self.showDate:
                        if 'SeriesDate' in seriesInfo['MainDicomTags']:
                            date = QDate.fromString(seriesInfo['MainDicomTags']['SeriesDate'], 'yyyyMMdd')
                            name = '%s %s'%(forceString(date), name)
                    self.items.append(name)
                    self.listWidget.addItem(name)

    def downloadReport(self, count, blockSize, totalSize):
        percent = ((count*blockSize*100/totalSize)/self.dlCount) + ((100/self.dlCount)*self.dlCurrent)
        self.progressBar.setValue(percent)


    def done(self, result):
        if result > 0:
            self.dlCount = len(self.listWidget.selectionModel().selectedIndexes())
            if self.dlCount:
                path = forceString(QtGui.qApp.preferences.appPrefs.get('pacsImagesBrowser', ''))
                if path:
                    fileList = []
                    templatePoint = path.find('{templateFile ')
                    studyPoint = path.find('{studyUID}')
                    if templatePoint > 0:
                       template = path[templatePoint+14:]
                       template = template.split('}')[0]
                       fileName = ''
                       seriesData = getRequest('http://%s/series/%s'%(self.address, self.idList[0]))
                       if seriesData:
                           studyUID = seriesData.get('ParentStudy', '')
                           template = template.replace('%studyUID', studyUID)
                           fileName = os.path.join(forceString(QDir.temp().absolutePath()), 'ref')
                           f = open(fileName, 'w')
                           f.write(template)
                           f.close()
                       path = path[:templatePoint] + fileName
                    elif studyPoint > 0:
                        studyData = getRequest('http://%s/series/%s/study'%(self.address, self.idList[0]))
                        if studyData:
                            studyUID = studyData['MainDicomTags'].get('StudyInstanceUID', '')
                            if studyUID:
                                path = path.replace('{studyUID}', studyUID)
                    else:
                        tempDir = forceString(QDir.tempPath())
                        destinationDir = tempDir+'/pacsImages'+str(random.randrange(10000, 99999))
                        os.mkdir(destinationDir)
                        self.dlCurrent = 0
                        for index in self.listWidget.selectionModel().selectedIndexes():
                            i = index.row()
                            url = 'http://%s/series/%s/archive'%(self.address, self.idList[i])
                            self.dlCurrent += 1
                            destination = tempDir +'/'+self.idList[i]
                            urllib.urlretrieve(url, destination, reporthook=self.downloadReport)
                            fileList.append(destination)
                            updackDestDir = destinationDir+'/%i'%self.dlCurrent
                            os.mkdir(updackDestDir)
                            with contextlib.closing(zipfile.ZipFile(destination, "r")) as z:
                                z.extractall(updackDestDir)
                        self.dlCount = None
                        path = path.replace('{dir}', destinationDir)
                        path = path.replace('{file}', fileList[0] if fileList else '')
                        path = path.replace('{files}', ' '.join(fileList))
                    try:
                        p = subprocess.Popen(path.replace('\\', '/').split(' '))
                        if fileList:
                            fileDeleter = CGarbageCollector(p, destinationDir, fileList)
                            fileDeleter.start()
                    except Exception as e:
                        QtGui.QMessageBox.critical(self,
                            u'Внимание!',
                            str(e).decode('utf8'),
                            QtGui.QMessageBox.Ok,
                            QtGui.QMessageBox.Ok)
                        QtGui.qApp.logCurrentException()
                elif self.address:
                    for index in self.listWidget.selectionModel().selectedIndexes():
                        i = index.row()
                        url = 'http://%s/web-viewer/app/viewer.html?series=%s'%(self.address, self.idList[i])
                        QtGui.QDesktopServices.openUrl(QUrl(url))
                else:
                    QtGui.QMessageBox.critical(self,
                            u'Внимание!',
                            u'Программа просмотра не найдена!',
                            QtGui.QMessageBox.Ok,
                            QtGui.QMessageBox.Ok)
        QtGui.QDialog.done(self, result)


