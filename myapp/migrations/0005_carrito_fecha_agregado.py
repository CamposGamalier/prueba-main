# Generated by Django 5.0.6 on 2024-06-22 03:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_carrito_fecha_agregado'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='fecha_agregado',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
