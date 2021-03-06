# Generated by Django 4.0.3 on 2022-06-16 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kla_connect_profiles', '0006_alter_klaconnectuserprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=225)),
                ('latitude', models.DecimalField(blank=True, decimal_places=20, max_digits=25, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=20, max_digits=25, null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VistedAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kla_connect_profiles.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visted_places', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='klaconnectuserprofile',
            name='home_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_home_address', to='kla_connect_profiles.address'),
        ),
        migrations.AddField(
            model_name='klaconnectuserprofile',
            name='work_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_query_name='my_work_address', to='kla_connect_profiles.address'),
        ),
    ]
