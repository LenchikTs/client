#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Reference) on 2016-03-29.
#  2016, SMART Health IT.


import element

class Reference(element.Element):
    """ A reference from one resource to another.
    """
    
    resource_name = "Reference"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.display = None
        """ Text alternative for the resource.
        Type `str`. """
        
        self.reference = None
        """ Relative, internal or absolute URL reference.
        Type `str`. """
        
        super(Reference, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Reference, self).elementProperties()
        js.extend([
            ("display", "display", str, False, None, False),
            ("reference", "reference", str, False, None, False),
        ])
        return js

