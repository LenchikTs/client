#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Element) on 2016-03-29.
#  2016, SMART Health IT.

import fhirabstractbase

class Element(fhirabstractbase.FHIRAbstractBase):
    """ Base for all elements.
    
    Base definition for all elements in a resource.
    """
    
    resource_name = "Element"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.extension = None
        """ Additional Content defined by implementations.
        List of `Extension` items (represented as `dict` in JSON). """
        
        self.id = None
        """ xml:id (or equivalent in JSON).
        Type `str`. """
        
        super(Element, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Element, self).elementProperties()
        js.extend([
            ("extension", "extension", extension.Extension, True, None, False),
            ("id", "id", str, False, None, False),
        ])
        return js


import extension
