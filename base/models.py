from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group, User, AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# class Informasi(models.Model):
#     logo_plut = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
#     logo_sidaku = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
#     ket_plut = models.CharField(max_length=100)
#     ket_sidaku = models.CharField(max_length=100)
#     alamat_plut = models.CharField(max_length=100)
#     telepon = models.CharField(max_length=13)
#     email = models.EmailField()
#     link_ig = models.CharField(max_length=100)
#     link_fb = models.CharField(max_length=100)

# class KontakPelayanan(models.Model):
#     fp_nahub1 = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
#     fp_nahub2 = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
#     nahub1 = models.CharField(max_length=50)
#     nahub2 = models.CharField(max_length=50)
#     wa_nahub1 = models.CharField(max_length=20)
#     wa_nahub2 = models.CharField(max_length=20)

class Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nik = models.CharField(max_length=16, unique=True)
    telepon = models.CharField(max_length=13)
    foto_profil = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
    is_umkm = models.SmallIntegerField(null=True)
    is_koperasi = models.SmallIntegerField(null=True)
    is_adminsi = models.SmallIntegerField(null=True)

class ProdukHukum(models.Model):
    nama = models.CharField(max_length=255, null=True)
    KATEGORI = (
        ("Undang-Undang", "Undang-Undang"),
        ("Perancangan Undang-Undang", "Perancangan Undang-Undang"),
        ("Peraturan Pemerintah", "Peraturan Pemerintah"),
        ("Peraturan Presiden", "Peraturan Presiden"),
        ("Keputusan dan Intruksi Presiden", "Keputusan dan Intruksi Presiden"),
        ("Peraturan Menteri", "Peraturan Menteri"),
        ("Keputusan Menteri", "Keputusan Menteri"),
        ("Keputusan Deputi", "Keputusan Deputi"),
        ("Peraturan Terkait", "Peraturan Terkait"),
        ("Petunjuk Pelaksanaan", "Petunjuk Pelaksanaan"),
        ("Surat Edaran", "Surat Edaran")
    )
    kategori = models.CharField(max_length=255, choices=KATEGORI)
    tahun = models.IntegerField(null=True)
    dokumen = models.FileField((""), upload_to='documents', null=True)
    
class RapatKoordinasi(models.Model):
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    dokumen = models.FileField((""), upload_to='documents', null=True)
    
class Paparan(models.Model):
    nama = models.CharField(max_length=255)
    dokumen = models.FileField((""), upload_to='documents', null=True)
    
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField(max_length=5000)
    gambar = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
    views_count = models.IntegerField(default=0)
    # date_created

