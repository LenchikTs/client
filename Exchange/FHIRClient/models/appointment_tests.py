#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 0.5.0.5149 on 2016-03-29.
#  2016, SMART Health IT.


import os
import io
import unittest
import json
import appointment
from .fhirdate import FHIRDate


class AppointmentTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Appointment", js["resourceType"])
        return appointment.Appointment(js)
    
    def testAppointment1(self):
        inst = self.instantiate_from("appointment-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Appointment instance")
        self.implAppointment1(inst)
        
        js = inst.as_json()
        self.assertEqual("Appointment", js["resourceType"])
        inst2 = appointment.Appointment(js)
        self.implAppointment1(inst2)
    
    def implAppointment1(self, inst):
        self.assertEqual(inst.comment, "Further expand on the results of the MRI and determine the next actions that may be appropriate.")
        self.assertEqual(inst.description, "Discussion on the results of your recent MRI")
        self.assertEqual(inst.end.date, FHIRDate("2013-12-10T11:00:00Z").date)
        self.assertEqual(inst.end.as_json(), "2013-12-10T11:00:00Z")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.participant[0].required, "required")
        self.assertEqual(inst.participant[0].status, "accepted")
        self.assertEqual(inst.participant[1].required, "required")
        self.assertEqual(inst.participant[1].status, "accepted")
        self.assertEqual(inst.participant[1].type[0].coding[0].code, "attending")
        self.assertEqual(inst.participant[2].required, "required")
        self.assertEqual(inst.participant[2].status, "accepted")
        self.assertEqual(inst.priority, 5)
        self.assertEqual(inst.start.date, FHIRDate("2013-12-10T09:00:00Z").date)
        self.assertEqual(inst.start.as_json(), "2013-12-10T09:00:00Z")
        self.assertEqual(inst.status, "booked")
        self.assertEqual(inst.text.div, "<div>Brian MRI results discussion</div>")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "52")
        self.assertEqual(inst.type.coding[0].display, "General Discussion")
    
    def testAppointment2(self):
        inst = self.instantiate_from("appointment-example2doctors.json")
        self.assertIsNotNone(inst, "Must have instantiated a Appointment instance")
        self.implAppointment2(inst)
        
        js = inst.as_json()
        self.assertEqual("Appointment", js["resourceType"])
        inst2 = appointment.Appointment(js)
        self.implAppointment2(inst2)
    
    def implAppointment2(self, inst):
        self.assertEqual(inst.comment, "Clarify the results of the MRI to ensure context of test was correct")
        self.assertEqual(inst.description, "Discussion about Peter Chalmers MRI results")
        self.assertEqual(inst.end.date, FHIRDate("2013-12-09T11:00:00Z").date)
        self.assertEqual(inst.end.as_json(), "2013-12-09T11:00:00Z")
        self.assertEqual(inst.id, "2docs")
        self.assertEqual(inst.participant[0].required, "information-only")
        self.assertEqual(inst.participant[0].status, "accepted")
        self.assertEqual(inst.participant[1].required, "required")
        self.assertEqual(inst.participant[1].status, "accepted")
        self.assertEqual(inst.participant[2].required, "required")
        self.assertEqual(inst.participant[2].status, "accepted")
        self.assertEqual(inst.participant[3].required, "information-only")
        self.assertEqual(inst.participant[3].status, "accepted")
        self.assertEqual(inst.priority, 5)
        self.assertEqual(inst.start.date, FHIRDate("2013-12-09T09:00:00Z").date)
        self.assertEqual(inst.start.as_json(), "2013-12-09T09:00:00Z")
        self.assertEqual(inst.status, "booked")
        self.assertEqual(inst.text.div, "<div>Brian MRI results discussion</div>")
        self.assertEqual(inst.text.status, "generated")
        self.assertEqual(inst.type.coding[0].code, "52")
        self.assertEqual(inst.type.coding[0].display, "General Discussion")

