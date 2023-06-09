# Generated by Django 4.1.6 on 2023-03-14 03:27

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Berita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('isi', models.TextField(max_length=5000)),
                ('gambar', models.ImageField(upload_to='templates', verbose_name='')),
                ('gambar_url', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paparan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('dokumen', models.FileField(null=True, upload_to='documents', verbose_name='')),
                ('dok_url', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProdukHukum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('kategori', models.CharField(max_length=255, verbose_name=[('kategori1', 'Undang-Undang'), ('kategori2', 'Perancangan Undang-Undang'), ('kategori3', 'Peraturan Pemerintah'), ('kategori4', 'Peraturan Presiden'), ('kategori5', 'Keputusan dan Intruksi Presiden'), ('kategori6', 'Peraturan Menteri'), ('kategori7', 'Keputusan Menteri'), ('kategori8', 'Keputusan Deputi'), ('kategori9', 'Peraturan Terkait'), ('kategori10', 'Petunjuk Pelaksanaan'), ('kategori11', 'Surat Edaran')])),
                ('tahun', models.IntegerField(null=True)),
                ('dokumen', models.FileField(null=True, upload_to='documents', verbose_name='')),
                ('dok_url', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RapatKoordinasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('kategori', models.CharField(max_length=255)),
                ('dokumen', models.FileField(null=True, upload_to='documents', verbose_name='')),
                ('dok_url', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Akun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nik', models.CharField(max_length=16, unique=True)),
                ('telepon', models.CharField(max_length=13)),
                ('nama_lengkap', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('foto_profil', models.ImageField(upload_to='foto_profil', verbose_name='')),
                ('foto_profil_url', models.CharField(max_length=255)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_adminsi', models.BooleanField(default=False)),
                ('is_umkm', models.BooleanField(default=False)),
                ('is_koperasi', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='auth_group', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='auth_permission', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]