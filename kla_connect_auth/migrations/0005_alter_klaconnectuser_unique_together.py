# Generated by Django 4.0.3 on 2022-03-21 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kla_connect_auth', '0004_alter_klaconnectuser_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='klaconnectuser',
            unique_together={('email',)},
            
        ),
    ]
