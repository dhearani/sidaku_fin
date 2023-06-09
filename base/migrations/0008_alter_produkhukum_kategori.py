# Generated by Django 4.1.6 on 2023-03-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_produkhukum_kategori'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produkhukum',
            name='kategori',
            field=models.CharField(choices=[('K1', 'Undang-Undang'), ('K2', 'Perancangan Undang-Undang'), ('K3', 'Peraturan Pemerintah'), ('K4', 'Peraturan Presiden'), ('K5', 'Keputusan dan Intruksi Presiden'), ('K6', 'Peraturan Menteri'), ('K7', 'Keputusan Menteri'), ('K8', 'Keputusan Deputi'), ('K9', 'Peraturan Terkait'), ('K10', 'Petunjuk Pelaksanaan'), ('K11', 'Surat Edaran')], max_length=255),
        ),
    ]
