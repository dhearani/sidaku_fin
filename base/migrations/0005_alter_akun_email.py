# Generated by Django 4.1.6 on 2023-03-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_akun_nik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='akun',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
