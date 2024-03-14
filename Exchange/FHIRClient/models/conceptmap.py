#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/ConceptMap) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class ConceptMap(domainresource.DomainResource):
    """ A map from one set of concepts to one or more other concepts.
    
    A statement of relationships from one set of concepts to one or more other
    concepts - either code systems or data elements, or classes in class
    models.
    """
    
    resource_name = "ConceptMap"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.contact = None
        """ Contact details of the publisher.
        List of `ConceptMapContact` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or Publishing restrictions.
        Type `str`. """
        
        self.date = None
        """ Date for given status.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.description = None
        """ Human language description of the concept map.
        Type `str`. """
        
        self.element = None
        """ Mappings for a concept from the source set.
        List of `ConceptMapElement` items (represented as `dict` in JSON). """
        
        self.experimental = None
        """ If for testing purposes, not real usage.
        Type `bool`. """
        
        self.identifier = None
        """ Additional identifier for the concept map.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.name = None
        """ Informal name for this concept map.
        Type `str`. """
        
        self.publisher = None
        """ Name of the publisher (Organization or individual).
        Type `str`. """
        
        self.requirements = None
        """ Why is this needed?.
        Type `str`. """
        
        self.sourceReference = None
        """ Identifies the source of the concepts which are being mapped.
        Type `FHIRReference` referencing `ValueSet, StructureDefinition` (represented as `dict` in JSON). """
        
        self.sourceUri = None
        """ Identifies the source of the concepts which are being mapped.
        Type `str`. """
        
        self.status = None
        """ draft | active | retired.
        Type `str`. """
        
        self.targetReference = None
        """ Provides context to the mappings.
        Type `FHIRReference` referencing `ValueSet, StructureDefinition` (represented as `dict` in JSON). """
        
        self.targetUri = None
        """ Provides context to the mappings.
        Type `str`. """
        
        self.url = None
        """ Globally unique logical id for concept map.
        Type `str`. """
        
        self.useContext = None
        """ Content intends to support these contexts.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Logical id for this version of the concept map.
        Type `str`. """
        
        super(ConceptMap, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ConceptMap, self).elementProperties()
        js.extend([
            ("contact", "contact", ConceptMapContact, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("description", "description", str, False, None, False),
            ("element", "element", ConceptMapElement, True, None, False),
            ("experimental", "experimental", bool, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("name", "name", str, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("requirements", "requirements", str, False, None, False),
            ("sourceReference", "sourceReference", fhirreference.FHIRReference, False, "source", True),
            ("sourceUri", "sourceUri", str, False, "source", True),
            ("status", "status", str, False, None, True),
            ("targetReference", "targetReference", fhirreference.FHIRReference, False, "target", True),
            ("targetUri", "targetUri", str, False, "target", True),
            ("url", "url", str, False, None, False),
            ("useContext", "useContext", codeableconcept.CodeableConcept, True, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js


import backboneelement

class ConceptMapContact(backboneelement.BackboneElement):
    """ Contact details of the publisher.
    
    Contacts to assist a user in finding and communicating with the publisher.
    """
    
    resource_name = "ConceptMapContact"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.name = None
        """ Name of a individual to contact.
        Type `str`. """
        
        self.telecom = None
        """ Contact details for individual or publisher.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        super(ConceptMapContact, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ConceptMapContact, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
        ])
        return js


class ConceptMapElement(backboneelement.BackboneElement):
    """ Mappings for a concept from the source set.
    
    Mappings for an individual concept in the source to one or more concepts in
    the target.
    """
    
    resource_name = "ConceptMapElement"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.code = None
        """ Identifies element being mapped.
        Type `str`. """
        
        self.codeSystem = None
        """ Code System (if value set crosses code systems).
        Type `str`. """
        
        self.dependsOn = None
        """ Other elements required for this mapping (from context).
        List of `ConceptMapElementDependsOn` items (represented as `dict` in JSON). """
        
        self.map = None
        """ Target of this map.
        List of `ConceptMapElementMap` items (represented as `dict` in JSON). """
        
        super(ConceptMapElement, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ConceptMapElement, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("codeSystem", "codeSystem", str, False, None, False),
            ("dependsOn", "dependsOn", ConceptMapElementDependsOn, True, None, False),
            ("map", "map", ConceptMapElementMap, True, None, False),
        ])
        return js


class ConceptMapElementDependsOn(backboneelement.BackboneElement):
    """ Other elements required for this mapping (from context).
    
    A set of additional dependencies for this mapping to hold. This mapping is
    only applicable if the specified element can be resolved, and it has the
    specified value.
    """
    
    resource_name = "ConceptMapElementDependsOn"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.code = None
        """ Value of the referenced element.
        Type `str`. """
        
        self.codeSystem = None
        """ Code System (if necessary).
        Type `str`. """
        
        self.element = None
        """ Reference to element/field/valueset mapping depends on.
        Type `str`. """
        
        super(ConceptMapElementDependsOn, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ConceptMapElementDependsOn, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("codeSystem", "codeSystem", str, False, None, True),
            ("element", "element", str, False, None, True),
        ])
        return js


class ConceptMapElementMap(backboneelement.BackboneElement):
    """ Target of this map.
    
    A concept from the target value set that this concept maps to.
    """
    
    resource_name = "ConceptMapElementMap"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.code = None
        """ Code that identifies the target element.
        Type `str`. """
        
        self.codeSystem = None
        """ System of the target (if necessary).
        Type `str`. """
        
        self.comments = None
        """ Description of status/issues in mapping.
        Type `str`. """
        
        self.equivalence = None
        """ equivalent | equal | wider | subsumes | narrower | specialises |
        inexact | unmatched | disjoint.
        Type `str`. """
        
        self.product = None
        """ Other concepts that this mapping also produces.
        List of `ConceptMapElementDependsOn` items (represented as `dict` in JSON). """
        
        super(ConceptMapElementMap, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ConceptMapElementMap, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("codeSystem", "codeSystem", str, False, None, False),
            ("comments", "comments", str, False, None, False),
            ("equivalence", "equivalence", str, False, None, True),
            ("product", "product", ConceptMapElementDependsOn, True, None, False),
        ])
        return js


import codeableconcept
import contactpoint
import fhirdate
import fhirreference
import identifier
