# -*- coding: utf-8 -*-

class Diagnostic():
    def __init__(self, symptoms=[], diseases=[], age=None, profession=None, observation=None):
        self.age = age
        self.symptoms = symptoms
        self.diseases = diseases
        self.profession = profession
        self.observation = observation
