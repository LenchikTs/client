#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/ProcessResponse) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class ProcessResponse(domainresource.DomainResource):
    """ ProcessResponse resource.
    
    This resource provides processing status, errors and notes from the
    processing of a resource.
    """
    
    resource_name = "ProcessResponse"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.created = None
        """ Creation date.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.disposition = None
        """ Disposition Message.
        Type `str`. """
        
        self.error = None
        """ Error code.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.form = None
        """ Printed Form Identifier.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Business Identifier.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.notes = None
        """ Notes.
        List of `ProcessResponseNotes` items (represented as `dict` in JSON). """
        
        self.organization = None
        """ Authoring Organization.
        Type `FHIRReference` referencing `Organization` (represented as `dict` in JSON). """
        
        self.originalRuleset = None
        """ Original version.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.outcome = None
        """ Processing outcome.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.request = None
        """ Request reference.
        Type `FHIRReference` referencing `Resource` (represented as `dict` in JSON). """
        
        self.requestOrganization = None
        """ Responsible organization.
        Type `FHIRReference` referencing `Organization` (represented as `dict` in JSON). """
        
        self.requestProvider = None
        """ Responsible Practitioner.
        Type `FHIRReference` referencing `Practitioner` (represented as `dict` in JSON). """
        
        self.ruleset = None
        """ Resource version.
        Type `Coding` (represented as `dict` in JSON). """
        
        super(ProcessResponse, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcessResponse, self).elementProperties()
        js.extend([
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("disposition", "disposition", str, False, None, False),
            ("error", "error", coding.Coding, True, None, False),
            ("form", "form", coding.Coding, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("notes", "notes", ProcessResponseNotes, True, None, False),
            ("organization", "organization", fhirreference.FHIRReference, False, None, False),
            ("originalRuleset", "originalRuleset", coding.Coding, False, None, False),
            ("outcome", "outcome", coding.Coding, False, None, False),
            ("request", "request", fhirreference.FHIRReference, False, None, False),
            ("requestOrganization", "requestOrganization", fhirreference.FHIRReference, False, None, False),
            ("requestProvider", "requestProvider", fhirreference.FHIRReference, False, None, False),
            ("ruleset", "ruleset", coding.Coding, False, None, False),
        ])
        return js


import backboneelement

class ProcessResponseNotes(backboneelement.BackboneElement):
    """ Notes.
    
    Suite of processing note or additional requirements is the processing has
    been held.
    """
    
    resource_name = "ProcessResponseNotes"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.text = None
        """ Notes text.
        Type `str`. """
        
        self.type = None
        """ display | print | printoper.
        Type `Coding` (represented as `dict` in JSON). """
        
        super(ProcessResponseNotes, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ProcessResponseNotes, self).elementProperties()
        js.extend([
            ("text", "text", str, False, None, False),
            ("type", "type", coding.Coding, False, None, False),
        ])
        return js


import coding
import fhirdate
import fhirreference
import identifier
