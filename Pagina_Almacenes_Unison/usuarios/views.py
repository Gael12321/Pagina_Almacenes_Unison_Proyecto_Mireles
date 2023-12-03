from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static



from .models import *
from .forms import *
# Create your views here.

class CrearUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    url_redirect = reverse_lazy('inicio_sesion')

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse_lazy("inicio_sesion"))
        else:
            return render(request, self.template_name, context={'form': form})


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
