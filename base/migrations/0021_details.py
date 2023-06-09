# Generated by Django 4.1.6 on 2023-05-19 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0020_alter_akun_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(max_length=16, unique=True)),
                ('telepon', models.CharField(max_length=13)),
                ('nama_lengkap', models.CharField(max_length=100)),
                ('foto_profil', models.ImageField(upload_to='foto_profil', verbose_name='')),
                ('foto_profil_url', models.CharField(max_length=255)),
                ('is_adminsi', models.BooleanField(default=False)),
                ('is_umkm', models.BooleanField(default=False)),
                ('is_koperasi', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
