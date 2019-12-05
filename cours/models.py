# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Matieres(models.Model):
    title = models.CharField('Matière du Cours', max_length=200, unique=True)
    slug = models.SlugField('URL', max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Cours(models.Model):
    instructeur = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Matieres, on_delete=models.CASCADE)
    title = models.CharField('Titre du Cours', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    resume = models.TextField()
    date_de_creation = models.DateField('Date de création du Cours', auto_now_add=True)

    class Meta:
        ordering = ['-date_de_creation']

    def __str__(self):
        return self.title


class Modules(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    title = models.CharField('Titre du Module', max_length=200)
    description = models.TextField('Description du Cours', blank=True)

    def __str__(self):
        return self.title
