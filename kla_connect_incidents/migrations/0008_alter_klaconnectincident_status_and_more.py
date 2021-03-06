# Generated by Django 4.0.3 on 2022-03-22 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kla_connect_incidents', '0007_alter_klaconnectincident_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klaconnectincident',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('complete', 'Approved')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='klaconnectreport',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('for_review', 'For Review'), ('rejected', 'Rejected'), ('complete', 'Approved')], default='pending', max_length=25),
        ),
    ]
