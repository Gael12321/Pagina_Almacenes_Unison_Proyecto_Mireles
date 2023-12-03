from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView, TemplateView, View

from .models import Gasto, Material, Carrito
from reportes.models import Reporte, DetalleReporte
from .forms import FormularioAgregarProducto, FormularioMaterial, FormularioTomarProducto, FormularioAgregarAlCarrito




class ListaMateriales(ListView):
    model = Material
    template_name = 'materiales/lista_material.html'
    context_object_name = 'materiales'
    
class AñadirMaterial(CreateView):
    model = Material
    form_class = FormularioMaterial
    template_name = 'materiales/añadir_material.html'
    succes_url = reverse_lazy('lista_materiales')
    
    def post(self,request,*args,**kwargs):
        form = FormularioMaterial(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit = False)
            material.save()
            
            Gasto.objects.create(producto=material, cantidad= material.cantidad, gasto=(material.precio_unitario * material.cantidad))
            return HttpResponseRedirect(reverse_lazy("lista_materiales"))
                

        else:
            form = FormularioMaterial(request.POST, request.FILES)
            return render(request, 'materiales/añadir_material.html', {'form':form})

class EditarMaterial(UpdateView):
    model = Material
    template_name = 'materiales/editar_material.html'
    form_class = FormularioMaterial
    success_url = reverse_lazy('lista_materiales')

class AgregarProducto(FormView):
    template_name = 'materiales/agregar_producto.html'
    form_class = FormularioAgregarProducto
    success_url = reverse_lazy('lista_materiales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = get_object_or_404(Material, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # Get the material and update its quantity
        material = self.get_context_data()['material']
        cantidad_a_agregar = form.cleaned_data['cantidad_a_agregar']
        material.cantidad += cantidad_a_agregar
        material.save()

        Gasto.objects.create(
            producto=material,
            cantidad=cantidad_a_agregar,
            gasto=(material.precio_unitario * cantidad_a_agregar),
        )

        return super().form_valid(form)
    
class TomarProductoView(TemplateView):  # Cambia a TemplateView para manejar solicitudes GET
    template_name = 'materiales/tomar_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = get_object_or_404(Material, pk=self.kwargs['pk'])
        context['form'] = FormularioTomarProducto()
        return context

    def post(self, request, *args, **kwargs):
        form = FormularioTomarProducto(request.POST)
        if form.is_valid():
            material = get_object_or_404(Material, pk=self.kwargs['pk'])
            cantidad_deseada = form.cleaned_data['cantidad_a_tomar']

            if cantidad_deseada < 0:
                form.add_error('cantidad_a_tomar', 'La cantidad a tomar no puede ser negativa.')
                return self.render_to_response(self.get_context_data(form=form))

            if cantidad_deseada <= material.cantidad:
                material.cantidad -= cantidad_deseada
                material.save()

                if material.cantidad <= material.umbral:
                    Reporte.objects.create(
                        solicitante=self.request.user,
                        producto=material,
                        cantidad=cantidad_deseada,
                        descripcion='Quedan pocos artículos',
                    )
                return HttpResponseRedirect(reverse_lazy('lista_materiales') + '?taken=true')
            else:
                form.add_error('cantidad_a_tomar', 'La cantidad deseada es mayor a la cantidad disponible.')

        return self.render_to_response(self.get_context_data(form=form))
    
class EliminarMaterial(DeleteView):
    model = Material
    success_url = reverse_lazy('lista_materiales')
    template_name = 'confirmar_eliminar.html'
        
class ListaGastos(ListView):
    model = Gasto
    template_name = 'materiales/lista_gastos.html'
    context_object_name = 'gastos'
    
class VerProducto(DetailView):
    model = Material
    template_name = 'materiales/ver_producto.html'  # Cambia al nombre correcto de tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar más contexto según sea necesario
        return context 
    
class AgregarAlCarritoView(View):
    def post(self, request, pk):
        # Obtén el material
        material = get_object_or_404(Material, pk=pk)

        # Obtén la cantidad a agregar del formulario
        cantidad_a_agregar = int(request.POST.get('cantidad_a_agregar', 1))

        # Verifica si el material ya está en el carrito para el usuario actual y no está confirmado
        carrito_item = Carrito.objects.filter(usuario=request.user, material=material, confirmado=False).first()

        if carrito_item:
            # Si el material ya está en el carrito, simplemente actualiza la cantidad
            carrito_item.cantidad += cantidad_a_agregar
            carrito_item.save()
        else:
            # Si el material no está en el carrito, crea un nuevo objeto Carrito
            Carrito.objects.create(usuario=request.user, material=material, cantidad=cantidad_a_agregar, confirmado=False)

        # Mensaje de éxito
        return redirect('lista_materiales' + '?taken=true')
    
def confirmar_pedido(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)

    # Crear un objeto Reporte
    reporte = Reporte.objects.create(
        solicitante=request.user,
        estado=Reporte.EstadoSolicitud.PENDIENTE,
    )

    for item in carrito_items:
        if not item.verificar_disponibilidad():
            # Manejar el error, por ejemplo, redireccionar a una página de error.
            return render(request, 'materiales/error_disponibilidad.html')

        # Reducir la cantidad en el modelo Material
        item.material.cantidad -= item.cantidad
        item.material.save()

        # Crear un objeto DetalleReporte para cada material individual
        DetalleReporte.objects.create(
            reporte=reporte,
            producto=item.material,
            cantidad=item.cantidad,
        )

        # Marcar el elemento del carrito como confirmado
        item.confirmado = True
        item.save()

    # Eliminar elementos confirmados del carrito
    carrito_items.filter(confirmado=True).delete()

    return redirect('ver_carrito')
    
def ver_carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user, confirmado=False)
    total_items = carrito_items.count()

    context = {
        'carrito_items': carrito_items,
        'total_items': total_items,
    }

    return render(request, 'materiales/ver_carrito.html', context)  

def eliminar_del_carrito(request, pk):
    item = Carrito.objects.get(pk=pk)
    item.delete()
    return redirect('ver_carrito')

def borrar_carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    carrito_items.delete()
    return redirect('ver_carrito')


def agregar_al_carrito_bulk(request):
    if request.method == 'POST':
        cantidades = request.POST.getlist('cantidades[]')
        materiales_ids = request.POST.getlist('materiales[]')

        for cantidad, material_id in zip(cantidades, materiales_ids):
            cantidad = int(cantidad)
            material = Material.objects.get(pk=material_id)

            if cantidad > 0:
                Carrito.objects.create(usuario=request.user, material=material, cantidad=cantidad)

    return redirect('lista_materiales')