from django.db import models
from usuarios.models import Usuario 
from django.db.models import Sum

# Create your models here.

class Material(models.Model):
    nombre_articulo = models.CharField('Nombre de artículo',max_length=50)
    precio_unitario = models.DecimalField('Precio unitario',max_digits=10,decimal_places=2)
    class Categoria_Material(models.TextChoices):
        ELECTRICO = 'Electrico'
        PLOMERIA = 'Plomeria'
        LIMPIEZA = 'Limpieza'
        OFICINA = 'Oficina'
    categoria = models.CharField('Categoría',max_length=10, choices=Categoria_Material.choices)
    cantidad = models.PositiveIntegerField('Cantidad', blank=True, null=True)
    imagen = models.ImageField('Imagen')
    descripcion = models.CharField('Descripción',max_length=100,blank=True, null=True)
    umbral = models.IntegerField('Umbral mínimo')
    unidades_o_paquetes = models.BooleanField('¿Se vende en unidades o paquetes?', default=True)
    cantidad_por_paquete = models.PositiveIntegerField('Cantidad por paquete', blank=True, null=True)
    class Origen_Producto(models.TextChoices):
        UNISON   = 'Unison'
        EXTERIOR = 'Exterior'
    Origen = models.CharField('Origen', max_length=8,choices = Origen_Producto.choices)

    def __str__(self):
        return self.nombre_articulo

class Gasto(models.Model):
    producto = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material", ) 
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    gasto = models.DecimalField('Gasto',max_digits=10,decimal_places=2)
    fecha = models.DateField('Fecha de gasto',auto_now=True)

    def obtener_mes_y_anio(self):
        return self.fecha.strftime('%Y-%m')

    @classmethod
    def obtener_gastos_totales_por_mes(cls):
        return cls.objects.values('fecha__year', 'fecha__month').annotate(total_gastos=models.Sum('gasto')).order_by('fecha__year', 'fecha__month')


class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    confirmado = models.BooleanField(default=False)

    def verificar_disponibilidad(self):
        return self.material.cantidad >= self.cantidad
    
    def __str__(self):
        return f"{self.material.nombre_articulo} - {self.cantidad}"