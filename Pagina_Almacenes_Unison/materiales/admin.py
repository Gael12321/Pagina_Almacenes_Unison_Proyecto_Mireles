from django.contrib import admin
from .models import Material, Gasto, Carrito
from usuarios.models import Usuario

class CarritoInline(admin.TabularInline):
    model = Carrito

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre_articulo', 'precio_unitario', 'categoria', 'cantidad', 'umbral', 'unidades_o_paquetes', 'cantidad_por_paquete', 'Origen')
    search_fields = ('nombre_articulo', 'categoria', 'Origen')
    list_filter = ('categoria', 'Origen')
    inlines = [CarritoInline]

class GastoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'gasto', 'fecha', 'obtener_mes_y_anio')
    search_fields = ('producto__nombre_articulo',)
    list_filter = ('fecha',)

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'material', 'cantidad', 'confirmado', 'verificar_disponibilidad')
    search_fields = ('usuario__username', 'material__nombre_articulo')
    list_filter = ('confirmado',)
    actions = ['marcar_confirmado']

    def marcar_confirmado(self, request, queryset):
        queryset.update(confirmado=True)

    marcar_confirmado.short_description = "Marcar como confirmado"

admin.site.register(Material, MaterialAdmin)
admin.site.register(Gasto, GastoAdmin)
admin.site.register(Carrito, CarritoAdmin)
