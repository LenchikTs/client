# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Преобразование генерируемого нами pdf в pdf/a1
## Для преобразования используется своя копия PyPDF2
## (см. https://github.com/mstamy2/PyPDF2)
##
## Решение завести свою копию обусловлено тем, что в различных версиях 
## дистрибутивов PyPDF2 может отсутствовать или присутствовать в
## очень старой версии.
##
## Кроме того я подправил import * и прочие жалобы pyflakes
##
#############################################################################


import uuid

from PyPDF2x import PdfFileReader, PdfFileWriter
from PyPDF2x.generic import TextStringObject, ByteStringObject, NameObject, ArrayObject, DictionaryObject, DecodedStreamObject, NumberObject
from datetime import datetime
from isodate.tzinfo import LOCAL

from extractGlyphWidthsFromTTFData import extractGlyphWidthsFromTTFData

__all__ = ( 'fixPdf',
          )

def fixPdf(sourceSream, destinationStream, title=None, author=None, subject=None, keywords=None, creator=None, producer=None):
    reader = PdfFileReader(sourceSream)
    documentInfo = reader.getDocumentInfo()
    writer = MyPdfFileWriter()
    writer.setTitle(title or documentInfo.title or '')
    writer.setAuthor(author or documentInfo.author or '')
    writer.setSubject(subject or documentInfo.subject or '')
    writer.setKeywords(keywords or '')
    writer.setCreator(creator or documentInfo.creator or '')
    writer.setProducer(producer or documentInfo.producer or '')

    for page in reader.pages:
        writer.addPage(page)
    writer.write(destinationStream)



class MyPdfFileWriter(PdfFileWriter):
    def __init__(self):
        PdfFileWriter.__init__(self)
        self._header = '%PDF-1.4'

        self._id       = uuid.uuid4()
        self._title    = u''
        self._author   = u''
        self._subject  = u''
        self._keywords = u''
        self._creator  = u''
        self._producer = u''
        self._creationDate = datetime.now(LOCAL)
#        self._modifyDate = datetime.now(LOCAL)


    def setTitle(self, title):
        self._title = title


    def setAuthor(self, author):
        self._author = author


    def setSubject(self, subject):
        self._subject = subject


    def setKeywords(self, keywords):
        self._keywords = keywords


    def setCreator(self, creator):
        self._creator = creator


    def setProducer(self, producer):
        self._producer = producer


    def write(self, stream):
        self.fixMetadata()
        self.fixId()
        self.addXmpMetadata()
        self.addColourProfileAndOutputIntent()
        self.fixFonts()
        self.fixXObjects()
        PdfFileWriter.write(self, stream)



    def fixMetadata(self):
        info = self._info.getObject()

        info[ NameObject('/Title')    ]  = TextStringObject( self._title )
        info[ NameObject('/Author')   ] = TextStringObject( self._author )
        info[ NameObject('/Subject')  ] = TextStringObject( self._subject )
        info[ NameObject('/Keywords') ] = TextStringObject( self._keywords )
        info[ NameObject('/Creator')  ] = TextStringObject( self._creator )
        info[ NameObject('/Producer') ] = TextStringObject( self._producer )
        info[ NameObject('/CreationDate') ] = TextStringObject( self._creationDate.strftime('D:%Y%m%d%H%M%S') + self._extractTz(self._creationDate, '\'') )


    def fixId(self):
        self._ID = ArrayObject()
        self._ID.append(ByteStringObject(self._id.bytes))
        self._ID.append(ByteStringObject(self._id.bytes))


    def addXmpMetadata(self):
        metadata = DecodedStreamObject()
        metadata[NameObject('/Type')]    = NameObject('/Metadata')
        metadata[NameObject('/Subtype')] = NameObject('/XML')

        # done: title, author, subject, producer, keywords, creator, createdate
        # что-то ещё? modifyDate?

        z = u'''<?xpacket begin='\uFEFF' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:pdf="http://ns.adobe.com/pdf/1.3/" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/">
<pdf:Producer>%(producer)s</pdf:Producer>
<pdf:Keywords>%(keywords)s</pdf:Keywords>
<xmp:CreateDate>%(creationDate)s</xmp:CreateDate>
<xmp:CreatorTool>%(creator)s</xmp:CreatorTool>
<xmpMM:DocumentID>uuid:%(id)s</xmpMM:DocumentID>
<dc:format>application/pdf</dc:format>
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">%(title)s</rdf:li></rdf:Alt></dc:title>
<dc:creator><rdf:Seq><rdf:li>%(author)s</rdf:li></rdf:Seq></dc:creator>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">%(subject)s</rdf:li></rdf:Alt></dc:description>
<pdfaid:conformance>B</pdfaid:conformance>
<pdfaid:part>1</pdfaid:part>
</rdf:Description>
</rdf:RDF>
</x:xmpmeta>
<?xpacket end='r'?>
''' % { 'id':           str(self._id),
        'title':        self.escapeXmlEntity(self._title),
        'author':       self.escapeXmlEntity(self._author),
        'subject':      self.escapeXmlEntity(self._subject),
        'keywords':     self.escapeXmlEntity(self._keywords),
        'creator':      self.escapeXmlEntity(self._creator),
        'producer':     self.escapeXmlEntity(self._producer),
        'creationDate': self._creationDate.strftime('%Y-%m-%dT%H:%M:%S') + self._extractTz(self._creationDate, ':')
      }
        metadata.setData(z.encode('utf-8'))
        metadataRef = self._addObject(metadata)
        r = self._root_object
        r[NameObject('/Metadata')] = metadataRef


    def addColourProfileAndOutputIntent(self):
        # stolen from kde5-digikam-data-5.9.0-alt1.M80P.1
        profileDump = 'AAACRGFyZ2wCIAAAbW50clJHQiBYWVogB9YABwAIAAMAHAAvYWNzcE1TRlQAAAAAbm9uZQAAAAAA' \
                      'AAAAAAAAAAAAAAAAAPbWAAEAAAAA0y1hcmdsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAKZGVzYwAAAPwAAAB7Y3BydAAAAXgAAAA1d3RwdAAAAbAAAAAUYmtw' \
                      'dAAAAcQAAAAUclhZWgAAAdgAAAAUZ1hZWgAAAewAAAAUYlhZWgAAAgAAAAAUclRSQwAAAhQAAAAO' \
                      'Z1RSQwAAAiQAAAAOYlRSQwAAAjQAAAAOZGVzYwAAAAAAAAAhQ29tcGF0aWJsZSB3aXRoIEFkb2Jl' \
                      'IFJHQiAoMTk5OCkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHRleHQAAAAAUHVibGljIERvbWFpbi4g' \
                      'Tm8gV2FycmFudHksIFVzZSBhdCBvd24gcmlzay4AAAAAWFlaIAAAAAAAAPNRAAEAAAABFsxYWVog' \
                      'AAAAAAAAAAAAAAAAAAAAAFhZWiAAAAAAAACcGAAAT6UAAAT8WFlaIAAAAAAAADSNAACgLAAAD5VY' \
                      'WVogAAAAAAAAJjEAABAvAAC+nGN1cnYAAAAAAAAAAQIzAABjdXJ2AAAAAAAAAAECMwAAY3VydgAA' \
                      'AAAAAAABAjMAAA=='

        rawProfile = DecodedStreamObject()
        rawProfile.setData(profileDump.decode('base64'))
        profile = rawProfile.flateEncode()
        profile[NameObject('/N')] = NumberObject(3)
        profileRef = self._addObject(profile)

        outputIntent = DictionaryObject()
        outputIntent[NameObject('/Type')] = NameObject('/OutputIntent')
