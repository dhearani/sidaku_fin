# Generated by Django 4.1.6 on 2023-05-24 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_musician_album'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Musician',
        ),
    ]