class Fakta(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField(max_length=5000)
    gambar = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
  
class Koperasi(models.Model):
#     # FK NIK pemilik
    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    foto_profil = models.ImageField((""), upload_to='foto_profil', height_field=None, width_field=None, max_length=None)
    JENIS_KOPERASI = (
        ("Konsumen", "Konsumen"),
        ("Simpan Pinjam", "Simpan Pinjam"),
        ("Jasa", "Jasa"),
        ("Produsen", "Produsen"),
        ("Pemasaran", "Pemasaran")
    )
    jenis = models.CharField(max_length=255, choices=JENIS_KOPERASI)
    badan_hukum = models.CharField(max_length=255)
    ketua = models.CharField(max_length=255)
    sekretaris = models.CharField(max_length=255)
    bendahara = models.CharField(max_length=255)
    pengelola = models.CharField(max_length=255)
    pengawas = models.CharField(max_length=255)
    jml_anggota = models.IntegerField(null=True)
    jml_karyawan = models.IntegerField(null=True)
    tgl_rat = models.DateField()
    jml_hadir_rat = models.IntegerField(null=True)
    produk_unggulan = models.FileField(max_length=255)
    simpanan = models.FileField((""), upload_to='documents', null=True)
    pinjaman = models.FileField((""), upload_to='documents', null=True)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    tgl_penginputan = models.DateField()
    nama_pemilik = models.CharField(max_length=255)
    nib = models.CharField(max_length=255)
    nik = models.CharField(max_length=255)
    dok_ketua = models.FileField((""), upload_to='documents', null=True)
    dok_sekretaris = models.FileField((""), upload_to='documents', null=True)
    dok_bendahara = models.FileField((""), upload_to='documents', null=True)
    dok_pengelola = models.FileField((""), upload_to='documents', null=True)
    dok_pengawas = models.FileField((""), upload_to='documents', null=True)
    
class JenisProdukKoperasi(models.Model):
#     # FK ID Koperasi
    koperasi = models.ForeignKey(Koperasi, on_delete=models.CASCADE, null=True, related_name='jenis_produk_koperasi')
    foto_produk = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
    komoditi = models.CharField(null=True, max_length=50)
    volume = models.IntegerField(null=True)
    satuan = models.IntegerField(null=True)
    harga = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    
class UMKM(models.Model):
#     # FK NIK pemilik
    nama_pemilik = models.CharField(max_length=255)
    nomor_anggota = models.CharField(max_length=255)
    alamat_domisili = models.CharField(max_length=255)
    nik = models.CharField(max_length=255)
    telepon = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    foto_profil = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
    nama_usaha = models.CharField(max_length=255)
    alamat_usaha = models.CharField(max_length=255)
    BENTUK = (
        ("Perorangan", "Perorangan"),
        ("CV", "CV"),
        ("UD", "UD"),
        ("Koperasi", "Koperasi"),
        ("Lainnya", "Lainnya")
    )
    bentuk = models.CharField(max_length=255, choices=BENTUK)
    tahun_berdiri = models.IntegerField(null=True)
    BIDANG = (
        ("Makanan dalam Kemasan", "Makanan dalam Kemasan"),
        ("Minuman dalam Kemasan", "Minuman dalam Kemasan"),
        ("Kerajinan", "Kerajinan"),
        ("Perdagangan", "Perdagangan"),
        ("Jasa", "Jasa"),
        ("Lainnya", "Lainnya")
    )
    bidang = models.CharField(max_length=255, choices=BIDANG)
    wilayah_pemasaran = models.CharField(max_length=255)
    omzet = models.IntegerField(null=True)
    total_aset = models.IntegerField(null=True)
    SKALA = (
        ("Mikro", "Mikro"),
        ("Kecil", "Kecil"),
        ("Menengah", "Menengah")
    )
    skala = models.CharField(max_length=255, choices=SKALA)
    uraian_masalah = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
class JenisProdukUMKM(models.Model):
#   # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='jenis_produk_umkm')
    foto_produk = models.ImageField((""), upload_to='assets', height_field=None, width_field=None, max_length=None)
    komoditi = models.IntegerField(null=True)
    volume = models.IntegerField(null=True)
    satuan = models.IntegerField(null=True)
    harga = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    
class PermintaanProduk(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='permintaan_produk_umkm')
    BULAN = (
        ("Januari", "Januari"),
        ("Februari", "Februari"),
        ("Maret", "Maret"),
        ("April", "April"),
        ("Mei", "Mei"),
        ("Juni", "Juni"),
        ("Juli", "Juli"),
        ("Agustus", "Agustus"),
        ("September", "September"),
        ("Oktober", "Oktober"),
        ("November", "November"),
        ("Desember", "Desember")
    )
    bulan = models.CharField(max_length=255, choices=BULAN)
    tahun = models.IntegerField(null=True)
    nama_produk = models.CharField(max_length=255)
    permintaan = models.CharField(max_length=255)
    produksi = models.CharField(max_length=255)
    
class PermintaanPemasok(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='permintaan_pemasok_umkm')
    BULAN = (
        ("Januari", "Januari"),
        ("Februari", "Februari"),
        ("Maret", "Maret"),
        ("April", "April"),
        ("Mei", "Mei"),
        ("Juni", "Juni"),
        ("Juli", "Juli"),
        ("Agustus", "Agustus"),
        ("September", "September"),
        ("Oktober", "Oktober"),
        ("November", "November"),
        ("Desember", "Desember")
    )
    bulan = models.CharField(max_length=255, choices=BULAN)
    tahun = models.IntegerField(null=True)
    PEMASOK = (
        ("Retailer", "Retailer"),
        ("Supplier", "Supplier")
    )
    pemasok = models.CharField(max_length=255)
    permintaan = models.CharField(max_length=255)
    produksi = models.CharField(max_length=255)
    
class PenilaianPemasok(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='penilaian_pemasok_umkm')
    nama_pemasok = models.CharField(max_length=255)
    kualitas = models.CharField(max_length=255)
    pengiriman = models.CharField(max_length=255)
    harga = models.IntegerField(null=True)
    kualitas_harga = models.IntegerField(null=True)
    kualitas_pengiriman = models.IntegerField(null=True)
    harga_pengiriman = models.IntegerField(null=True)
    
class TenagaKerja(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='tenaga_kerja_umkm')
    JENIS_KELAMIN = (
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan")
    )
    jenis = models.CharField(max_length=255, choices=JENIS_KELAMIN)
    jumlah = models.IntegerField(null=True)
    PENDIDIKAN = (
        ("SD Sederajat", "SD Sederajat"),
        ("SMP Sederajat", "SMP Sederajat"),
        ("SMA Sederajat", "SMA Sederajat"),
        ("S1/S2/S3", "S1/S2/S3")
    )
    pendidikan = models.CharField(max_length=255, choices=PENDIDIKAN)
    
class Perijinan(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='perijinan_umkm')
    JENIS_PERIJINAN = (
        ("NIB", "NIB"),
        ("P-IRT", "P-IRT"),
        ("NPWP", "NPWP"),
        ("MERK", "MERK"),
        ("HALAL", "HALAL"),
        ("BPOM", "BPOM"),
        ("Akta Pendirian", "Akta Pendirian"),
        ("Lainnya", "Lainnya")
    )
    jenis = models.CharField(max_length=255, choices=JENIS_PERIJINAN)
    nomor = models.CharField(max_length=255)
    tanggal = models.DateField()
    
class BahanBaku(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='bahan_baku_umkm')
    jenis = models.CharField(max_length=255)
    volume = models.IntegerField(null=True)
    nilai = models.IntegerField(null=True)
    asal = models.CharField(max_length=255)
    
class PemakaianEnergi(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='pemakaian_energi_umkm')
    JENIS_ENERGI = (
        ("PLN", "PLN"),
        ("Bahan Bakar Generator/Genset", "Bahan Bakar Generator/Genset"),
        ("Bahan Bakar Gas LPG (3kg/12kg)", "Bahan Bakar Gas LPG (3kg/12kg)"),
        ("Air (PDAM/HIPAM/Sumur)", "Air (PDAM/HIPAM/Sumur)")
    )
    jenis = models.CharField(max_length=255, choices=JENIS_ENERGI)
    kapasitas = models.IntegerField(null=True)
    keterangan = models.CharField(max_length=255)
    
class AlatProduksi(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='alat_produksi_umkm')
    nama = models.CharField(max_length=255)
    
class Fasilitas(models.Model):
    # FK ID UMKM
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='fasilitas_umkm')
    JENIS_FASILITAS = (
        ("ISO", "ISO"),
        ("SNI", "SNI"),
        ("SERTIFIKAT HALAL", "SERTIFIKAT HALAL"),
        ("MEREK DAGANG", "MEREK DAGANG"),
        ("UJI PRODUK", "UJI PRODUK"),
        ("ALAT/MESIN", "ALAT/MESIN"),
        ("Lainnya", "Lainnya")
    )
    jenis = models.CharField(max_length=255, choices=JENIS_FASILITAS)
    nama = models.CharField(max_length=255)
    tahun = models.IntegerField(null=True)
    
