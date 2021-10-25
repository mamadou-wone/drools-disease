# -*- coding: utf-8 -*-
from odoo import fields, models, api

class Disease(models.Model):
    _name = "smart_form.disease"
    
    name = fields.Char(string="Maladie")
    score = fields.Char(string="Score")
    
    