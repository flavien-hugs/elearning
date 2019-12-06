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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Matieres(models.Model):
    title = models.CharField('Matière du Cours', max_length=200, unique=True)
    slug = models.SlugField('URL', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Matière'
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
        verbose_name = 'Cours'
        ordering = ['-date_de_creation']

    def __str__(self):
        return self.title


class Modules(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    title = models.CharField('Titre du Module', max_length=200)
    description = models.TextField('Description du Cours', blank=True)

    class Meta:
        verbose_name = 'Module'

    def __str__(self):
        return self.title


class Contenus(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    content_types = models.ForeignKey(ContentType, on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':(
                'ContenuText',
                'ContenuFichier',
                'ContenuImage',
                'ContenuVideo'
            )
        }
    )
    identifiant = models.PositiveIntegerField()
    item = GenericForeignKey('content_types', 'identifiant')


class TypeContenu(models.Model):
    instructeur = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField('Titre du contenu', max_length=250)
    date_de_creation = models.DateTimeField('Date de création', auto_now_add=True)
    date_mise_a_jour = models.DateTimeField('Date de mise en ligne', auto_now_add=True)


    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class ContenuText(TypeContenu):
    contenu = models.TextField('Description du contenu')


class ContenuFichier(TypeContenu):
    fichier = models.FileField('Ajouter un fichier', upload_to='fichier')


class ContenuImage(TypeContenu):
    image = models.FileField('Ajouter une image', upload_to='images')


class ContenuVideo(TypeContenu):
    video_url = models.URLField()
