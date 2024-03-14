#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
import requests
import urllib3


import xml.etree.ElementTree as ET



t = open('FileOperationsLnService?wsdl','rb').read()


root = ET.fromstring(t)
print root

imps = root.findall('{http://schemas.xmlsoap.org/wsdl/}import')
print imps
for imp in imps:
    print imp, dir(imp), imp.attrib['location']
    imp.attrib['location'] = 'aaaa'

print ET.tostring(root, encoding='UTF-8')