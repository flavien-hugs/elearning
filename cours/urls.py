# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elearning'


from django.urls import path
from . import views

app_name = 'cours'

urlpatterns = [
    path('', views.GestionCoursListView.as_view(), name='gestion_liste_cours'),
    path('create/', views.CoursCreateView.as_view(), name='cours_create'),
    path('edit/<pk>/', views.CoursUpdateView.as_view(), name='cours_edit'),
    path('delete/<pk>/', views.CoursDeleteView.as_view(), name='cours_delete'),
    path('module/<pk>/', views.CoursModuleUpdateView.as_view(), name='cours_module_update'),
    path('module/<int:module_id>/contenu/<model_name>/create/',
        views.ContenuCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/contenu/<model_name>/<id>/',
        views.ContenuCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', views.ContenuDeleteView.as_view(),
        name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContenuListView.as_view(),
        name='module_content_liste'),

    path('matiere/<slug:matiere>/', views.CoursListView.as_view(),
        name='cours_liste_matiere'),
    path('detail/<slug:slug>/', views.CoursDetailView.as_view(), name='cours_detail'),
]
