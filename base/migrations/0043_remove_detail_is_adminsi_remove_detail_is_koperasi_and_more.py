# Generated by Django 4.2.2 on 2023-07-07 18:35

import base.models
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0042_laporankeuangan_beban_ymh_dibayar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='is_adminsi',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='is_koperasi',
        ),
        migrations.RemoveField(
            model_name='detail',
            name='is_umkm',
        ),
        migrations.AddField(
            model_name='detail',
            name='role',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='koperasi',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='umkm',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='dok_bendahara',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='dok_ketua',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='dok_pengawas',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='dok_pengelola',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='dok_sekretaris',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='pinjaman',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='produk_unggulan',
            field=models.FileField(max_length=255, upload_to='', validators=[base.models.PDFValidator()]),
        ),
        migrations.AlterField(
            model_name='koperasi',
            name='simpanan',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='arus_kas',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='catatan_keuangan',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='laba_rugi',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='neraca',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='perubahan_modal',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='paparan',
            name='dokumen',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='produkhukum',
            name='dokumen',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
        migrations.AlterField(
            model_name='rapatkoordinasi',
            name='dokumen',
            field=models.FileField(null=True, upload_to='documents', validators=[base.models.PDFValidator()], verbose_name=''),
        ),
    ]
