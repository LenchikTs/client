<?xml version="1.0" encoding="UTF-8"?>
<!--
# перенос определения ROW из ROWSET в ROW

<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:complexType name="ROWSET">
        <xs:sequence>
            <xs:element name="ROW" maxOccurs="unbounded">
                <xs:complexType>
...
в
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:complexType name="ROW">

 xmlns:xsd="http://www.w3.org/2001/XMLSchema"

-->
<xsl:stylesheet
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:xs="http://www.w3.org/2001/XMLSchema"
 version="1.0">
    <xsl:output method="xml" indent="yes"/>

    <!-- copy all nodes and attributes -->
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>

    <!-- now work -->
    <xsl:template match="/xs:schema/xs:complexType[@name='ROW']">
        <xs:complexType name="ROW">
            <xsl:apply-templates select="/xs:schema/xs:complexType[@name='ROWSET']/xs:sequence/xs:element[@name='ROW']/xs:complexType/*" />
        </xs:complexType>
    </xsl:template>

    <xsl:template match="/xs:schema/xs:complexType[@name='ROWSET']/xs:sequence/xs:element[@name='ROW']">
        <xs:element name="ROW" type="tns:ROW" maxOccurs="unbounded"/>
    </xsl:template>
</xsl:stylesheet>
