# Generated by Django 4.2.7 on 2024-08-23 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_alumno_altura_remove_alumno_edad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenamiento',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
