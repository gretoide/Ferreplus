# Generated by Django 5.0.4 on 2024-05-03 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vista_usuario', '0008_usuario_apellido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
        migrations.AlterField(
            model_name='imagen',
            name='publicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vista_usuario.publicacion'),
        ),
    ]
