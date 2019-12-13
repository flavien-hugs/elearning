# -*- coding: utf-8 -*-

"""
__init__.py

Crée par Flavien-hugs - 2019/12/05/.
Copyright (c) 2019 unsta. All rights reserved.

"""
__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta projet elaerning'

from django.apps import apps
from django.db.models import Count
from django.core.cache import cache
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ModuleFormSet
from etudiants.forms import CoursEnrollementForm
from .models import Matieres, Cours, Modules, Contenus

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
    fields = ['matiere', 'title', 'slug', 'resume']
    success_url = reverse_lazy('cours:gestion_liste_cours')


class InstructeurCoursEditMixin(InstructeurCoursMixin, InstructeurEditMixin):
    fields = ['matiere', 'title', 'slug', 'resume']
    success_url = reverse_lazy('cours:gestion_liste_cours')
    template_name = 'cours/gestion/cours/formulaire_cours.html'


class GestionCoursListView(InstructeurCoursMixin, ListView):
    template_name = 'cours/gestion/cours/liste_cours.html'


class CoursCreateView(PermissionRequiredMixin, InstructeurCoursEditMixin, CreateView):
    permission_required = 'cours.add_cours'


class CoursUpdateView(PermissionRequiredMixin, InstructeurCoursEditMixin, UpdateView):
    permission_required = 'cours.change_cours'


class CoursDeleteView(PermissionRequiredMixin, InstructeurCoursMixin, DeleteView):
    template_name = 'cours/gestion/cours/supprimer_cours.html'
    success_url = reverse_lazy('cours:gestion_liste_cours')
    permission_required = 'cours.delete_cours'


class CoursModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'cours/gestion/module/formulaire_module.html'
    cours = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.cours, prefix='module', data=data)

    def dispatch(self, request, pk):
        self.cours = get_object_or_404(Cours, id=pk, instructeur=request.user)
        return super(CoursModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'cours': self.cours, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('cours:gestion_liste_cours')

        return self.render_to_response({'cours': self.cours, 'formset':formset})


class ContenuCreateUpdateView(TemplateResponseMixin, View):
    module = model = obj = None
    template_name = 'cours/gestion/contenu/formulaire_contenu.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='cours', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=[
            'instructeur', 'ordre',
            'date_de_creation', 'date_mise_a_jour'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Modules, id=module_id,
            cours__instructeur=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, instructeur=request.user)
        return super(ContenuCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.instructeur = request.user
            obj.save()

            if not id:
                Contenus.objects.create(module=self.module, item=obj)
            return redirect('cours:module_content_liste', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj})


class ContenuDeleteView(View):
    def post(self, request, id):
        contenu = get_object_or_404(Contenus, id=id, module__cours__instructeur=request.user)
        module = contenu.module
        contenu.item.delete()
        contenu.delete()

        return redirect('cours:module_content_liste', module.id)


class ModuleContenuListView(TemplateResponseMixin, View):
    template_name = 'cours/gestion/module/liste_contenu.html'

    def get(self, request, module_id):
        module = get_object_or_404(Modules, id=module_id,
            cours__instructeur=request.user)

        return self.render_to_response({'module': module})


class CoursListView(TemplateResponseMixin, View):
    model = Cours
    template_name = 'cours/cours/liste_cours.html'

    def get(self, request, matiere=None):
        matieres = cache.get('all_matieres')
        if not matieres:
            matieres = Matieres.objects.annotate(total_cours=Count('cours'))
            cache.set('all_matieres', matieres)

        all_cours = Cours.objects.annotate(total_modules=Count('modules'))
        if matiere:
            matiere = get_object_or_404(Matieres, slug=matiere)
            key = 'matiere_{}_cours'.format(matiere.id)
            cours = cache.get(key)
            if not cours:
                cours = all_cours.filter(matiere=matiere)
                cache.set(key, cours)
        else:
            cours = cache.get('all_cours')
            if not cours:
                cours = all_cours
                cache.set('all_cours', cours)
        return self.render_to_response({'matieres': matieres, 'matiere': matiere,
            'cours': cours})


class CoursDetailView(DetailView):
    model = Cours
    template_name = 'cours/cours/detail_cours.html'

    def get_context_data(self, **kwargs):
        context = super(CoursDetailView, self).get_context_data(**kwargs)
        context['formulaire_enrollement'] = CoursEnrollementForm(initial={'cours': self.object})
        return context
