<?xml version="1.0" encoding="UTF-8"?>
<!--
# замена
#        <xsd:schema>
#            <xsd:import namespace="http://ru/ibs/fss/ln/ws/FileOperationsLn.wsdl" schemaLocation="FileOperationsLnPort.1.xsd"/>
#        </xsd:schema>
#
#        <xsd:schema targetNamespace="http://ru/ibs/fss/ln/ws/FileOperationsLn.wsdl">
#            <xsd:include schemaLocation="FileOperationsLnPort.1.xsd"/>
#        </xsd:schema>
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="1.0">
    <xsl:output method="xml" indent="yes"/>

    <!-- copy all nodes and attributes -->
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>

    <!-- now work -->
    <xsl:template match="xsd:schema">
        <xsd:schema targetNamespace="{xsd:import/@namespace}">
            <xsd:include schemaLocation="{xsd:import/@schemaLocation}"/>
        </xsd:schema>
    </xsl:template>
</xsl:stylesheet>
