# Generated by Django 3.0.8 on 2020-07-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': "Catégorie d'agents",
                'verbose_name_plural': "Catégories d'agents",
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='FolderCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Catégorie de dossiers',
                'verbose_name_plural': 'Catégories de dossiers',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('categorie_dossier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='app.FolderCategory')),
            ],
            options={
                'verbose_name': 'Dossier',
                'verbose_name_plural': 'Dossiers',
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=50)),
                ('prenoms', models.CharField(blank=True, max_length=50, null=True)),
                ('categorie_agent', models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='agents', to='app.AgentCategory')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
                'ordering': ['code', 'nom'],
            },
        ),
    ]
