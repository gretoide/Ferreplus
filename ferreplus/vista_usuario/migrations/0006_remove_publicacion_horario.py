# Generated by Django 5.0.4 on 2024-05-02 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vista_usuario', '0005_remove_publicacion_autor_alter_publicacion_categoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='horario',
        ),
    ]
