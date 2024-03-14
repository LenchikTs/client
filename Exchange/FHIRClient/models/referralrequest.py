#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 (http://hl7.org/fhir/StructureDefinition/ReferralRequest) on 2016-03-29.
#  2016, SMART Health IT.


import domainresource

class ReferralRequest(domainresource.DomainResource):
    """ A request for referral or transfer of care.
    
    Used to record and send details about a request for referral service or
    transfer of a patient to the care of another provider or provider
    organisation.
    """
    
    resource_name = "ReferralRequest"
    
    def __init__(self, jsondict=None):
        """ Initialize all valid properties.
        """
        
        self.dateSent = None
        """ Date referral/transfer of care request is sent.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.description = None
        """ A textual description of the referral.
        Type `str`. """
        
        self.encounter = None
        """ Encounter.
        Type `FHIRReference` referencing `Encounter` (represented as `dict` in JSON). """
        
        self.fulfillmentTime = None
        """ Requested service(s) fulfillment time.
        Type `Period` (represented as `dict` in JSON). """
        
        self.identifier = None
        """ Identifier of request.
        List of `Identifier` items (represented as `dict` in JSON). """
        
        self.patient = None
        """ Patient referred to care or transfer.
        Type `FHIRReference` referencing `Patient` (represented as `dict` in JSON). """
        
        self.priority = None
        """ Urgency of referral / transfer of care request.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.reason = None
        """ Reason for referral / Transfer of care request.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.recipient = None
        """ Receiver of referral / transfer of care request.
        List of `FHIRReference` items referencing `Practitioner, Organization` (represented as `dict` in JSON). """
        
        self.requester = None
        """ Requester of referral / transfer of care.
        Type `FHIRReference` referencing `Practitioner, Organization, Patient` (represented as `dict` in JSON). """
        
        self.serviceRequested = None
        """ Service(s) requested.
        List of `CodeableConcept` items (represented as `dict` in JSON). """
        
        self.specialty = None
        """ The clinical specialty (discipline) that the referral is requested
        for.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.status = None
        """ draft | requested | active | cancelled | accepted | rejected |
        completed.
        Type `str`. """
        
        self.supportingInformation = None
        """ Additonal information to support referral or transfer of care
        request.
        List of `FHIRReference` items referencing `Resource` (represented as `dict` in JSON). """
        
        self.type = None
        """ Referral/Transition of care request type.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        super(ReferralRequest, self).__init__(jsondict)
    
    def elementProperties(self):
        js = super(ReferralRequest, self).elementProperties()
        js.extend([
            ("dateSent", "dateSent", fhirdate.FHIRDate, False, None, False),
            ("description", "description", str, False, None, False),
            ("encounter", "encounter", fhirreference.FHIRReference, False, None, False),
            ("fulfillmentTime", "fulfillmentTime", period.Period, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("patient", "patient", fhirreference.FHIRReference, False, None, False),
            ("priority", "priority", codeableconcept.CodeableConcept, False, None, False),
            ("reason", "reason", codeableconcept.CodeableConcept, False, None, False),
            ("recipient", "recipient", fhirreference.FHIRReference, True, None, False),
            ("requester", "requester", fhirreference.FHIRReference, False, None, False),
            ("serviceRequested", "serviceRequested", codeableconcept.CodeableConcept, True, None, False),
            ("specialty", "specialty", codeableconcept.CodeableConcept, False, None, False),
            ("status", "status", str, False, None, True),
            ("supportingInformation", "supportingInformation", fhirreference.FHIRReference, True, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
        ])
        return js


import codeableconcept
import fhirdate
import fhirreference
import identifier
import period
