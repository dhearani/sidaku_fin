# Generated by Django 4.1.6 on 2023-03-14 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_akun_nik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='akun',
            name='nik',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
