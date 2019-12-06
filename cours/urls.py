# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.urls import path

from . import views

urlpatterns = [
    path('mine/', views.GestionCoursListView.as_view(), name='manage_course_list'),
    path('create/', views.CoursCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', views.CoursUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', views.CoursDeleteView.as_view(), name='course_delete'),
]
