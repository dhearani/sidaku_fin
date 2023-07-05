# Generated by Django 4.2.2 on 2023-07-02 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0036_fakta_rename_no_ktp_sim_umkm_nik_umkm_latitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bahanbaku',
            old_name='asal_bahan_baku',
            new_name='asal',
        ),
        migrations.RemoveField(
            model_name='berita',
            name='gambar_url',
        ),
        migrations.RemoveField(
            model_name='fakta',
            name='gambar_url',
        ),
        migrations.RemoveField(
            model_name='jenisprodukkoperasi',
            name='foto_produk_url',
        ),
        migrations.RemoveField(
            model_name='jenisprodukumkm',
            name='foto_produk_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='dok_bendahara_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='dok_ketua_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='dok_pengawas_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='dok_pengelola_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='dok_sekretaris_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='foto_profil_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='pinjaman_url',
        ),
        migrations.RemoveField(
            model_name='koperasi',
            name='simpanan_url',
        ),
        migrations.RemoveField(
            model_name='laporankeuangan',
            name='catatan_keuangan_url',
        ),
        migrations.RemoveField(
            model_name='laporankeuangan',
            name='laba_rugi_url',
        ),
        migrations.RemoveField(
            model_name='laporankeuangan',
            name='neraca_url',
        ),
        migrations.RemoveField(
            model_name='laporankeuangan',
            name='perubahan_modal_url',
        ),
        migrations.RemoveField(
            model_name='paparan',
            name='dok_url',
        ),
        migrations.RemoveField(
            model_name='produkhukum',
            name='dok_url',
        ),
        migrations.RemoveField(
            model_name='rapatkoordinasi',
            name='dok_url',
        ),
        migrations.RemoveField(
            model_name='umkm',
            name='foto_profil_url',
        ),
        migrations.AlterField(
            model_name='laporankeuangan',
            name='arus_kas',
            field=models.FileField(null=True, upload_to='documents', verbose_name=''),
        ),
    ]
