# -*- coding: utf-8 -*-
from odoo import fields, models, api
from ..utils import *

from datetime import datetime
from python_drools_sdk.commands.insert_elements_command import InsertElementsCommand
from python_drools_sdk.commands.insert_object_command import InsertObjectCommand
from python_drools_sdk.kie.drools import Drools
from python_drools_sdk.utils import helpers
from python_drools_sdk.exceptions.drools_exception import DroolsException

Drools.KIE_SERVER_CONTAINER_PACKAGE = 'com.myspace.ministere' 
Drools.KIE_SERVER_USERNAME = 'admin'
Drools.KIE_SERVER_PASSWORD = 'admin'
Drools.KIE_SERVER_ROOT_URL = 'http://172.17.0.1:8180'
Drools.KIE_SERVER_CONTAINER_ID = 'ministere_1.0.0-SNAPSHOT' 

class Diagnostic(models.Model):
    _name = 'smart_form.diagnostic'
    
    name = fields.Char(string=u"Référence de la consultation")
    patient_last_name = fields.Char(string="Nom", required=True)
    patient_first_name = fields.Char(string=u"Prénom", required=True)
    patient_address = fields.Char(string="Adresse", required=True)
    patient_age = fields.Integer(string="Âge", required=True)
    symptom_ids = fields.Many2many('smart_form.symptom', string=u"Symptômes", required=True)
    diagnostic_date = fields.Datetime(string=u'Date de la consultation', readonly=True, default=fields.Datetime.now())
    disease_ids = fields.Many2many("smart_form.disease", string="Maladies", readonly=True)
    
    def get_diagnostic(self):
        symptomsList = []
        for record in self:
            for symtom in record.symptom_ids:
                name = symtom.name
                symptoms = symptom.Symptom("-".join(name.split(" ")))
                symptomsList.append(symptoms.name)
        # symptomsList = ",".join(symptomsList)        
        decision = diagnostic.Diagnostic(symptoms=symptomsList)
        insert_command = InsertObjectCommand(object=decision, out_identifier="decision").initialize()
        Drools.add_command(insert_command)     
        try:
            response = Drools.execute_commands()
        except DroolsException as de:
            print(de)

        drools_diagnostic_response = response['decision']
        diseases = [self.env["smart_form.disease"].create({"name": item.split(",")[0], "score": item.split(",")[1]}) for item in drools_diagnostic_response['diseases']]
        self.disease_ids = [(6, 0, [disease.id for disease in diseases])]    