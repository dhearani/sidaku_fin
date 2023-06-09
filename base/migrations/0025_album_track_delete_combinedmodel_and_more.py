# Generated by Django 4.1.6 on 2023-05-24 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_contoh2_contoh1_alter_contoh1_isi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=100)),
                ('tracks', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CombinedModel',
        ),
        migrations.RemoveField(
            model_name='contoh2',
            name='contoh1',
        ),
        migrations.DeleteModel(
            name='Contoh1',
        ),
        migrations.DeleteModel(
            name='Contoh2',
        ),
        migrations.AddField(
            model_name='album',
            name='track',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.track'),
        ),
    ]
