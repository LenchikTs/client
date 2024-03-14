import requests
import urlparse
from PyQt4 import QtGui
from PyQt4.QtCore import QXmlStreamReader

from library.Utils import forceString


class CPyServices:
    def __init__(self, url):
        url = url.replace('\\\\', '//')
        self.url = url
        self.schematronApi = urlparse.urljoin(url, '/api/schematron/')
    
    def listCdaCodes(self):
        try:
            return requests.get(self.schematronApi + 'list_cda_codes').json()
        except requests.exceptions.RequestException:
            QtGui.qApp.logCurrentException()

    def validateCda(self, xmlText):
        files = {'file': xmlText}
        response = requests.post(self.schematronApi + 'validate_cda', files=files)
        try:
            json = response.json()
        except ValueError:
            json = None
        if response.status_code != 200:
            if not json:
                raise Exception(response.text)
            if 'detail' in json:
                raise Exception(json['detail'])
            else:
                raise Exception(json)
        return json


def getCdaCode(xmlText):
    reader = QXmlStreamReader(xmlText)
    reader.setNamespaceProcessing(False)
    while not reader.atEnd():
        reader.readNext()
        if reader.isStartElement() and reader.name() == "code":
            attributes = reader.attributes()
            if attributes.value("codeSystem") == "1.2.643.5.1.13.13.11.1522":
                return str(attributes.value("code"))
    return None


def getPyServices():
    url = forceString(QtGui.qApp.getGlobalPreference('23:servicesURL'))
    return CPyServices(url) if url else None
