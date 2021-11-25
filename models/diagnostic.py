# -*- coding: utf-8 -*-
from odoo import fields, models, api
import os
from dotenv import load_dotenv
load_dotenv()
from ..utils import *

from datetime import datetime
from python_drools_sdk.commands.insert_elements_command import InsertElementsCommand
from python_drools_sdk.commands.insert_object_command import InsertObjectCommand
from python_drools_sdk.kie.drools import Drools
from python_drools_sdk.utils import helpers
from python_drools_sdk.exceptions.drools_exception import DroolsException


Drools.KIE_SERVER_CONTAINER_PACKAGE = os.getenv('KIE_SERVER_CONTAINER_PACKAGE') 
Drools.KIE_SERVER_USERNAME = os.getenv('KIE_SERVER_USERNAME') 
Drools.KIE_SERVER_PASSWORD = os.getenv('KIE_SERVER_PASSWORD') 
Drools.KIE_SERVER_ROOT_URL = os.getenv('KIE_SERVER_ROOT_URL')  
Drools.KIE_SERVER_CONTAINER_ID = os.getenv('KIE_SERVER_CONTAINER_ID')  
Drools.KIE_SESSION_NAME = os.getenv('KIE_SESSION_NAME') 
class Diagnostic(models.Model):
    _name = 'smart_form.diagnostic'
    
    
    name = fields.Char(string=u"Référence de la consultation")
    patient_last_name = fields.Char(string="Nom", required=True)
    patient_first_name = fields.Char(string=u"Prénom", required=True)
    patient_address = fields.Char(string="Adresse", required=True)
    patient_phone_number = fields.Char(string=u"Numéro de téléphone")
    patient_age = fields.Integer(string="Âge", required=True)
    symptom_ids = fields.Many2many('smart_form.symptom', string=u"Symptômes", required=True)
    diagnostic_date = fields.Datetime(string=u'Date de la consultation', readonly=True, default=fields.Datetime.now())
    disease_ids = fields.Many2many("smart_form.disease", string="Maladies", readonly=True)
    
    def get_diagnostic(self):
        symptoms_list = []
        diagnostics = []
        for record in self:
            for symtom in record.symptom_ids:
                name = symtom.name
                symptoms_list.append(name)
                
        if len(symptoms_list) > 0:
            diagnostics = [diagnostic.Diagnostic(age=self.patient_age, symptoms=[item]) for item in symptoms_list]
                    
            insert_elements_command = InsertElementsCommand(objects=diagnostics, out_identifier='decision').initialize()

            Drools.add_command(insert_elements_command)

            try:
                response = Drools.execute_commands()
            except DroolsException as de:
                print(de)
                
            drools_diagnostic_response = response['decision']
        
            if len(drools_diagnostic_response) > len(symptoms_list):
                for item in drools_diagnostic_response:
                    if item["symptoms"][0] not in symptoms_list:
                        print(item["symptoms"][0])
                        print(drools_diagnostic_response.index(item))
                        drools_diagnostic_response.pop(drools_diagnostic_response.index(item))
            
            print(drools_diagnostic_response)
            diseases = [data["diseases"] for data in drools_diagnostic_response]
            min_length = min([len(data["diseases"]) for data in drools_diagnostic_response])
            
            result = []
            score = []
            for item in diseases:
                for i in range(min_length):
                    result.append(item[i].split(",")[0])
                    score.append(item[i].split(",")[1])
            
            other_disease = []      
            other_score = []   
            for item in diseases:
                for i in range(min_length ,len(item)):
                    other_disease.append(item[i].split(",")[0])
                    other_score.append(item[i].split(",")[1])  

            result = result + other_disease
            score = score + other_score
            
            final_score = []
            final_list = []
            for d in range(len(result)):
                if result[d] not in final_list:
                    final_score.append(score[d])
                    final_list.append(result[d])
                else:
                    final_score[final_list.index(result[d])] = int(final_score[final_list.index(result[d])]) + int(score[d])

            diseases = [self.env["smart_form.disease"].create({"name": final_list[item], "score": final_score[item]}) for item in range(len(final_list))]
            self.disease_ids = [(6, 0, [disease.id for disease in diseases])]  
        else:
            self.disease_ids = [(6, 0, [])]   
