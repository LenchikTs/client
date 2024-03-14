#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/DocumentManifest) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class DocumentManifest(domainresource.DomainResource):
    """ A manifest that defines a set of documents.
    """
    
    resource_name = "DocumentManifest"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.author = None
        """ Who and/or what authored the document.
        List of `FHIRReference` items referencing `Practitioner, Organization, Device, Patient, RelatedPerson` (represented as `dict` in JSON). """
        
        self.content = None
        """ Contents of the manifest.
        List of `DocumentManifestContent` items (represented as `dict` in JSON). """
        
        self.created = None
        """ When this document manifest created.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.description = None
        """ Human-readable description (title).
        Type `str`. """
        
        self.identifier = None
        """ Other identifiers for the manifest.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.masterIdentifier = None
        """ Unique Identifier for the set of documents.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Intended to get notified about this set of documents.
        List of `FHIRReference` items referencing `Patient, Practitioner, Organization` (represented as `dict` in JSON). """
        
        self.related = None
        """ Related things.
        List of `DocumentManifestRelated` items (represented as `dict` in JSON). """
        
        self.source = None
        """ The source system/application/software.
        Type `str`. """
        
        self.status = None
        """ current | superceded | entered-in-error.
        Type `str`. """
        
        self.subject = None
        """ The subject of the set of documents.
        Type `FHIRReference` referencing `Patient, Practitioner, Group, Device` (represented as `dict` in JSON). """
        
        self.type = None
        """ What kind of document set this is.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(DocumentManifest, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DocumentManifest, self).elementProperties()
        js.extend([
            ("author", "author", fhirreference.FHIRReference, True, None, False),
            ("content", "content", DocumentManifestContent, True, None, True),
            ("created", "created", fhirdate.FHIRDate, False, None, False),
            ("description", "description", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("masterIdentifier", "masterIdentifier", identifier.Identifier, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, True, None, False),
            ("related", "related", DocumentManifestRelated, True, None, False),
            ("source", "source", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", fhirreference.FHIRReference, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import backboneelement

class DocumentManifestContent(backboneelement.BackboneElement):
    """ Contents of the manifest.
    
    The manifest list.
    """
    
    resource_name = "DocumentManifestContent"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.pAttachment = None
        """ Contents of this set of documents.
        Type `Attachment` (represented as `dict` in JSON). """
        
        self.pReference = None
        """ Contents of this set of documents.
        Type `FHIRReference` referencing `DocumentReference, Media` (represented as `dict` in JSON). """
        
        super(DocumentManifestContent, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DocumentManifestContent, self).elementProperties()
        js.extend([
            ("pAttachment", "pAttachment", attachment.Attachment, False, "p", True),
            ("pReference", "pReference", fhirreference.FHIRReference, False, "p", True),
        ])
        return js


class DocumentManifestRelated(backboneelement.BackboneElement):
    """ Related things.
    
    Related identifiers or resources associated with the DocumentManifest.
    """
    
    resource_name = "DocumentManifestRelated"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.identifier = None
        """ Related Identifier.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.ref = None
        """ Related Resource.
        Type `FHIRReference` referencing `Resource` (represented as `dict` in JSON). """
        
        super(DocumentManifestRelated, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(DocumentManifestRelated, self).elementProperties()
        js.extend([
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("ref", "ref", fhirreference.FHIRReference, False, None, False),
        ])
        return js


import attachment
import codeableconcept
import fhirdate
import fhirreference
import identifier
