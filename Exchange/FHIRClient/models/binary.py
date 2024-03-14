#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Binary) on 2016-03-29.
#  2016, SMART Health IT.


import resource

class Binary(resource.Resource):
    """ Pure binary content defined by sime other format than FHIR.
    
    A binary resource can contain any content, whether text, image, pdf, zip
    archive, etc.
    """
    
    resource_name = "Binary"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.content = None
        """ The actual content.
        Type `str`. """
        
        self.contentType = None
        """ MimeType of the binary content.
        Type `str`. """
        
        super(Binary, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Binary, self).elementProperties()
        js.extend([
            ("content", "content", str, False, None, True),
            ("contentType", "contentType", str, False, None, True),
        ])
        return js


