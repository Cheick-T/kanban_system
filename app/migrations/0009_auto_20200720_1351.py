# Generated by Django 3.0.8 on 2020-07-20 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200706_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mouvement',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mouvements', to='app.Agent'),
        ),
    ]
