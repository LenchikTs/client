#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
import requests
import urllib3

urllib3.disable_warnings()


def loaWsdlOrSchema(url, loaded):
    data = requests.get(url, verify=False)
#    print dir(data)
#    print type(data.text), len(data.text)
#    print type(data.content), len(data.content)


    fileName = os.path.basename(url)
    print fileName, url
    with open(fileName, 'wb') as f:
        f.write(data.content)
    loaded.add(url)
    subUrls = re.findall('schemaLocation="([^"]+)"', data.content)
    for subUrl in subUrls:
        if subUrl not in loaded:
            loaWsdlOrSchema(subUrl, loaded)


s = set([])
loaWsdlOrSchema('https://docs-test.fss.ru/WSLnV20_2/FileOperationsLnService?wsdl', s)
# loaWsdlOrSchema('https://docs-test.fss.ru/WSLnV20_2/FileOperationsLnService?wsdl=../Faults.wsdl', s)




