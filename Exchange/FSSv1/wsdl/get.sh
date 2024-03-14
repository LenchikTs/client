#!/bin/bash

DATE=`date +'%F'`
URL=https://docs-test.fss.ru/WSLnV11/FileOperationsLnPort

mkdir -p "${DATE}/raw"

/usr/bin/curl --insecure  "${URL}?WSDL" -o "${DATE}/raw/FileOperationsLnPort.wsdl"
/usr/bin/curl --insecure  "${URL}?xsd=1" -o "${DATE}/raw/FileOperationsLnPort.1.xsd"
/usr/bin/curl --insecure  "${URL}?xsd=2" -o "${DATE}/raw/FileOperationsLnPort.2.xsd"

xmlformat <"${DATE}/raw/FileOperationsLnPort.wsdl"  >"${DATE}/FileOperationsLnPort.wsdl"
xmlformat <"${DATE}/raw/FileOperationsLnPort.1.xsd" >"${DATE}/FileOperationsLnPort.1.xsd"
xmlformat <"${DATE}/raw/FileOperationsLnPort.2.xsd" >"${DATE}/FileOperationsLnPort.2.xsd"

for FN in "${DATE}/FileOperationsLnPort".*
do
#    echo ${FN} 
    sed -r -i \
        -e 's/schemaLocation=".*FileOperationsLnPort\?xsd=1"/schemaLocation="FileOperationsLnPort.1.xsd"/g' \
        -e 's/schemaLocation=".*FileOperationsLnPort\?xsd=2"/schemaLocation="FileOperationsLnPort.2.xsd"/g' \
        "${FN}"
done
