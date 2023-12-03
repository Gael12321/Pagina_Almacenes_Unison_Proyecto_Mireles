from django.db import models
from usuarios.models import Usuario
from materiales.models import Material

# Create your models here.

class Reporte(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Solicitante")
    fecha = models.DateField("Fecha de solicitud", auto_now_add=True)

    class Descripcion(models.TextChoices):
        PRODUCTO_ACABADO = 'Ya no hay artículos'
        PRODUCTO_ESCASO = 'Quedan pocos artículos'
    descripcion = models.CharField("Descripción", max_length=22,  choices=Descripcion.choices, default='Quedan pocos artículos')

    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = 'Pendiente'
        COMPLETADO = 'Completado'
    estado = models.CharField('Estado de solicitud', max_length=10, choices=EstadoSolicitud.choices, default='Pendiente')

    detalles = models.ManyToManyField(Material, through='DetalleReporte')

    def __str__(self):
        return f"Reporte de solicitud por {self.solicitante.nombres} {self.solicitante.apellidos} el {self.fecha}"

class DetalleReporte(models.Model):
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, verbose_name="Reporte")
    producto = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Material")
    cantidad = models.IntegerField("Cantidad")

    def __str__(self):
        return f"{self.cantidad} artículos pedidos de: {self.producto.nombre_articulo} en el reporte {self.reporte}"