# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elearning'


from django import template
from django.db.models import Count

from ..models import Cours

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.inclusion_tag('cours/cours/latest_cours.html')
def show_latest_cours(count=4):
    latest_cours = Cours.objects.filter(date_de_creation__isnull=False).order_by('-date_de_creation')[:count]
    context = { 'latest_cours': latest_cours }
    return context
