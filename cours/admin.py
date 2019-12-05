# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.contrib import admin
from .models import Matieres, Cours, Modules

# Register your models here.

@admin.register(Matieres)
class MatieresAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class ModulesAdmin(admin.StackedInline):
    model = Modules


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_de_creation'
    ordering = ('theme', 'title')
    list_display = ['title', 'theme', 'date_de_creation']
    list_filter = ('date_de_creation', 'theme')
    search_fields = ('title', 'resume')
    prepopulated_fields = {'slug', ('title',)}
    inlines = [ ModulesAdmin]
