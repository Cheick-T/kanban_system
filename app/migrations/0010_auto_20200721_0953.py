# Generated by Django 3.0.8 on 2020-07-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200720_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dossier',
            name='emplacement',
        ),
        migrations.AddField(
            model_name='mouvement',
            name='sens',
            field=models.CharField(blank=True, max_length=3, verbose_name='Sens'),
        ),
    ]
