# Generated by Django 3.0.8 on 2020-07-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emplacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Emplacement de dossiers',
                'verbose_name_plural': 'Emplacements de dossiers',
            },
        ),
    ]
