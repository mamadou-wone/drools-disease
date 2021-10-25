# -*- coding: utf-8 -*-
from odoo import fields, models

class Symptom(models.Model):
    _name = "smart_form.symptom"
    
    name = fields.Char(string=u"Symptôme", required=True)