# Generated by Django 3.0.8 on 2020-08-12 00:02

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import river.models.fields.state


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('river', '0002_auto_20200716_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=50)),
                ('prenoms', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
                'ordering': ['code', 'nom'],
            },
        ),
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
            name='Dossier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Dossier',
                'verbose_name_plural': 'Dossiers',
                'permissions': [('can_manipulate_folders', 'Can manipulate folders')],
            },
        ),
        migrations.CreateModel(
            name='EmplacementMPTT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app.EmplacementMPTT')),
            ],
            options={
                'verbose_name': 'Emplacement de dossiers MPTT',
                'verbose_name_plural': 'Emplacements de dossiers MPTT',
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
            name='Mouvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('sens', models.CharField(blank=True, max_length=3, verbose_name='Sens')),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mouvements', to='app.Agent')),
                ('dossier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mouvements', to='app.Dossier')),
                ('emplacement', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mouvements', to='app.EmplacementMPTT')),
            ],
            options={
                'verbose_name': 'Mouvement de dossier',
                'verbose_name_plural': 'Mouvements de dossiers',
                'ordering': ['dossier', 'creation_time'],
            },
        ),
        migrations.AddField(
            model_name='dossier',
            name='categorie_dossier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dossiers', to='app.FolderCategory'),
        ),
        migrations.AddField(
            model_name='dossier',
            name='state',
            field=river.models.fields.state.StateField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='river.State'),
        ),
        migrations.AddField(
            model_name='agent',
            name='categorie_agent',
            field=models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='agents', to='app.AgentCategory'),
        ),
        migrations.CreateModel(
            name='DossierOut',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('app.dossier',),
        ),
    ]
