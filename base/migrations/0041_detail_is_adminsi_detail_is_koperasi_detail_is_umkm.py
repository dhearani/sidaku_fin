# Generated by Django 4.2.2 on 2023-07-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_detail_remove_details_user_delete_akun_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='is_adminsi',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='detail',
            name='is_koperasi',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='detail',
            name='is_umkm',
            field=models.SmallIntegerField(null=True),
        ),
    ]