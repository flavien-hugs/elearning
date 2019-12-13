# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'

from django import forms
from django.forms.models import inlineformset_factory

from .models import Cours, Modules

ModuleFormSet = inlineformset_factory(
        Cours, Modules,
        fields=['title', 'description'],
        extra = 2, can_delete = True
    )
