# Generated by Django 4.2.1 on 2023-12-03 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0011_alter_carrito_cantidad_alter_material_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='cantidad_por_paquete',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad por paquete'),
        ),
        migrations.AddField(
            model_name='material',
            name='unidad_de_medida',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Unidad de medida'),
        ),
        migrations.AddField(
            model_name='material',
            name='unidades_o_paquetes',
            field=models.BooleanField(default=True, verbose_name='¿Se vende en unidades o paquetes?'),
        ),
    ]
