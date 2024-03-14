#!/bin/bash

# замена
#        <xsd:schema>
#            <xsd:import namespace="http://ru/ibs/fss/ln/ws/FileOperationsLn.wsdl" schemaLocation="FileOperationsLnPort.1.xsd"/>
#        </xsd:schema>
#
#        <xsd:schema targetNamespace="http://ru/ibs/fss/ln/ws/FileOperationsLn.wsdl">
#            <xsd:include schemaLocation="FileOperationsLnPort.1.xsd"/>
#        </xsd:schema>

cp -fv FileOperationsLnPort.wsdl FileOperationsLnPort.wsdl.before-up01

xmlstarlet tr up01.xslt <FileOperationsLnPort.wsdl.before-up01 | xmlformat >FileOperationsLnPort.wsdl

rm -fv FileOperationsLnPort.wsdl.before-up01
