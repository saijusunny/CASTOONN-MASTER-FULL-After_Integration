# Generated by Django 4.0.2 on 2023-07-18 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CastoonnApp', '0003_profile_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_artist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CastoonnApp.user_registration'),
        ),
    ]