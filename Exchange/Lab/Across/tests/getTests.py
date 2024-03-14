#!/usr/bin/python
# -*- coding: utf-8 -*-

from IConvertservice_client import *
from classes import *

logFile = file('logGetTests','w+');

loc = IConvertserviceLocator()
#port = loc.getIConvertPort('http://across.utech.ru/ws_test/ServiceServ.exe/soap/IConvert',tracefile=logFile)
port = loc.getIConvertPort('http://utech.across.ru/ws_test/ServiceServ.exe/soap/IConvert',tracefile=logFile)

print '='*10+' call test '+'='*40

responceObject = port.SendTableTest(SendTableTest1Request())
print responceObject, responceObject._return
