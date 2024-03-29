#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/ValueSet) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class ValueSet(domainresource.DomainResource):
    """ A set of codes drawn from one or more code systems.
    
    A value set specifies a set of codes drawn from one or more code systems.
    """
    
    resource_name = "ValueSet"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.compose = None
        """ When value set includes codes from elsewhere.
        Type `ValueSetCompose` (represented as `dict` in JSON). """
        
        self.contact = None
        """ Contact details of the publisher.
        List of `ValueSetContact` items (represented as `dict` in JSON). """
        
        self.copyright = None
        """ Use and/or Publishing restrictions.
        Type `str`. """
        
        self.date = None
        """ Date for given status.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.define = None
        """ When value set defines its own codes.
        Type `ValueSetDefine` (represented as `dict` in JSON). """
        
        self.description = None
        """ Human language description of the value set.
        Type `str`. """
        
        self.expansion = None
        """ Used when the value set is "expanded".
        Type `ValueSetExpansion` (represented as `dict` in JSON). """
        
        self.experimental = None
        """ If for testing purposes, not real usage.
        Type `bool`. """
        
        self.extensible = None
        """ Whether this is intended to be used with an extensible binding.
        Type `bool`. """
        
        self.identifier = None
        """ Additional identifier for the value set (v2 / CDA).
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.immutable = None
        """ Indicates whether or not any change to the content logical
        definition may occur.
        Type `bool`. """
        
        self.lockedDate = None
        """ Fixed date for all referenced code systems and value sets.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.name = None
        """ Informal name for this value set.
        Type `str`. """
        
        self.publisher = None
        """ Name of the publisher (Organization or individual).
        Type `str`. """
        
        self.requirements = None
        """ Why is this needed?.
        Type `str`. """
        
        self.status = None
        """ draft | active | retired.
        Type `str`. """
        
        self.url = None
        """ Globally unique logical id for  value set.
        Type `str`. """
        
        self.useContext = None
        """ Content intends to support these contexts.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.version = None
        """ Logical id for this version of the value set.
        Type `str`. """
        
        super(ValueSet, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSet, self).elementProperties()
        js.extend([
            ("compose", "compose", ValueSetCompose, False, None, False),
            ("contact", "contact", ValueSetContact, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("define", "define", ValueSetDefine, False, None, False),
            ("description", "description", str, False, None, False),
            ("expansion", "expansion", ValueSetExpansion, False, None, False),
            ("experimental", "experimental", bool, False, None, False),
            ("extensible", "extensible", bool, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("immutable", "immutable", bool, False, None, False),
            ("lockedDate", "lockedDate", fhirdate.FHIRDate, False, None, False),
            ("name", "name", str, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("requirements", "requirements", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("url", "url", str, False, None, False),
            ("useContext", "useContext", codeableconcept.CodeableConcept, True, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js


import backboneelement

class ValueSetCompose(backboneelement.BackboneElement):
    """ When value set includes codes from elsewhere.
    """
    
    resource_name = "ValueSetCompose"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.exclude = None
        """ Explicitly exclude codes.
        List of `ValueSetComposeInclude` items (represented as `dict` in JSON). """
        
        self.import_fhir = None
        """ Import the contents of another value set.
        List of `str` items. """
        
        self.include = None
        """ Include one or more codes from a code system.
        List of `ValueSetComposeInclude` items (represented as `dict` in JSON). """
        
        super(ValueSetCompose, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetCompose, self).elementProperties()
        js.extend([
            ("exclude", "exclude", ValueSetComposeInclude, True, None, False),
            ("import_fhir", "import", str, True, None, False),
            ("include", "include", ValueSetComposeInclude, True, None, False),
        ])
        return js


class ValueSetComposeInclude(backboneelement.BackboneElement):
    """ Include one or more codes from a code system.
    """
    
    resource_name = "ValueSetComposeInclude"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.concept = None
        """ A concept defined in the system.
        List of `ValueSetComposeIncludeConcept` items (represented as `dict` in JSON). """
        
        self.filter = None
        """ Select codes/concepts by their properties (including relationships).
        List of `ValueSetComposeIncludeFilter` items (represented as `dict` in JSON). """
        
        self.system = None
        """ The system the codes come from.
        Type `str`. """
        
        self.version = None
        """ Specific version of the code system referred to.
        Type `str`. """
        
        super(ValueSetComposeInclude, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetComposeInclude, self).elementProperties()
        js.extend([
            ("concept", "concept", ValueSetComposeIncludeConcept, True, None, False),
            ("filter", "filter", ValueSetComposeIncludeFilter, True, None, False),
            ("system", "system", str, False, None, True),
            ("version", "version", str, False, None, False),
        ])
        return js


class ValueSetComposeIncludeConcept(backboneelement.BackboneElement):
    """ A concept defined in the system.
    
    Specifies a concept to be included or excluded.
    """
    
    resource_name = "ValueSetComposeIncludeConcept"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.code = None
        """ Code or expression from system.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for this valueset.
        List of `ValueSetDefineConceptDesignation` items (represented as `dict` in JSON). """
        
        self.display = None
        """ Test to display for this code for this value set.
        Type `str`. """
        
        super(ValueSetComposeIncludeConcept, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetComposeIncludeConcept, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, True),
            ("designation", "designation", ValueSetDefineConceptDesignation, True, None, False),
            ("display", "display", str, False, None, False),
        ])
        return js


class ValueSetComposeIncludeFilter(backboneelement.BackboneElement):
    """ Select codes/concepts by their properties (including relationships).
    
    Select concepts by specify a matching criteria based on the properties
    (including relationships) defined by the system. If multiple filters are
    specified, they SHALL all be true.
    """
    
    resource_name = "ValueSetComposeIncludeFilter"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.op = None
        """ = | is-a | is-not-a | regex | in | not-in.
        Type `str`. """
        
        self.property = None
        """ A property defined by the code system.
        Type `str`. """
        
        self.value = None
        """ Code from the system, or regex criteria.
        Type `str`. """
        
        super(ValueSetComposeIncludeFilter, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetComposeIncludeFilter, self).elementProperties()
        js.extend([
            ("op", "op", str, False, None, True),
            ("property", "property", str, False, None, True),
            ("value", "value", str, False, None, True),
        ])
        return js


class ValueSetContact(backboneelement.BackboneElement):
    """ Contact details of the publisher.
    
    Contacts to assist a user in finding and communicating with the publisher.
    """
    
    resource_name = "ValueSetContact"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.name = None
        """ Name of a individual to contact.
        Type `str`. """
        
        self.telecom = None
        """ Contact details for individual or publisher.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        super(ValueSetContact, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetContact, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            ("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
        ])
        return js


class ValueSetDefine(backboneelement.BackboneElement):
    """ When value set defines its own codes.
    
    A definition of an code system, inlined into the value set.
    """
    
    resource_name = "ValueSetDefine"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.caseSensitive = None
        """ If code comparison is case sensitive.
        Type `bool`. """
        
        self.concept = None
        """ Concepts in the code system.
        List of `ValueSetDefineConcept` items (represented as `dict` in JSON). """
        
        self.system = None
        """ URI to identify the code system.
        Type `str`. """
        
        self.version = None
        """ Version of this system.
        Type `str`. """
        
        super(ValueSetDefine, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetDefine, self).elementProperties()
        js.extend([
            ("caseSensitive", "caseSensitive", bool, False, None, False),
            ("concept", "concept", ValueSetDefineConcept, True, None, False),
            ("system", "system", str, False, None, True),
            ("version", "version", str, False, None, False),
        ])
        return js


class ValueSetDefineConcept(backboneelement.BackboneElement):
    """ Concepts in the code system.
    """
    
    resource_name = "ValueSetDefineConcept"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.abstract = None
        """ If this code is not for use as a real concept.
        Type `bool`. """
        
        self.code = None
        """ Code that identifies concept.
        Type `str`. """
        
        self.concept = None
        """ Child Concepts (is-a / contains).
        List of `ValueSetDefineConcept` items (represented as `dict` in JSON). """
        
        self.definition = None
        """ Formal Definition.
        Type `str`. """
        
        self.designation = None
        """ Additional representations for the concept.
        List of `ValueSetDefineConceptDesignation` items (represented as `dict` in JSON). """
        
        self.display = None
        """ Text to Display to the user.
        Type `str`. """
        
        super(ValueSetDefineConcept, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetDefineConcept, self).elementProperties()
        js.extend([
            ("abstract", "abstract", bool, False, None, False),
            ("code", "code", str, False, None, True),
            ("concept", "concept", ValueSetDefineConcept, True, None, False),
            ("definition", "definition", str, False, None, False),
            ("designation", "designation", ValueSetDefineConceptDesignation, True, None, False),
            ("display", "display", str, False, None, False),
        ])
        return js


class ValueSetDefineConceptDesignation(backboneelement.BackboneElement):
    """ Additional representations for the concept.
    
    Additional representations for the concept - other languages, aliases,
    specialised purposes, used for particular purposes, etc.
    """
    
    resource_name = "ValueSetDefineConceptDesignation"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.language = None
        """ Language of the designation.
        Type `str`. """
        
        self.use = None
        """ Details how this designation would be used.
        Type `Coding` (represented as `dict` in JSON). """
        
        self.value = None
        """ The text value for this designation.
        Type `str`. """
        
        super(ValueSetDefineConceptDesignation, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetDefineConceptDesignation, self).elementProperties()
        js.extend([
            ("language", "language", str, False, None, False),
            ("use", "use", coding.Coding, False, None, False),
            ("value", "value", str, False, None, True),
        ])
        return js


class ValueSetExpansion(backboneelement.BackboneElement):
    """ Used when the value set is "expanded".
    
    A value set can also be "expanded", where the value set is turned into a
    simple collection of enumerated codes. This element holds the expansion, if
    it has been performed.
    """
    
    resource_name = "ValueSetExpansion"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.contains = None
        """ Codes in the value set.
        List of `ValueSetExpansionContains` items (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Uniquely identifies this expansion.
        Type `str`. """
        
        self.parameter = None
        """ Parameter that controlled the expansion process.
        List of `ValueSetExpansionParameter` items (represented as `dict` in JSON). """
        
        self.timestamp = None
        """ Time valueset expansion happened.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        super(ValueSetExpansion, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetExpansion, self).elementProperties()
        js.extend([
            ("contains", "contains", ValueSetExpansionContains, True, None, False),
            ("identifier", "identifier", str, False, None, True),
            ("parameter", "parameter", ValueSetExpansionParameter, True, None, False),
            ("timestamp", "timestamp", fhirdate.FHIRDate, False, None, True),
        ])
        return js


class ValueSetExpansionContains(backboneelement.BackboneElement):
    """ Codes in the value set.
    
    The codes that are contained in the value set expansion.
    """
    
    resource_name = "ValueSetExpansionContains"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.abstract = None
        """ If user cannot select this entry.
        Type `bool`. """
        
        self.code = None
        """ Code - if blank, this is not a choosable code.
        Type `str`. """
        
        self.contains = None
        """ Codes contained in this concept.
        List of `ValueSetExpansionContains` items (represented as `dict` in JSON). """
        
        self.display = None
        """ User display for the concept.
        Type `str`. """
        
        self.system = None
        """ System value for the code.
        Type `str`. """
        
        self.version = None
        """ Version in which this code / display is defined.
        Type `str`. """
        
        super(ValueSetExpansionContains, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetExpansionContains, self).elementProperties()
        js.extend([
            ("abstract", "abstract", bool, False, None, False),
            ("code", "code", str, False, None, False),
            ("contains", "contains", ValueSetExpansionContains, True, None, False),
            ("display", "display", str, False, None, False),
            ("system", "system", str, False, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js


class ValueSetExpansionParameter(backboneelement.BackboneElement):
    """ Parameter that controlled the expansion process.
    
    A Parameter that controlled the expansion process. These paameters may be
    used by users of expanded value sets to check whether the expansion is
    suitable for a particular purpose, or to pick the correct expansion.
    """
    
    resource_name = "ValueSetExpansionParameter"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.name = None
        """ Name as assigned by server.
        Type `str`. """
        
        self.valueBoolean = None
        """ Value of the parameter.
        Type `bool`. """
        
        self.valueCode = None
        """ Value of the parameter.
        Type `str`. """
        
        self.valueDecimal = None
        """ Value of the parameter.
        Type `float`. """
        
        self.valueInteger = None
        """ Value of the parameter.
        Type `int`. """
        
        self.valueString = None
        """ Value of the parameter.
        Type `str`. """
        
        self.valueUri = None
        """ Value of the parameter.
        Type `str`. """
        
        super(ValueSetExpansionParameter, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ValueSetExpansionParameter, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, True),
            ("valueBoolean", "valueBoolean", bool, False, "value", False),
            ("valueCode", "valueCode", str, False, "value", False),
            ("valueDecimal", "valueDecimal", float, False, "value", False),
            ("valueInteger", "valueInteger", int, False, "value", False),
            ("valueString", "valueString", str, False, "value", False),
            ("valueUri", "valueUri", str, False, "value", False),
        ])
        return js


import codeableconcept
import coding
import contactpoint
import fhirdate
import identifier
