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
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .champs import ChampsPerso

# Create your models here.

class Matieres(models.Model):
    title = models.CharField('Matière du Cours', max_length=200, unique=True)
    slug = models.SlugField('URL', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Matière'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cours:cours_liste_matiere', args=[self.slug])


class Cours(models.Model):
    instructeur = models.ForeignKey(User, on_delete=models.CASCADE)
    etudiants = models.ManyToManyField(User, related_name='rejoindre_cours', blank=True)
    matiere = models.ForeignKey(Matieres, related_name='cours', on_delete=models.CASCADE)
    title = models.CharField('Titre du Cours', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    resume = models.TextField()
    date_de_creation = models.DateField('Date de création du Cours', auto_now_add=True)

    class Meta:
        verbose_name = 'Cours'
        ordering = ['-date_de_creation']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cours:cours_detail', args=[self.slug])


class Modules(models.Model):
    cours = models.ForeignKey(Cours, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField('Titre du Module', max_length=200)
    description = models.TextField('Description du Cours', blank=True)
    ordre = ChampsPerso(blank=True, for_fields={'cours'})

    class Meta:
        verbose_name = 'Module'
        ordering = ['ordre']

    def __str__(self):
        return '{}. {}'.format(self.ordre, self.title)

    def get_absolute_url(self):
        return reverse('cours:module_content_liste', args=[self.id])


class Contenus(models.Model):
    module = models.ForeignKey(Modules, related_name='contenus', on_delete=models.CASCADE)
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
    ordre = ChampsPerso(blank=True, for_fields=['module'])

    class Meta:
        verbose_name = 'Contenu'
        ordering = ['ordre']


class TypeContenu(models.Model):
    instructeur = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField('Titre du contenu', max_length=250)
    date_de_creation = models.DateTimeField('Date de création', auto_now_add=True)
    date_mise_a_jour = models.DateTimeField('Date de mise en ligne', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('cours/contenu/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(TypeContenu):
    contenu = models.TextField('Description du contenu')


class File(TypeContenu):
    file = models.FileField('Ajouter un fichier', upload_to='fichier')


class Image(TypeContenu):
    file = models.FileField('Ajouter une image', upload_to='images')


class Video(TypeContenu):
    video_url = models.URLField("Ajouter l'url de la video")
