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
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from cours.models import Cours, Modules, Matieres
from .forms import CoursEnrollementForm


# Create your views here.


class EtudiantRegistrationView(CreateView):
    template_name = 'etudiants/etudiant/registration_etudiant.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('etudiant:etudiant_cours_liste')

    def form_valid(self, form):
        result = super(EtudiantRegistrationView, self).form_valid(form)
        cdata = form.cleaned_data
        user = authenticate(username=cdata['username'], password=cdata['password1'])
        login(self.request, user)
        return result


class EtudiantEnrollementCoursView(LoginRequiredMixin, FormView):
    cours = None
    form_class = CoursEnrollementForm

    def form_valid(self, form):
        self.cours = form.cleaned_data['cours']
        self.cours.etudiants.add(self.request.user)
        return super(EtudiantEnrollementCoursView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('etudiant:etudiant_detail_cours', args=[self.cours.id])



# Vue permettent aux étudiants de lister les cours auxquels
# ils sont inscrits
class EtudiantCoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = 'etudiants/cours/etudiant_liste_cours.html'

    def get_queryset(self):
        queryset = super(EtudiantCoursListView, self).get_queryset()
        return queryset.filter(etudiants__in=[self.request.user])


class EtudiantCoursDetailView(DetailView):
    model = Cours
    template_name = 'etudiants/cours/etudiant_detail_cours.html'

    def get_queryset(self):
        queryset = super(EtudiantCoursDetailView, self).get_queryset()
        return queryset.filter(etudiants__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(EtudiantCoursDetailView, self).get_context_data(**kwargs)
        # obtenir les objets du cours
        cours = self.get_object()
        # obtenir le module courant
        if 'module_id' in self.kwargs:
            context['module'] = cours.modules.get(id=self.kwargs['module_id'])
        else:
            # obtenir le premier module
            context['module'] = cours.modules.all()[0]
        return context
