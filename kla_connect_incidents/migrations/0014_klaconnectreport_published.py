# Generated by Django 4.0.3 on 2022-04-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kla_connect_incidents', '0013_alter_klaconnectincident_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='klaconnectreport',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
