# -*- coding: utf-8 -*-

class Diagnostic():
    def __init__(self, symptoms=[], diseases=[], age=None):
        self.age = age
        self.symptoms = symptoms
        self.diseases = diseases
