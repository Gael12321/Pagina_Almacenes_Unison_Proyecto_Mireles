from django.contrib import admin
from django.db import models
from .models import Reporte, DetalleReporte

class DetalleReporteInline(admin.TabularInline):
    model = DetalleReporte
    extra = 1

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'fecha', 'descripcion', 'estado', 'total_gastado')
    search_fields = ('solicitante__username', 'solicitante__nombres', 'solicitante__apellidos')
    list_filter = ('estado', 'descripcion')
    inlines = [DetalleReporteInline]

class DetalleReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte', 'producto', 'cantidad', 'total_gastado')
    search_fields = ('reporte__solicitante__username', 'producto__nombre_articulo')
    list_filter = ('producto',)

admin.site.register(Reporte, ReporteAdmin)
admin.site.register(DetalleReporte, DetalleReporteAdmin)
