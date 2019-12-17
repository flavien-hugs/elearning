# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elearning'

import dj_database_url
from elearning.settings import *

DEBUG = TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]
#  Add configuration for static files storage using whitenoise

ALLOWED_HOSTS = ['elear.herokuapp.com']

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
