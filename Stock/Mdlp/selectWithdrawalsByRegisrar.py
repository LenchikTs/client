# -*- coding: utf-8 -*-
# Заголовок будет потом,
# сейчас это "превью"
# -------------
# ЧЗ советует брать информацию из регистратора выбытия.
# возможно, что это правильно.
# у меня сейчас нет возможности работать с регистратором выбытия,
# зато есть возможность запросить что-то в МДЛП.
# поэтому так и сделаем -
# Это подборка исходящих документов типа 10531-skzkm_health_care
# выбор некоторого количества и выборка содержимого

from PyQt4.QtCore import Qt, pyqtSignature,  QAbstractTableModel, QTimer, QVariant
#from PyQt4 import QtGui

from library.DialogBase import CDialogBase
from library.Utils import withWaitCursor

from connection import CMdlpConnection

from Ui_WithdrawalsByRegisrar import Ui_withdrawalsByRegisrar


def selectWithdrawalsByRegisrar(widget, connection, date, sender):
    dlg = CWithdrawalsByRegisrar(widget)
    dlg.setFilter(date, sender)
    dlg.connection = connection
    dlg.exec_()
    return dlg.getDocumentIdsAndContent()


class CDocumentContentItem(object):
    def __init__(self,
                 sgtin,
                 batch,
                 expirationDate
                ):
        self.sgtin = sgtin
        self.batch = batch
        self.expirationDate = expirationDate


# Нам нужен список из документов,
# В списке мы хотим показать:
# - Дату (из мета-информации? из документа?)
# - Номер (из документа)
# - идентификатор РВ
# - document_id?


class CWithdrawalsByRegisrar(Ui_withdrawalsByRegisrar, CDialogBase):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.addModels('Items', CMdlpDocumensModel(self))
#        self.addObject('actLoad', QAction(self))
        self.setupUi(self)
        self.tblItems.setModel(self.modelItems)
        self.tblItems.setSelectionBehavior(self.tblItems.SelectRows)
        self.tblItems.setSelectionMode(self.tblItems.ExtendedSelection)

        self.connection   = None
        self.selectedRows = []
        self.autoLoad     = True
        self.date         = None
        self.sender       = None


    def exec_(self):
        self.show()
        if self.autoLoad:
            QTimer.singleShot(200, self.loadData) # 0.2 сек.
        return CDialogBase.exec_(self)


    def accept(self):
#        self.selectedRows = self.tblItems.getSelectedRows()
        rows = sorted(index.row() for
                      index in self.tblItems.selectionModel().selectedRows()
                     )
        self.selectedRows = rows
        CDialogBase.accept(self)


    def setFilter(self, date, sender):
        self.date = date
        self.sender = sender


    def getDocumentIdsAndContent(self):
        ids     = []
        sgtins  = []
        for row in self.selectedRows:
            item = self.modelItems.items[row]
            ids.append(item.documentId)
            sgtins.extend(item.content)

        succeedSgtinInfos, failedSgtinInfos = self.connection.getSgtinsByList(sgtins)
        content = [ CDocumentContentItem(sgtinInfo.sgtin,
                                         sgtinInfo.batch,
                                         sgtinInfo.expirationDate
                                        )
                    for sgtinInfo in succeedSgtinInfos
                  ]
        return ids, content


#    @withExceptionLog
    @withWaitCursor
    def loadData(self):
        self.modelItems.removeAllItems()
        if self.connection is None:
            self.connection = CMdlpConnection()
        connection = self.connection
        filter = {}
        if self.date:
            filter['begDate'] = self.date
            filter['endDate'] = self.date
        docs = connection.getOutcomingDocuments(count     = 100,
                                                docType   = 10531,
                                                senderId  = self.sender,
                                                docStatus = 'PROCESSED_DOCUMENT',
                                                **filter
                                               )
        for metaDoc in docs:
            documentId = metaDoc.documentId
            outerDoc = connection.getDocument(documentId)
            doc = outerDoc.skzkm_health_care
            content = []
            for u in doc.order_details.union:
                sgtin = unicode(u.sgtin)
                if sgtin:
                    content.append(sgtin)
            item = CMdlpDocumentDescr(date       = unicode(doc.doc_date),
                                      number     = unicode(doc.doc_num),
                                      deviceId   = unicode(doc.device_info.device_id),
                                      documentId = documentId,
                                      content    = content
                                     )
            self.modelItems.addItem(item)


    @pyqtSignature('QModelIndex')
    def on_tblItems_doubleClicked(self, index):
        self.selectedRow = index.row()
        self.close()



class CMdlpDocumentDescr:
    headers = ( u'Номер',
                u'Дата',
                u'Регистратор выбытия',
                u'Идентификатор документа',
              )

    def __init__(self,
                       number=None,
                       date=None,
                       deviceId = None,
                       documentId = None,
                       content = None
                ):
        self.number     = number
        self.date       = date
        self.deviceId   = deviceId
        self.documentId = documentId
        self.content    = content


    @classmethod
    def columnCount(cls):
        return len(cls.headers)


    @classmethod
    def header(cls, column):
        return cls.headers[column]


    def data(self, column):
        if column == 0: return self.number
        if column == 1: return self.date
        if column == 2: return self.deviceId
        if column == 3: return self.documentId
        return None


class CMdlpDocumensModel(QAbstractTableModel):
    def __init__(self, parent = 0):
        QAbstractTableModel.__init__(self, parent)
        self.items = []


    def columnCount(self, parent=None):
        return CMdlpDocumentDescr.columnCount()


    def rowCount(self, parent=None):
        return len(self.items)


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(CMdlpDocumentDescr.header(section))


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return QVariant(self.items[row].data(column))
        return QVariant()


    def removeAllItems(self):
        self.items = []
        self.reset()


    def addItem(self, item):
        self.items.append(item)
        self.reset()

