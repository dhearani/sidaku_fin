# Generated by Django 4.1.6 on 2023-03-17 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_berita_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='berita',
            old_name='id',
            new_name='uuid',
        ),
    ]
