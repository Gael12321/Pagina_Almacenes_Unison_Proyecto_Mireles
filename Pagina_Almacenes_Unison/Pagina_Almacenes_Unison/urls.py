"""Pagina_Almacenes_Unison URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


from .views import *
from usuarios.views import *
from materiales.views import *
from reportes.views import *

def es_admin(user):
    return user.rol == Usuario.Rol.ADMIN

def es_intendencia(user):
    return user.rol == Usuario.Rol.INTENDENCIA



urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/admin/', user_passes_test(es_admin, login_url='/portal/')(Portal_admin.as_view()), name='portal_admin'),
    path('portal/', user_passes_test(es_intendencia, login_url='/portal/')(Portal_intendencia.as_view()), name='portal_intendencia'),
    path('', RedirectView.as_view(url='portal/')),
]

urlpatterns += [
    path('iniciar-sesion/', InicioSesionView.as_view(), name='inicio_sesion'),
    path('crear-usuario/', CrearUsuario.as_view(), name='crear_usuario'),
    path('cerrar-sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),   
]

urlpatterns += [
    path('lista-materiales/', login_required(ListaMateriales.as_view()), name='lista_materiales'),
    path('gastos/', login_required(ListaGastos.as_view()), name='lista_gastos'),
    path('añadir-material/', login_required(AñadirMaterial.as_view()), name='añadir_material'),
    path('agregar-material/<int:pk>/', login_required(AgregarProducto.as_view()), name='agregar_material'),
    path('editar-material/<int:pk>/', login_required(EditarMaterial.as_view()), name='editar_material'),
    path('tomar-material/<int:pk>/', login_required(TomarProductoView.as_view()), name='tomar_producto'),
    path('eliminar-material/<int:pk>/', login_required(EliminarMaterial.as_view()), name = 'eliminar_material'),
    path('ver-material/<int:pk>/', VerProducto.as_view(), name='ver_producto'),
    path('agregar-al-carrito/<int:pk>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('confirmar-pedido/', confirmar_pedido, name='confirmar_pedido'),
    path('ver-carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar-del-carrito/<int:pk>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('borrar-carrito/', borrar_carrito, name='borrar_carrito'),
    path('agregar-al-carrito-bulk/', agregar_al_carrito_bulk, name='agregar_al_carrito_bulk'),

]

urlpatterns += [
    path('lista-reportes/', login_required(ListaReportes.as_view()), name='lista_reportes'),
    path('añadir-reporte/', login_required(CrearReporte.as_view()), name='hacer_reporte'),
    path('eliminar-reporte/<int:pk>/', login_required(EliminarReporte.as_view()), name = 'eliminar_reporte'),
    path('borrar-todos-reportes/', BorrarTodosReportesView.as_view(), name='borrar_todos_reportes'),   
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
