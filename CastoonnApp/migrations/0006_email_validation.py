# Generated by Django 4.0.2 on 2023-07-19 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CastoonnApp', '0005_alter_profile_artist_achievements_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_temp', models.EmailField(max_length=254)),
                ('email_otp_temp', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
