#!/usr/bin/python
# -*- coding: utf-8 -*-

from IConvertservice_client import *
from classes import *

logFile = file('log','w+');

loc = IConvertserviceLocator()
port = loc.getIConvertPort('http://utech.across.ru/ws_test/ServiceServ.exe/soap/IConvert',tracefile=logFile)

print '='*10+' call test '+'='*40

responceObject = port.SendTableSpecimen(SendTableSpecimen2Request())
print responceObject, responceObject._return
