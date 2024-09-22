# Generated by Django 4.2.7 on 2024-09-09 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_rename_ajuste_deficit_ninoinfo_estatura_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ninosanoinfo',
            name='formula_infantil',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ninosanoinfo',
            name='leche_materna_exclusiva',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ninosanoinfo',
            name='leche_materna_y_formula',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ninosanoinfo',
            name='rango_1_18_anos',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='alimentacion',
            field=models.CharField(default='No Aplica', max_length=255),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='base_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuarios.ninoinfo'),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='clasificacion_pce',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='clasificacion_pt',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='clasificacion_te',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='pce',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='pt',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ninosanoinfo',
            name='te',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
