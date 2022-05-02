# Generated by Django 4.0.3 on 2022-05-02 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kla_connect_utils.helpers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kla_connect_auth', '0006_customnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('reset_code', models.CharField(default=kla_connect_utils.helpers.generate_verification_code, max_length=6, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'abstract': False,
            },
        ),
    ]