#        outputIntent[NameObject('/OutputConditionIdentifier')] = TextStringObject('sRGB') # sRGB ?
        outputIntent[NameObject('/OutputConditionIdentifier')] = TextStringObject('compatibleWithAdobe1989') # sRGB ?
        outputIntent[NameObject('/S')]    = NameObject('/GTS_PDFA1')
        outputIntent[NameObject('/DestOutputProfile')] = profileRef

        outputIntentRef = self._addObject(outputIntent)
        r = self._root_object
        r[NameObject('/OutputIntents')] = ArrayObject([outputIntentRef])


    def fixFonts(self):
        fixedFonts = set()

        for i in xrange( self.getNumPages() ):
            page = self.getPage(i)
            resources = page.get('/Resources')
            if resources:
                fonts = resources.getObject().get('/Font')
                if fonts:
                    for font in fonts.getObject().itervalues():
                        for df in font.getObject()['/DescendantFonts']:
                            dfo = df.getObject()
                            if id(dfo) not in fixedFonts:
                                fdo = dfo['/FontDescriptor']
                                ff = fdo['/FontFile2']
                                widths = extractGlyphWidthsFromTTFData(ff.getData())
                                if '/W' in dfo:
                                    dfo['/W'][1] = ArrayObject([NumberObject(gw) for gw in widths])
                                if '/Widths' in dfo:
                                    dfo['/Widths'] = ArrayObject([NumberObject(gw) for gw in widths])
                                fixedFonts.add(id(dfo))


    def fixXObjects(self):
        for i in xrange( self.getNumPages() ):
            page = self.getPage(i)
            resources = page.get('/Resources')
            if resources:
                xobjects = resources.getObject().get('/XObject')
                if xobjects:
                    for xobject in xobjects.getObject().itervalues():
                        xo = xobject.getObject()
                        if '/SMask' in xo:
                            del xo['/SMask']


    @staticmethod
    def escapeXmlEntity(txt):
        return txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')



    @staticmethod
    def _extractTz(dt, sep=':'):
        offset = dt.strftime('%z')
        if offset == '':
            return 'Z'
        else:
            return offset[:3] + sep + offset[3:]
