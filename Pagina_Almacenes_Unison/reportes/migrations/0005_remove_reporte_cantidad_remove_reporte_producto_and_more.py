# Generated by Django 4.2.1 on 2023-11-30 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0009_alter_gasto_cantidad_alter_gasto_gasto'),
        ('reportes', '0004_alter_reporte_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporte',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='producto',
        ),
        migrations.CreateModel(
            name='DetalleReporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiales.material', verbose_name='Material')),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportes.reporte', verbose_name='Reporte')),
            ],
        ),
        migrations.AddField(
            model_name='reporte',
            name='detalles',
            field=models.ManyToManyField(through='reportes.DetalleReporte', to='materiales.material'),
        ),
    ]
