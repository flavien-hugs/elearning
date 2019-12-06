# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'


from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Cours

# Create your views here.

class InstructeurMixin(object):
    def get_queryset(self):
        queryset = super(InstructeurMixin, self).get_queryset()
        return queryset.filter(instructeur=self.request.user)

class InstructeurEditMixin(object):
    def form_valid(self, form):
        form.instance.instructeur= self.request.user
        return super(InstructeurEditMixin, self).form_valid(form)

class InstructeurCoursMixin(InstructeurMixin, LoginRequiredMixin):
    model = Cours
    fields = ['theme', 'title', 'slug', 'resume']
    success_url = reverse_lazy('gestion_liste_cours')

class InstructeurCoursEditMixin(InstructeurCoursMixin, InstructeurEditMixin):
    fields = ['theme', 'title', 'slug', 'resume']
    success_url = reverse_lazy('gestion_liste_cours')
    template_name = 'cours/gestion/cours/formulaire_cours.html'

class GestionCoursListView(InstructeurCoursMixin, ListView):
    template_name = 'cours/gestion/cours/liste_cours.html'

class CoursCreateView(PermissionRequiredMixin, InstructeurCoursEditMixin, CreateView):
    permission_required = 'cours.add_cours'

class CoursUpdateView(PermissionRequiredMixin, InstructeurCoursEditMixin, UpdateView):
    permission_required = 'cours.change_cours'

class CoursDeleteView(PermissionRequiredMixin, InstructeurCoursMixin, DeleteView):
    template_name = 'cours/gestion/cours/supprimer_cours.html'
    success_url = reverse_lazy('gestion_liste_cours')
    permission_required = 'cours.delete_cours'
