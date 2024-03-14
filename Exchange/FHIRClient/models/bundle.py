#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/Bundle) on 2016-03-29.
#  2016, SMART Health IT.


import resource

class Bundle(resource.Resource):
    """ Contains a collection of resources.
    
    A container for a collection of resources.
    """
    
    resource_name = "Bundle"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.base = None
        """ Stated Base URL.
        Type `str`. """
        
        self.entry = None
        """ Entry in the bundle - will have a resource, or information.
        List of `BundleEntry` items (represented as `dict` in JSON). """
        
        self.link = None
        """ Links related to this Bundle.
        List of `BundleLink` items (represented as `dict` in JSON). """
        
        self.signature = None
        """ XML Digital Signature (base64 encoded).
        Type `str`. """
        
        self.total = None
        """ If search, the total number of matches.
        Type `int`. """
        
        self.type = None
        """ document | message | transaction | transaction-response | history |
        searchset | collection.
        Type `str`. """
        
        super(Bundle, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(Bundle, self).elementProperties()
        js.extend([
            ("base", "base", str, False, None, False),
            ("entry", "entry", BundleEntry, True, None, False),
            ("link", "link", BundleLink, True, None, False),
            ("signature", "signature", str, False, None, False),
            ("total", "total", int, False, None, False),
            ("type", "type", str, False, None, True),
        ])
        return js


import backboneelement

class BundleEntry(backboneelement.BackboneElement):
    """ Entry in the bundle - will have a resource, or information.
    
    An entry in a bundle resource - will either contain a resource, or
    information about a resource (transactions and history only).
    """
    
    resource_name = "BundleEntry"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.base = None
        """ Base URL, if different to bundle base.
        Type `str`. """
        
        self.link = None
        """ Links related to this entry.
        List of `BundleLink` items (represented as `dict` in JSON). """
        
        self.resource = None
        """ Resources in this bundle.
        Type `Resource` (represented as `dict` in JSON). """
        
        self.search = None
        """ Search related information.
        Type `BundleEntrySearch` (represented as `dict` in JSON). """
        
        self.transaction = None
        """ Transaction Related Information.
        Type `BundleEntryTransaction` (represented as `dict` in JSON). """
        
        self.transactionResponse = None
        """ Transaction Related Information.
        Type `BundleEntryTransactionResponse` (represented as `dict` in JSON). """
        
        super(BundleEntry, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(BundleEntry, self).elementProperties()
        js.extend([
            ("base", "base", str, False, None, False),
            ("link", "link", BundleLink, True, None, False),
            ("resource", "resource", resource.Resource, False, None, False),
            ("search", "search", BundleEntrySearch, False, None, False),
            ("transaction", "transaction", BundleEntryTransaction, False, None, False),
            ("transactionResponse", "transactionResponse", BundleEntryTransactionResponse, False, None, False),
        ])
        return js


class BundleEntrySearch(backboneelement.BackboneElement):
    """ Search related information.
    
    Information about the search process that lead to the creation of this
    entry.
    """
    
    resource_name = "BundleEntrySearch"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.mode = None
        """ match | include - why this is in the result set.
        Type `str`. """
        
        self.score = None
        """ Search ranking (between 0 and 1).
        Type `float`. """
        
        super(BundleEntrySearch, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(BundleEntrySearch, self).elementProperties()
        js.extend([
            ("mode", "mode", str, False, None, False),
            ("score", "score", float, False, None, False),
        ])
        return js


class BundleEntryTransaction(backboneelement.BackboneElement):
    """ Transaction Related Information.
    
    Additional information about how this entry should be processed as part of
    a transaction.
    """
    
    resource_name = "BundleEntryTransaction"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.ifMatch = None
        """ For managing update contention.
        Type `str`. """
        
        self.ifModifiedSince = None
        """ For managing update contention.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.ifNoneExist = None
        """ For conditional creates.
        Type `str`. """
        
        self.ifNoneMatch = None
        """ For managing cache currency.
        Type `str`. """
        
        self.method = None
        """ GET | POST | PUT | DELETE.
        Type `str`. """
        
        self.url = None
        """ The URL for the transaction.
        Type `str`. """
        
        super(BundleEntryTransaction, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(BundleEntryTransaction, self).elementProperties()
        js.extend([
            ("ifMatch", "ifMatch", str, False, None, False),
            ("ifModifiedSince", "ifModifiedSince", fhirdate.FHIRDate, False, None, False),
            ("ifNoneExist", "ifNoneExist", str, False, None, False),
            ("ifNoneMatch", "ifNoneMatch", str, False, None, False),
            ("method", "method", str, False, None, True),
            ("url", "url", str, False, None, True),
        ])
        return js


class BundleEntryTransactionResponse(backboneelement.BackboneElement):
    """ Transaction Related Information.
    
    Additional information about how this entry should be processed as part of
    a transaction.
    """
    
    resource_name = "BundleEntryTransactionResponse"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.etag = None
        """ The etag for the resource (if relevant).
        Type `str`. """
        
        self.lastModified = None
        """ Server's date time modified.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.location = None
        """ The location, if the operation returns a location.
        Type `str`. """
        
        self.status = None
        """ Status return code for entry.
        Type `str`. """
        
        super(BundleEntryTransactionResponse, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(BundleEntryTransactionResponse, self).elementProperties()
        js.extend([
            ("etag", "etag", str, False, None, False),
            ("lastModified", "lastModified", fhirdate.FHIRDate, False, None, False),
            ("location", "location", str, False, None, False),
            ("status", "status", str, False, None, True),
        ])
        return js


class BundleLink(backboneelement.BackboneElement):
    """ Links related to this Bundle.
    
    A series of links that provide context to this bundle.
    """
    
    resource_name = "BundleLink"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.relation = None
        """ http://www.iana.org/assignments/link-relations/link-relations.xhtml.
        Type `str`. """
        
        self.url = None
        """ Reference details for the link.
        Type `str`. """
        
        super(BundleLink, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(BundleLink, self).elementProperties()
        js.extend([
            ("relation", "relation", str, False, None, True),
            ("url", "url", str, False, None, True),
        ])
        return js


import fhirdate
