# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='connexion'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='deconnexion'),
    path('admin/', admin.site.urls),
    path('', include('cours.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
