#!/bin/bash

# замена <xs:attribute ref="ns1:Id"/> на <xs:attribute ref="ns1:Id" form="qualified"/>
# тут тёмное место - ZSI теряет признак qualified, а сервис требует.
# при этом я не смог составить твёрдого мнения как правильно.

#sed -iEe 's@<xs:attribute ref="ns1:Id"/>@<xs:attribute ref="ns1:Id" form="qualified"/>@g' FileOperationsLnPort.1.xsd

# перенос определения ROW из ROWSET в отдельный ROW.
# отличаются они только наличием или отсутствием id, а так вроде бы правильнее#

rm -fv FileOperationsLnPort.1.xsd.test

xmlstarlet tr up02.xslt <FileOperationsLnPort.1.xsd >FileOperationsLnPort.1.xsd.test
