from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombres', 'apellidos', 'rol', 'edificio', 'piso', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'nombres', 'apellidos')
    list_filter = ('is_active', 'is_staff', 'rol')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'rol')}),
        ('Ubicación', {'fields': ('edificio', 'piso')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombres', 'apellidos', 'rol', 'edificio', 'piso', 'password1', 'password2'),
        }),
    )
    ordering = ('nombres',)

admin.site.register(Usuario, UsuarioAdmin)
