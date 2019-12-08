# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views

app_name = 'etudiant'

urlpatterns = [
    path('register/', views.EtudiantRegistrationView.as_view(),
        name='etudiant_registration'),
    path('enrollement/', views.EtudiantEnrollementCoursView.as_view(),
        name='etudiant_enrollement_cours'),
    path('cours/', views.EtudiantCoursListView.as_view(),
        name='etudiant_liste_cours'),
    path('cours/<pk>/', cache_page(60*15)(views.EtudiantCoursDetailView.as_view()),
        name='etudiant_detail_cours'),
    path('cours/<pk>/<module_id>/', cache_page(60*15)(views.EtudiantCoursDetailView.as_view()),
        name='etudiant_detail_cours_module'),
]
