# Generated by Django 4.2.1 on 2023-12-03 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0012_material_cantidad_por_paquete_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='unidad_de_medida',
        ),
    ]