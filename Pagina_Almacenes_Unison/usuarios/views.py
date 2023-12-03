from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.contrib import messages



from .models import *
from .forms import *
# Create your views here.

class CrearUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    url_redirect = reverse_lazy('inicio_sesion')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Usuario {form.instance.username} creado correctamente')
        return response

    def get_success_url(self):
        return reverse('portal_admin')

class InicioSesionView(LoginView):
    template_name = 'iniciar_sesion.html'
    authentication_form = FormularioLogin

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.get_user()

        if user.rol == Usuario.Rol.ADMIN:
            return HttpResponseRedirect(reverse('portal_admin'))
        elif user.rol == Usuario.Rol.INTENDENCIA:
            return HttpResponseRedirect(reverse('portal_intendencia'))

class CerrarSesionView(LogoutView):
    next_page = reverse_lazy ('inicio_sesion')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ListaUsuario(ListView):
    model = Usuario
    template_name = 'lista_usuario.html'
    context_object_name = 'usuarios'

class VerUsuario(UpdateView, DetailView):
    model = Usuario
    template_name = 'ver_usuarios.html'
    context_object_name = 'usuario'
    fields = ['username', 'email', 'nombres', 'apellidos', 'rol', 'edificio', 'piso']
    success_url = reverse_lazy('lista_usuario')

class EditarUsuario(UpdateView):
    model = Usuario
    template_name = 'editar_usuario.html'
    fields = ['username', 'email', 'nombres', 'apellidos', 'rol', 'edificio', 'piso']
    success_url = reverse_lazy('lista_usuario')

class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = 'eliminar_usuario_confirmar.html'  # You can create this template
    success_url = reverse_lazy('lista_usuario')
