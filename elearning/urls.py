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

admin.autodiscover()

from cours.views import CoursListView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='connexion'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='cours/cours/liste_cours.html'), name='deconnexion'),
    path('admin/', admin.site.urls),
    path('cours/', include('cours.urls', namespace='cours')),
    path('', CoursListView.as_view(), name='liste_cours'),
    path('etudiants/', include('etudiants.urls', namespace='etudiant')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
