from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView

class Portal(TemplateView):
    template_name = 'portal.html'  # Ruta relativa a la plantilla en tu directorio de plantillas

class Portal_admin(TemplateView):
    template_name = 'portal_admin.html'  # Ruta relativa a la plantilla en tu directorio de plantillas

class Portal_intendencia(TemplateView):
    template_name = 'portal_intendencia.html'  # Ruta relativa a la plantilla en tu directorio de plantillas
