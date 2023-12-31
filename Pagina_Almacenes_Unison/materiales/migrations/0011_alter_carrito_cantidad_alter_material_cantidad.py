# Generated by Django 4.2.1 on 2023-12-03 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0010_alter_material_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='material',
            name='cantidad',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad'),
        ),
    ]