class Pelatihan(models.Model):
    # FK ID UMKM 
    umkm = models.ForeignKey(UMKM, on_delete=models.CASCADE, null=True, related_name='pelatihan_umkm')
    nama = models.CharField(max_length=255)
    tahun = models.IntegerField(null=True)
    tempat = models.CharField(max_length=255)
    
class LaporanKeuangan(models.Model):
#     # FK ID UMKM
#     # FK ID Koperasi
    koperasi = models.OneToOneField(Koperasi, on_delete=models.CASCADE, null=True, related_name='lapkeu_koperasi')
    umkm = models.OneToOneField(UMKM, on_delete=models.CASCADE, null=True, related_name='lapkeu_umkm')
    nama_KUMKM = models.CharField(max_length=50)
    BULAN = (
        ("Januari", "Januari"),
        ("Februari", "Februari"),
        ("Maret", "Maret"),
        ("April", "April"),
        ("Mei", "Mei"),
        ("Juni", "Juni"),
        ("Juli", "Juli"),
        ("Agustus", "Agustus"),
        ("September", "September"),
        ("Oktober", "Oktober"),
        ("November", "November"),
        ("Desember", "Desember")
    )
    bulan = models.CharField(max_length=10, choices=BULAN)
    tahun = models.IntegerField()
    laba_rugi = models.FileField((""), upload_to='documents', null=True)
    neraca = models.FileField((""), upload_to='documents', null=True)
    arus_kas = models.FileField((""), upload_to='documents', null=True)
    perubahan_modal = models.FileField((""), upload_to='documents', null=True)
    catatan_keuangan = models.FileField((""), upload_to='documents', null=True)
    kas = models.IntegerField()
    bank = models.IntegerField()
    pinjaman_anggota = models.IntegerField()
    pinjaman_macet = models.IntegerField()
    pendapatan_diterima = models.IntegerField()
    beban = models.IntegerField()
    piutang_tak_tertagih = models.IntegerField()
    aset_lancar = models.IntegerField()
    persediaan_barang = models.IntegerField()
    persediaan_konsinyasi = models.IntegerField()
    piutang_usaha = models.IntegerField()
    tanah = models.IntegerField()
    bangunan = models.IntegerField()
    peny_bangunan = models.IntegerField()
    inventaris_kantor = models.IntegerField()
    peny_invent_kantor = models.IntegerField()
    aset_tidak_lancar = models.IntegerField()
    simpanan_sukarela = models.IntegerField(null=True)
    simpanan_berjangka = models.IntegerField(null=True)
    hutang_usaha = models.IntegerField(null=True)
    beban_ymh_dibayar = models.IntegerField(null=True)
    hutang_lain_lain = models.IntegerField(null=True)
    simpanan_pokok = models.IntegerField()
    simpanan_wajib = models.IntegerField()
    donasi = models.IntegerField()
    cad = models.IntegerField()
    modal_penyertaan = models.IntegerField()
    pendapatan_jasa = models.IntegerField()
    pendapatan_administrasi = models.IntegerField()
    pendapatan_toko = models.IntegerField()
    pendapatan_lainnya = models.IntegerField()
    hpp = models.IntegerField()
    jasa_simpanan = models.IntegerField()
    jasa_bank = models.IntegerField()
    jasa_simpanan_lain = models.IntegerField()
    jasa_simpanan_berjangka = models.IntegerField()
    jasa_simpanan_khusus = models.IntegerField()
    biaya_asuransi = models.IntegerField()
    biaya_audit = models.IntegerField()
    biaya_pajak = models.IntegerField()
    biaya_keuangan_lain = models.IntegerField()
    biaya_rapat_pengurus = models.IntegerField()
    biaya_rapat_anggota = models.IntegerField()
    biaya_perjalanan_dinas = models.IntegerField()
    biaya_diklat = models.IntegerField()
    honor_pengurus = models.IntegerField()
    biaya_pembinaan = models.IntegerField()
    biaya_org_lain = models.IntegerField()
    gaji_karyawan = models.IntegerField()
    tunjangan = models.IntegerField()
    konsumsi = models.IntegerField()
    biaya_transport_dinas = models.IntegerField()
    biaya_pendidikan = models.IntegerField()
    biaya_karyawan_lain = models.IntegerField()
    biaya_alat_tulis = models.IntegerField()
    biaya_listrik = models.IntegerField()
    biaya_telepon = models.IntegerField()
    biaya_air = models.IntegerField()
    biaya_ops_lain = models.IntegerField()
