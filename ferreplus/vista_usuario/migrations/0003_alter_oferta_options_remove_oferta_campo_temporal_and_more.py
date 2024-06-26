# Generated by Django 5.0.4 on 2024-06-14 01:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vista_usuario', '0002_oferta_campo_temporal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oferta',
            options={'ordering': ['fecha_intercambio', 'hora']},
        ),
        migrations.RemoveField(
            model_name='oferta',
            name='campo_temporal',
        ),
        migrations.AlterField(
            model_name='oferta',
            name='usuario_ofertante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_hechas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='usuario_recibe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_recibidas_oferta', to=settings.AUTH_USER_MODEL),
        ),
    ]
