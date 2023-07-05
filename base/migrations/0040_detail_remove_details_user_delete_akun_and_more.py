# Generated by Django 4.2.2 on 2023-07-03 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0039_remove_akun_foto_profil_url_remove_akun_is_adminsi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(max_length=16, unique=True)),
                ('telepon', models.CharField(max_length=13)),
                ('foto_profil', models.ImageField(upload_to='assets', verbose_name='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='details',
            name='user',
        ),
        migrations.DeleteModel(
            name='Akun',
        ),
        migrations.DeleteModel(
            name='Details',
        ),
    ]