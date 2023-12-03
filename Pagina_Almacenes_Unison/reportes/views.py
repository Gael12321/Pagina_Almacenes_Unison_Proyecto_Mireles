from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, TemplateView

from .models import Reporte
from .forms import FormularioReporte

class ListaReportes(ListView):
    model = Reporte
    template_name = 'reportes/lista_reportes.html'
    context_object_name = 'reportes'
    
class CrearReporte(CreateView):
    model = Reporte
    form_class = FormularioReporte
    template_name = 'reportes/hacer_reporte.html'
    succes_url = reverse_lazy('lista_reportes')
    
    def post(self,request,*args,**kwargs):
        form = FormularioReporte(request.POST)
        if form.is_valid():
            reporte = form.save(commit = False)
            reporte.solicitante = request.user
            reporte.save()
            return HttpResponseRedirect(reverse_lazy("lista_reportes"))

        else:
            form = FormularioReporte()
            return render(request, 'reportes/hacer_reporte', {'form':form})
        
class EliminarReporte(DeleteView):
    model = Reporte
    success_url = reverse_lazy('lista_reportes')
    template_name = 'confirmar_eliminar.html'

class BorrarTodosReportesView(View):
    template_name = 'reportes/borrar_todos_reportes.html'

    def get(self, request):
        reportes = Reporte.objects.all()
        return render(request, self.template_name, {'reportes': reportes})

    def post(self, request):
        # Borrar todos los reportes
        Reporte.objects.all().delete()
        return redirect('portal_admin')