# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elearning'


from django import forms
from cours.models import Cours

class CoursEnrollementForm(forms.Form):
    cours = forms.ModelChoiceField(
        queryset=Cours.objects.all(), widget=forms.HiddenInput)
