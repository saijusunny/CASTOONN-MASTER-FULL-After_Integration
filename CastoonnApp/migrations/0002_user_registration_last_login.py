# Generated by Django 4.0.2 on 2023-07-14 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CastoonnApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_registration',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
