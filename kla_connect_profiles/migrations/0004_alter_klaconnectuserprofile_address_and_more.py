# Generated by Django 4.0.3 on 2022-03-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kla_connect_profiles', '0003_klaconnectlanguage_alter_department_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klaconnectuserprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='klaconnectuserprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
