from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from drf_writable_nested import NestedUpdateMixin
from rest_framework import status
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth.password_validation import validate_password
from base.models import ProdukHukum, RapatKoordinasi, Paparan, Berita, Fakta, Detail, Koperasi, JenisProdukKoperasi, UMKM, JenisProdukUMKM, PermintaanProduk, PermintaanPemasok, PenilaianPemasok, TenagaKerja, Perijinan, BahanBaku, PemakaianEnergi, AlatProduksi, Fasilitas, Pelatihan, LaporanKeuangan
from django.contrib.auth.models import User
from django.contrib import messages
import cloudinary
import cloudinary.uploader

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    detail = DetailSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'detail')
        
    def create(self, validated_data, *args, **kwargs):
        detail_data = validated_data.pop('detail')
        nik = detail_data['nik']

        instance = super().create(validated_data)
        instance.set_password(nik)
        
        Detail.objects.create(user=instance, **detail_data)
            
        instance.save()
        return instance
    
    def retrieve(self, instance):
        return instance
    
    def update(self, instance, validated_data):
        detail_data = validated_data.pop('detail', [])
        detail = instance.detail
        
        instance = super().update(instance, validated_data)
        
        detail.nik = detail_data.pop('nik')
        detail.telepon = detail_data.pop('telepon')
        foto_profil = detail_data.pop('foto_profil', detail.foto_profil)
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            detail.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        detail.save()
        
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, attrs):
        user = User.objects.filter(nik=attrs.get("nik"))
        data = super().validate(attrs)
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
        # return RefreshToken(validated_data['refresh']).access_token
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class ProdukHukumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdukHukum
        fields = '__all__'
        
    def create(self, validated_data):
        dokumen = validated_data.pop('dokumen')
        instance = super().create(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_dokumen = instance.dokumen
        
        if old_dokumen:
            cloudinary.uploader.destroy(old_dokumen.name)
        
        nama = validated_data.pop('nama')
        kategori = validated_data.pop('kategori')
        tahun = validated_data.pop('tahun')
        dokumen = validated_data.pop('dokumen')
        instance = super().update(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    

        if nama:
            instance.nama = nama
            
        if kategori:
            instance.kategori = kategori
            
        if tahun:
            instance.tahun = tahun
            
        instance.save()
        return instance 
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)
       
class RapatKoordinasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapatKoordinasi
        fields = '__all__'
        
    def create(self, validated_data):
        dokumen = validated_data.pop('dokumen')
        instance = super().create(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_dokumen = instance.dokumen
        
        if old_dokumen:
            cloudinary.uploader.destroy(old_dokumen.name)
            
        nama = validated_data.pop('nama')
        kategori = validated_data.pop('kategori')
        dokumen = validated_data.pop('dokumen')
        instance = super().update(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    

        if nama:
            instance.nama = nama
            
        if kategori:
            instance.kategori = kategori

        instance.save()
        return instance 
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)

        
class PaparanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paparan
        fields = '__all__'
        
    def create(self, validated_data):
        dokumen = validated_data.pop('dokumen')
        instance = super().create(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_dokumen = instance.dokumen
        
        if old_dokumen:
            cloudinary.uploader.destroy(old_dokumen.name)
            
        nama = validated_data.pop('nama')
        dokumen = validated_data.pop('dokumen')
        instance = super().update(instance, validated_data)
        if dokumen:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dokumen = cloudinary_storage.save(dokumen.name, dokumen)    

        if nama:
            instance.nama = nama
            
        instance.save()
        return instance 
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)

        
class BeritaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Berita
        fields = ('id', 'judul', 'isi', 'gambar', 'views_count')
    
    def create(self, validated_data):
        gambar = validated_data.pop('gambar', None)
        instance = super().create(validated_data)
        if gambar:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.gambar = cloudinary_storage.save(gambar.name, gambar)    
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_gambar = instance.gambar
        
        if old_gambar:
            cloudinary.uploader.destroy(old_gambar.name)
            
        gambar = validated_data.pop('gambar', None)
        instance = super().update(instance, validated_data)
        if gambar:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.gambar = cloudinary_storage.save(gambar.name, gambar)  
            
        instance.save()
        return instance 
    
    def retrieve(self, instance):
        berita = Berita.objects.get(id=instance.id)
        berita.views_count += 1
        berita.save()
        return berita
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)

class GambarSerializer(serializers.ModelSerializer):
    gambar = serializers.CharField()
    
    class Meta:
        model = Berita
        fields = ['id', 'gambar']

        
class FaktaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fakta
        fields = '__all__'
        
    def create(self, validated_data):
        gambar = validated_data.pop('gambar')
        instance = super().create(validated_data)
        if gambar:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.gambar = cloudinary_storage.save(gambar.name, gambar)   
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        old_gambar = instance.gambar
        
        if old_gambar:
            cloudinary.uploader.destroy(old_gambar.name)
            
        judul = validated_data.pop('judul')
        isi = validated_data.pop('isi')
        gambar = validated_data.pop('gambar')
        instance = super().update(instance, validated_data)
        if gambar:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.gambar = cloudinary_storage.save(gambar.name, gambar)    

        if judul:
            instance.nama = judul
            
        if isi:
            instance.kategori = isi
            
        instance.save()
        return instance 
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)


class LaporanKeuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaporanKeuangan
        fields = '__all__'
        
class JenisProdukKoperasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisProdukKoperasi
        fields = ('id', 'koperasi', 'foto_produk', 'komoditi', 'volume', 'satuan', 'harga', 'total')        
            
class KoperasiSerializer(serializers.ModelSerializer):
    jenis_produk_koperasi = JenisProdukKoperasiSerializer(many=True)
    lapkeu_koperasi = LaporanKeuanganSerializer()
    
    class Meta:
        model = Koperasi
        fields = ('id', 'nama', 'alamat', 'foto_profil', 'jenis', 'badan_hukum', 'ketua', 'sekretaris', 'bendahara', 'pengelola', 'pengawas', 'jml_anggota', 'jml_karyawan', 'tgl_rat', 'jml_hadir_rat', 'produk_unggulan', 'simpanan', 'pinjaman', 'latitude', 'longitude', 'tgl_penginputan', 'nama_pemilik', 'nib', 'nik', 'dok_ketua', 'dok_sekretaris', 'dok_bendahara', 'dok_pengelola', 'dok_pengawas', 'jenis_produk_koperasi', 'lapkeu_koperasi')
        
    def create(self, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_koperasi', [])
        lapkeu_data = validated_data.pop('lapkeu_koperasi')
        
        foto_profil = validated_data.pop('foto_profil', None)
        simpanan = validated_data.pop('simpanan', None)
        pinjaman = validated_data.pop('pinjaman', None)
        dok_ketua = validated_data.pop('dok_ketua', None)
        dok_sekretaris = validated_data.pop('dok_sekretaris', None)
        dok_bendahara = validated_data.pop('dok_bendahara', None)
        dok_pengelola = validated_data.pop('dok_pengelola', None)
        dok_pengawas = validated_data.pop('dok_pengawas', None)
        
        instance = super().create(validated_data)
        
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        
        if simpanan:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.simpanan = cloudinary_storage.save(simpanan.name, simpanan)
            
        if pinjaman:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.pinjaman = cloudinary_storage.save(pinjaman.name, pinjaman)
            
        if dok_ketua:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_ketua = cloudinary_storage.save(dok_ketua.name, dok_ketua)
            
        if dok_sekretaris:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_sekretaris = cloudinary_storage.save(dok_sekretaris.name, dok_sekretaris)
            
        if dok_bendahara:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_bendahara = cloudinary_storage.save(dok_bendahara.name, dok_bendahara)
            
        if dok_pengelola:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_pengelola = cloudinary_storage.save(dok_pengelola.name, dok_pengelola)
            
        if dok_pengawas:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_pengawas = cloudinary_storage.save(dok_pengawas.name, dok_pengawas)
                
        for jenis_produk_data in jenis_produks_data:
            jenis_produk_data['koperasi'] = instance.pk
            jenis_produk_serializer = JenisProdukKoperasiSerializer(data=jenis_produk_data)
            jenis_produk_serializer.is_valid(raise_exception=True)
            jenis_produk_serializer.save()
            
        LaporanKeuangan.objects.create(koperasi=instance, **lapkeu_data)
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_koperasi', [])
        jenis_produks = (instance.jenis_produk_koperasi).all()
        jenis_produks = list(jenis_produks)
        
        lapkeu_data = validated_data.pop('lapkeu_koperasi', [])
        lapkeu = instance.lapkeu_koperasi
        
        foto_profil = validated_data.pop('foto_profil', instance.foto_profil)
        simpanan = validated_data.pop('simpanan', instance.simpanan)
        pinjaman = validated_data.pop('pinjaman', instance.pinjaman)
        dok_ketua = validated_data.pop('dok_ketua', instance.dok_ketua)
        dok_sekretaris = validated_data.pop('dok_sekretaris', instance.dok_sekretaris)
        dok_bendahara = validated_data.pop('dok_bendahara', instance.dok_bendahara)
        dok_pengelola = validated_data.pop('dok_pengelola', instance.dok_pengelola)
        dok_pengawas = validated_data.pop('dok_pengawas', instance.dok_pengawas)
        
        instance = super().update(instance, validated_data)
        
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        
        if simpanan:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.simpanan = cloudinary_storage.save(simpanan.name, simpanan)
            
        if pinjaman:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.pinjaman = cloudinary_storage.save(pinjaman.name, pinjaman)
            
        if dok_ketua:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_ketua = cloudinary_storage.save(dok_ketua.name, dok_ketua)
            
        if dok_sekretaris:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_sekretaris = cloudinary_storage.save(dok_sekretaris.name, dok_sekretaris)
            
        if dok_bendahara:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_bendahara = cloudinary_storage.save(dok_bendahara.name, dok_bendahara)
            
        if dok_pengelola:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_pengelola = cloudinary_storage.save(dok_pengelola.name, dok_pengelola)
            
        if dok_pengawas:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.dok_pengawas = cloudinary_storage.save(dok_pengawas.name, dok_pengawas)
        
        for jenis_produk_data in jenis_produks_data:
            jenis_produk = jenis_produks.pop(0)
            
            foto_produk = jenis_produk_data.pop('foto_produk', jenis_produk.foto_produk)
            
            if foto_produk:
                cloudinary_storage = RawMediaCloudinaryStorage()
                jenis_produk.foto_produk = cloudinary_storage.save(foto_produk.name, foto_produk)
                
            jenis_produk.komoditi = jenis_produk_data.pop('komoditi', jenis_produk.komoditi)
            jenis_produk.volume = jenis_produk_data.pop('volume', jenis_produk.volume)
            jenis_produk.satuan = jenis_produk_data.pop('satuan', jenis_produk.satuan)
            jenis_produk.harga = jenis_produk_data.pop('harga', jenis_produk.harga)
            jenis_produk.total = jenis_produk_data.pop('total', jenis_produk.total)
            jenis_produk.save()
        
        laba_rugi = lapkeu_data.pop('laba_rugi', lapkeu.laba_rugi)
        neraca = lapkeu_data.pop('neraca', lapkeu.neraca)
        arus_kas = lapkeu_data.pop('arus_kas', lapkeu.arus_kas)
        perubahan_modal = lapkeu_data.pop('perubahan_modal', lapkeu.perubahan_modal)
        catatan_keuangan = lapkeu_data.pop('catatan_keuangan', lapkeu.catatan_keuangan)
        
        if laba_rugi:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.laba_rugi = cloudinary_storage.save(laba_rugi.name, laba_rugi)
            
        if neraca:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.neraca = cloudinary_storage.save(neraca.name, neraca)

        if arus_kas:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.arus_kas = cloudinary_storage.save(arus_kas.name, arus_kas)

        if perubahan_modal:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.perubahan_modal = cloudinary_storage.save(perubahan_modal.name, perubahan_modal)

        if catatan_keuangan:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.catatan_keuangan = cloudinary_storage.save(catatan_keuangan.name, catatan_keuangan)
        
        lapkeu.nama_KUMKM = lapkeu_data.pop('nama_KUMKM', lapkeu.nama_KUMKM)
        lapkeu.bulan = lapkeu_data.pop('bulan')
        lapkeu.tahun = lapkeu_data.pop('tahun')
        lapkeu.perubahan_modal = lapkeu_data.pop('perubahan_modal')
        lapkeu.catatan_keuangan = lapkeu_data.pop('catatan_keuangan')
        lapkeu.kas = lapkeu_data.pop('kas')
        lapkeu.bank = lapkeu_data.pop('bank')
        lapkeu.pinjaman_anggota = lapkeu_data.pop('pinjaman_anggota')
        lapkeu.pinjaman_macet = lapkeu_data.pop('pinjaman_macet')
        lapkeu.pendapatan_diterima = lapkeu_data.pop('pendapatan_diterima')
        lapkeu.beban = lapkeu_data.pop('beban')
        lapkeu.piutang_tak_tertagih = lapkeu_data.pop('piutang_tak_tertagih')
        lapkeu.aset_lancar = lapkeu_data.pop('aset_lancar')
        lapkeu.persediaan_barang = lapkeu_data.pop('persediaan_barang')
        lapkeu.persediaan_konsinyasi = lapkeu_data.pop('persediaan_konsinyasi')
        lapkeu.piutang_usaha = lapkeu_data.pop('piutang_usaha')
        lapkeu.tanah = lapkeu_data.pop('tanah')
        lapkeu.bangunan = lapkeu_data.pop('bangunan')
        lapkeu.peny_bangunan = lapkeu_data.pop('peny_bangunan')
        lapkeu.inventaris_kantor = lapkeu_data.pop('inventaris_kantor')
        lapkeu.peny_inventaris_kantor = lapkeu_data.pop('peny_inventaris_kantor')
        lapkeu.aset_tidak_lancar = lapkeu_data.pop('aset_tidak_lancar')
        lapkeu.simpanan_pokok = lapkeu_data.pop('simpanan_pokok')
        lapkeu.simpanan_wajib = lapkeu_data.pop('simpanan_wajib')
        lapkeu.donasi = lapkeu_data.pop('donasi')
        lapkeu.cad = lapkeu_data.pop('cad')
        lapkeu.modal_penyertaan = lapkeu_data.pop('modal_penyertaan')
        lapkeu.pendapatan_jasa = lapkeu_data.pop('pendapatan_jasa')
        lapkeu.pendapatan_administrasi = lapkeu_data.pop('pendapatan_administrasi')
        lapkeu.pendapatan_toko = lapkeu_data.pop('pendapatan_toko')
        lapkeu.pendapatan_lainnya = lapkeu_data.pop('pendapatan_lainnya')
        lapkeu.hpp = lapkeu_data.pop('hpp')
        lapkeu.jasa_simpanan = lapkeu_data.pop('jasa_simpanan')
        lapkeu.jasa_bank = lapkeu_data.pop('jasa_bank')
        lapkeu.jasa_simpanan_lain = lapkeu_data.pop('jasa_simpanan_lain')
        lapkeu.jasa_simpanan_berjangka = lapkeu_data.pop('jasa_simpanan_berjangka')
        lapkeu.jasa_simpanan_khusus = lapkeu_data.pop('jasa_simpanan_khusus')
        lapkeu.biaya_asuransi = lapkeu_data.pop('biaya_asuransi')
        lapkeu.biaya_audit = lapkeu_data.pop('biaya_audit')
        lapkeu.biaya_pajak = lapkeu_data.pop('biaya_pajak')
        lapkeu.biaya_keuangan_lain = lapkeu_data.pop('biaya_keuangan_lain')
        lapkeu.biaya_rapat_pengurus = lapkeu_data.pop('biaya_rapat_pengurus')
        lapkeu.biaya_rapat_anggota = lapkeu_data.pop('biaya_rapat_anggota')
        lapkeu.biaya_perjalanan_dinas = lapkeu_data.pop('biaya_perjalanan_dinas')
        lapkeu.biaya_diklat = lapkeu_data.pop('biaya_diklat')
        lapkeu.honor_pengurus = lapkeu_data.pop('honor_pengurus')
        lapkeu.biaya_pembinaan = lapkeu_data.pop('biaya_pembinaan')
        lapkeu.biaya_org_lain = lapkeu_data.pop('biaya_org_lain')
        lapkeu.gaji_karyawan = lapkeu_data.pop('gaji_karyawan')
        lapkeu.tunjangan = lapkeu_data.pop('tunjangan')
        lapkeu.konsumsi = lapkeu_data.pop('konsumsi')
        lapkeu.biaya_transport_dinas = lapkeu_data.pop('biaya_transport_dinas')
        lapkeu.biaya_pendidikan = lapkeu_data.pop('biaya_pendidikan')
        lapkeu.biaya_karyawan_lain = lapkeu_data.pop('biaya_karyawan_lain')
        lapkeu.biaya_alat_tulis = lapkeu_data.pop('biaya_alat_tulis')
        lapkeu.biaya_listrik = lapkeu_data.pop('biaya_listrik')
        lapkeu.biaya_telepon = lapkeu_data.pop('biaya_telepon')
        lapkeu.biaya_air = lapkeu_data.pop('biaya_air')
        lapkeu.biaya_ops_lain = lapkeu_data.pop('biaya_ops_lain')
        lapkeu.save()
        
        instance.save()
        return instance
    
    def retrieve(self, instance):
        return instance
    
    def destroy(self, instance, request, *args, **kwargs):
        instance.delete()
        # return Response({"Success": "Data deleted successfully"}, status=status.HTTP_202_OK)
        return messages.success(self.request, 'Form submission successful')
       
class JenisProdukUMKMSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisProdukUMKM
        fields = ('id', 'koperasi', 'foto_produk', 'komoditi', 'volume', 'satuan', 'harga', 'total')

class PermintaanProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanProduk
        fields = '__all__'
        
class PermintaanPemasokSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanPemasok
        fields = '__all__'
        
class PenilaianPemasokSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenilaianPemasok
        fields = '__all__'
        
class TenagaKerjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenagaKerja
        fields = '__all__'
        
class PerijinanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perijinan
        fields = '__all__'
        
class BahanBakuSerializer(serializers.ModelSerializer):
    class Meta:
        model = BahanBaku
        fields = '__all__'
        
class PemakaianEnergiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PemakaianEnergi
        fields = '__all__'
        
class AlatProduksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlatProduksi
        fields = '__all__'
        
class FasilitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fasilitas
        fields = '__all__'

class PelatihanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelatihan
        fields = '__all__'
  
class UMKMSerializer(serializers.ModelSerializer):
    jenis_produk_umkm = JenisProdukUMKMSerializer(many=True)
    permintaan_produk_umkm = PermintaanProdukSerializer(many=True)
    permintaan_pemasok_umkm = PermintaanPemasokSerializer(many=True)
    penilaian_pemasok_umkm = PenilaianPemasokSerializer(many=True)
    tenaga_kerja_umkm = TenagaKerjaSerializer(many=True)
    perijinan_umkm = PerijinanSerializer(many=True)
    bahan_baku_umkm = BahanBakuSerializer(many=True)
    pemakaian_energi_umkm = PemakaianEnergiSerializer(many=True)
    alat_produksi_umkm = AlatProduksiSerializer(many=True)
    fasilitas_umkm = FasilitasSerializer(many=True)
    pelatihan_umkm = PelatihanSerializer(many=True)
    lapkeu_umkm = LaporanKeuanganSerializer()
    
    class Meta:
        model = UMKM
        fields = ('nama_pemilik', 'nomor_anggota', 'alamat_domisili', 'nik', 'telepon', 'email', 'foto_profil', 'nama_usaha', 'alamat_usaha', 'bentuk', 'tahun_berdiri', 'bidang', 'wilayah_pemasaran', 'omzet', 'total_aset', 'skala', 'uraian_masalah', 'jenis_produk_umkm', 'permintaan_produk_umkm', 'permintaan_pemasok_umkm', 'penilaian_pemasok_umkm', 'tenaga_kerja_umkm', 'perijinan_umkm', 'bahan_baku_umkm', 'pemakaian_energi_umkm', 'alat_produksi_umkm', 'fasilitas_umkm', 'pelatihan_umkm', 'lapkeu_umkm')
        
    def create(self, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_umkm', [])
        permintaan_produks_data = validated_data.pop('permintaan_produk_umkm', [])
        permintaan_pemasoks_data = validated_data.pop('permintaan_pemasok_umkm', [])
        penilaian_pemasoks_data = validated_data.pop('penilaian_pemasok_umkm', [])
        tenaga_kerjas_data = validated_data.pop('tenaga_kerja_umkm', [])
        perijinans_data = validated_data.pop('perijinan_umkm', [])
        bahan_bakus_data = validated_data.pop('bahan_baku_umkm', [])
        pemakaian_energis_data = validated_data.pop('pemakaian_energi_umkm', [])
        alat_produksis_data = validated_data.pop('alat_produksi_umkm', [])
        fasilitass_data = validated_data.pop('fasilitas_umkm', [])
        pelatihans_data = validated_data.pop('pelatihan_umkm', [])
        lapkeu_data = validated_data.pop('lapkeu_umkm')
        
        foto_profil = validated_data.pop('foto_profil', None)
        
        instance = super().create(validated_data)
        
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        
        for jenis_produk_data in jenis_produks_data:
            jenis_produk_data['umkm'] = instance.pk
            jenis_produk_serializer = JenisProdukUMKMSerializer(data=jenis_produk_data)
            jenis_produk_serializer.is_valid(raise_exception=True)
            jenis_produk_serializer.save()
            
        for permintaan_produk_data in permintaan_produks_data:
            permintaan_produk_data['umkm'] = instance.pk
            permintaan_produk_serializer = PermintaanProdukSerializer(data=permintaan_produk_data)
            permintaan_produk_serializer.is_valid(raise_exception=True)
            permintaan_produk_serializer.save()
            
        for permintaan_pemasok_data in permintaan_pemasoks_data:
            permintaan_pemasok_data['umkm'] = instance.pk
            permintaan_pemasok_serializer = PermintaanPemasokSerializer(data=permintaan_pemasok_data)
            permintaan_pemasok_serializer.is_valid(raise_exception=True)
            permintaan_pemasok_serializer.save()
            
        for penilaian_pemasok_data in penilaian_pemasoks_data:
            penilaian_pemasok_data['umkm'] = instance.pk
            penilaian_pemasok_serializer = PenilaianPemasokSerializer(data=penilaian_pemasok_data)
            penilaian_pemasok_serializer.is_valid(raise_exception=True)
            penilaian_pemasok_serializer.save()
            
        for tenaga_kerja_data in tenaga_kerjas_data:
            tenaga_kerja_data['umkm'] = instance.pk
            tenaga_kerja_serializer = TenagaKerjaSerializer(data=tenaga_kerja_data)
            tenaga_kerja_serializer.is_valid(raise_exception=True)
            tenaga_kerja_serializer.save()
            
        for perijinan_data in perijinans_data:
            perijinan_data['umkm'] = instance.pk
            perijinan_serializer = PerijinanSerializer(data=perijinan_data)
            perijinan_serializer.is_valid(raise_exception=True)
            perijinan_serializer.save()
            
        for bahan_baku_data in bahan_bakus_data:
            bahan_baku_data['umkm'] = instance.pk
            bahan_baku_serializer = BahanBakuSerializer(data=bahan_baku_data)
            bahan_baku_serializer.is_valid(raise_exception=True)
            bahan_baku_serializer.save()
            
        for pemakaian_energi_data in pemakaian_energis_data:
            pemakaian_energi_data['umkm'] = instance.pk
            pemakaian_energi_serializer = PemakaianEnergiSerializer(data=pemakaian_energi_data)
            pemakaian_energi_serializer.is_valid(raise_exception=True)
            pemakaian_energi_serializer.save()
            
        for alat_produksi_data in alat_produksis_data:
            alat_produksi_data['umkm'] = instance.pk
            alat_produksi_serializer = AlatProduksiSerializer(data=alat_produksi_data)
            alat_produksi_serializer.is_valid(raise_exception=True)
            alat_produksi_serializer.save()
            
        for fasilitas_data in fasilitass_data:
            fasilitas_data['umkm'] = instance.pk
            fasilitas_serializer = FasilitasSerializer(data=fasilitas_data)
            fasilitas_serializer.is_valid(raise_exception=True)
            fasilitas_serializer.save()
            
        for pelatihan_data in pelatihans_data:
            pelatihan_data['umkm'] = instance.pk
            pelatihan_serializer = PelatihanSerializer(data=pelatihan_data)
            pelatihan_serializer.is_valid(raise_exception=True)
            pelatihan_serializer.save()
            
        LaporanKeuangan.objects.create(umkm=instance, **lapkeu_data)
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_umkm', [])
        jenis_produks = (instance.jenis_produk_umkm).all()
        jenis_produks = list(jenis_produks)
        
        permintaan_produks_data = validated_data.pop('permintaan_produk_umkm', [])
        permintaan_produks = (instance.permintaan_produk_umkm).all()
        permintaan_produks = list(permintaan_produks)
        
        permintaan_pemasoks_data = validated_data.pop('permintaan_pemasok_umkm', [])
        permintaan_pemasoks = (instance.permintaan_pemasok_umkm).all()
        permintaan_pemasoks = list(permintaan_pemasoks)
        
        penilaian_pemasoks_data = validated_data.pop('penilaian_pemasok_umkm', [])
        penilaian_pemasoks = (instance.penilaian_pemasok_umkm).all()
        penilaian_pemasoks = list(penilaian_pemasoks)
        
        tenaga_kerjas_data = validated_data.pop('tenaga_kerja_umkm', [])
        tenaga_kerjas = (instance.tenaga_kerj_umkm).all()
        tenaga_kerjas = list(tenaga_kerjas)
        
        perijinans_data = validated_data.pop('perijinan_umkm', [])
        perijinans = (instance.perijinan_umkm).all()
        perijinans = list(perijinans)
        
        bahan_bakus_data = validated_data.pop('bahan_baku_umkm', [])
        bahan_bakus = (instance.bahan_baku_umkm).all()
        bahan_bakus = list(bahan_bakus)
        
        pemakaian_energis_data = validated_data.pop('pemakaian_energi_umkm', [])
        pemakaian_energis = (instance.pemakaian_energi_umkm).all()
        pemakaian_energis = list(pemakaian_energis)
        
        alat_produksis_data = validated_data.pop('alat_produksi_umkm', [])
        alat_produksis = (instance.alat_produksi_umkm).all()
        alat_produksis = list(alat_produksis)
        
        fasilitass_data = validated_data.pop('fasilitas_umkm', [])
        fasilitass = (instance.fasilitas_umkm).all()
        fasilitass = list(fasilitass)
        
        pelatihans_data = validated_data.pop('pelatihan_umkm', [])
        pelatihans = (instance.pelatihan_umkm).all()
        pelatihans = list(pelatihans)
        
        lapkeu_data = validated_data.pop('lapkeu_umkm', [])
        lapkeu = instance.lapkeu_umkm
        
        foto_profil = validated_data.pop('foto_profil', instance.foto_profil)
        
        instance = super().update(instance, validated_data)
        
        if foto_profil:
            cloudinary_storage = RawMediaCloudinaryStorage()
            instance.foto_profil = cloudinary_storage.save(foto_profil.name, foto_profil)
        
        for jenis_produk_data in jenis_produks_data:
            jenis_produk = jenis_produks.pop(0)
            
            foto_produk = jenis_produk_data.pop('foto_produk', jenis_produk.foto_produk)
            
            if foto_produk:
                cloudinary_storage = RawMediaCloudinaryStorage()
                jenis_produk.foto_produk = cloudinary_storage.save(foto_produk.name, foto_produk)
                
            jenis_produk.komoditi = jenis_produk_data.pop('komoditi', jenis_produk.komoditi)
            jenis_produk.volume = jenis_produk_data.pop('volume', jenis_produk.volume)
            jenis_produk.satuan = jenis_produk_data.pop('satuan', jenis_produk.satuan)
            jenis_produk.harga = jenis_produk_data.pop('harga', jenis_produk.harga)
            jenis_produk.total = jenis_produk_data.pop('total', jenis_produk.total)
            jenis_produk.save()
            
        for permintaan_produk_data in permintaan_produks_data:
            permintaan_produk = permintaan_produks.pop(0)
        
            permintaan_produk.bulan = permintaan_produk_data.pop('bulan', permintaan_produk.bulan)
            permintaan_produk.tahun = permintaan_produk_data.pop('tahun', permintaan_produk.tahun)
            permintaan_produk.nama_produk = permintaan_produk_data.pop('nama_produk', permintaan_produk.nama_produk)
            permintaan_produk.permintaan = permintaan_produk_data.pop('permintaan', permintaan_produk.permintaan)
            permintaan_produk.produksi = permintaan_produk_data.pop('produksi', permintaan_produk.produksi)
            permintaan_produk.save()
            
        for permintaan_pemasok_data in permintaan_pemasoks_data:
            permintaan_pemasok  = permintaan_pemasoks.pop(0)
            
            permintaan_pemasok.bulan = permintaan_pemasok_data.pop('bulan', permintaan_pemasok.bulan)
            permintaan_pemasok.tahun = permintaan_pemasok_data.pop('tahun', permintaan_pemasok.tahun)
            permintaan_pemasok.pemasok = permintaan_pemasok_data.pop('pemasok', permintaan_pemasok.pemasok)
            permintaan_pemasok.permintaan = permintaan_pemasok_data.pop('permintaan', permintaan_pemasok.permintaan)
            permintaan_pemasok.produksi = permintaan_pemasok_data.pop('produksi', permintaan_pemasok.produksi)
            permintaan_pemasok.save()
            
        for penilaian_pemasok_data in penilaian_pemasoks_data:
            penilaian_pemasok = penilaian_pemasoks.pop(0)
            
            penilaian_pemasok.nama_pemasok = penilaian_pemasok_data.pop('nama_pemasok', penilaian_pemasok.nama_pemasok)
            penilaian_pemasok.kualitas = penilaian_pemasok_data.pop('kualitas', penilaian_pemasok.kualitas)
            penilaian_pemasok.pengiriman = penilaian_pemasok_data.pop('pengiriman', penilaian_pemasok.pengiriman)
            penilaian_pemasok.harga = penilaian_pemasok_data.pop('harga', penilaian_pemasok.harga)
            penilaian_pemasok.kualitas_harga = penilaian_pemasok_data.pop('kualitas_harga', penilaian_pemasok.kualitas_harga)
            penilaian_pemasok.kualitas_pengiriman = penilaian_pemasok_data.pop('kualitas_pengiriman', penilaian_pemasok.kualitas_pengiriman)
            penilaian_pemasok.harga_pengiriman = penilaian_pemasok_data.pop('harga_pengiriman', penilaian_pemasok.harga_pengiriman)
            penilaian_pemasok.save()
            
        for tenaga_kerja_data in tenaga_kerjas_data:
            tenaga_kerja = tenaga_kerjas.pop(0)
            
            tenaga_kerja.jenis = tenaga_kerja_data.pop('jenis', tenaga_kerja.jenis) 
            tenaga_kerja.jumlah = tenaga_kerja_data.pop('jumlah', tenaga_kerja.jumlah)
            tenaga_kerja.pendidikan = tenaga_kerja_data.pop('pendidikan', tenaga_kerja.pendidikan)
            tenaga_kerja.save()
            
        for perijinan_data in perijinans_data:
            perijinan = perijinans.pop(0)
            
            perijinan.jenis = perijinan_data.pop('jenis', perijinan.jenis)
            perijinan.nomor = perijinan_data.pop('nomor', perijinan.nomor)
            perijinan.tanggal = perijinan_data.pop('tanggal', perijinan.tanggal)
            perijinan.save(
                
            )
        for bahan_baku_data in bahan_bakus_data:
            bahan_baku = bahan_bakus.pop(0)
            
            bahan_baku.jenis = bahan_baku_data.pop('jenis', bahan_baku.jenis)
            bahan_baku.volume = bahan_baku_data.pop('volume', bahan_baku.volume) 
            bahan_baku.nilai = bahan_baku_data.pop('nilai', bahan_baku.nilai)
            bahan_baku.asal = bahan_baku_data.pop('asal', bahan_baku.asal)
            bahan_baku.save()
            
        for pemakaian_energi_data in pemakaian_energis_data:
            pemakaian_energi = pemakaian_energis.pop(0)
            
            pemakaian_energi.jenis = pemakaian_energi_data.pop('jenis', pemakaian_energi.jenis)
            pemakaian_energi.kapasitas = pemakaian_energi_data.pop('kapasitas', pemakaian_energi.kapasitas)
            pemakaian_energi.keterangan = pemakaian_energi_data.pop('keterangan', pemakaian_energi.keterangan)
            pemakaian_energi.save()
        
        for alat_produksi_data in alat_produksis_data:
            alat_produksi = alat_produksis.pop(0)
            
            alat_produksi.nama = alat_produksi_data.pop('nama', alat_produksi.nama)
            alat_produksi.save()
            
        for fasilitas_data in fasilitass_data:
            fasilitas = fasilitass.pop(0)
            
            fasilitas.jenis = fasilitas_data.pop('jenis', fasilitas.jenis)
            fasilitas.nama = fasilitas_data.pop('nama', fasilitas.nama)    
            fasilitas.tahun = fasilitas_data.pop('tahun', fasilitas.tahun)
            fasilitas.save()
            
        for pelatihan_data in pelatihans_data:
            pelatihan = pelatihans.pop(0)
            
            pelatihan.nama = pelatihan_data.pop('nama', pelatihan.nama)
            pelatihan.tahun = pelatihan_data.pop('tahun', pelatihan.tahun)
            pelatihan.tempat = pelatihan_data.pop('tempat', pelatihan.tempat)
            pelatihan.save()
        
        laba_rugi = lapkeu_data.pop('laba_rugi', lapkeu.laba_rugi)
        neraca = lapkeu_data.pop('neraca', lapkeu.neraca)
        arus_kas = lapkeu_data.pop('arus_kas', lapkeu.arus_kas)
        perubahan_modal = lapkeu_data.pop('perubahan_modal', lapkeu.perubahan_modal)
        catatan_keuangan = lapkeu_data.pop('catatan_keuangan', lapkeu.catatan_keuangan)
        
        if laba_rugi:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.laba_rugi = cloudinary_storage.save(laba_rugi.name, laba_rugi)
            
        if neraca:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.neraca = cloudinary_storage.save(neraca.name, neraca)

        if arus_kas:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.arus_kas = cloudinary_storage.save(arus_kas.name, arus_kas)

        if perubahan_modal:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.perubahan_modal = cloudinary_storage.save(perubahan_modal.name, perubahan_modal)

        if catatan_keuangan:
            cloudinary_storage = RawMediaCloudinaryStorage()
            lapkeu.catatan_keuangan = cloudinary_storage.save(catatan_keuangan.name, catatan_keuangan)
        
        lapkeu.nama_KUMKM = lapkeu_data.pop('nama_KUMKM', lapkeu.nama_KUMKM)
        lapkeu.bulan = lapkeu_data.pop('bulan')
        lapkeu.tahun = lapkeu_data.pop('tahun')
        lapkeu.perubahan_modal = lapkeu_data.pop('perubahan_modal')
        lapkeu.catatan_keuangan = lapkeu_data.pop('catatan_keuangan')
        lapkeu.kas = lapkeu_data.pop('kas')
        lapkeu.bank = lapkeu_data.pop('bank')
        lapkeu.pinjaman_anggota = lapkeu_data.pop('pinjaman_anggota')
        lapkeu.pinjaman_macet = lapkeu_data.pop('pinjaman_macet')
        lapkeu.pendapatan_diterima = lapkeu_data.pop('pendapatan_diterima')
        lapkeu.beban = lapkeu_data.pop('beban')
        lapkeu.piutang_tak_tertagih = lapkeu_data.pop('piutang_tak_tertagih')
        lapkeu.aset_lancar = lapkeu_data.pop('aset_lancar')
        lapkeu.persediaan_barang = lapkeu_data.pop('persediaan_barang')
        lapkeu.persediaan_konsinyasi = lapkeu_data.pop('persediaan_konsinyasi')
        lapkeu.piutang_usaha = lapkeu_data.pop('piutang_usaha')
        lapkeu.tanah = lapkeu_data.pop('tanah')
        lapkeu.bangunan = lapkeu_data.pop('bangunan')
        lapkeu.peny_bangunan = lapkeu_data.pop('peny_bangunan')
        lapkeu.inventaris_kantor = lapkeu_data.pop('inventaris_kantor')
        lapkeu.peny_inventaris_kantor = lapkeu_data.pop('peny_inventaris_kantor')
        lapkeu.aset_tidak_lancar = lapkeu_data.pop('aset_tidak_lancar')
        lapkeu.simpanan_pokok = lapkeu_data.pop('simpanan_pokok')
        lapkeu.simpanan_wajib = lapkeu_data.pop('simpanan_wajib')
        lapkeu.donasi = lapkeu_data.pop('donasi')
        lapkeu.cad = lapkeu_data.pop('cad')
        lapkeu.modal_penyertaan = lapkeu_data.pop('modal_penyertaan')
        lapkeu.pendapatan_jasa = lapkeu_data.pop('pendapatan_jasa')
        lapkeu.pendapatan_administrasi = lapkeu_data.pop('pendapatan_administrasi')
        lapkeu.pendapatan_toko = lapkeu_data.pop('pendapatan_toko')
        lapkeu.pendapatan_lainnya = lapkeu_data.pop('pendapatan_lainnya')
        lapkeu.hpp = lapkeu_data.pop('hpp')
        lapkeu.jasa_simpanan = lapkeu_data.pop('jasa_simpanan')
        lapkeu.jasa_bank = lapkeu_data.pop('jasa_bank')
        lapkeu.jasa_simpanan_lain = lapkeu_data.pop('jasa_simpanan_lain')
        lapkeu.jasa_simpanan_berjangka = lapkeu_data.pop('jasa_simpanan_berjangka')
        lapkeu.jasa_simpanan_khusus = lapkeu_data.pop('jasa_simpanan_khusus')
        lapkeu.biaya_asuransi = lapkeu_data.pop('biaya_asuransi')
        lapkeu.biaya_audit = lapkeu_data.pop('biaya_audit')
        lapkeu.biaya_pajak = lapkeu_data.pop('biaya_pajak')
        lapkeu.biaya_keuangan_lain = lapkeu_data.pop('biaya_keuangan_lain')
        lapkeu.biaya_rapat_pengurus = lapkeu_data.pop('biaya_rapat_pengurus')
        lapkeu.biaya_rapat_anggota = lapkeu_data.pop('biaya_rapat_anggota')
        lapkeu.biaya_perjalanan_dinas = lapkeu_data.pop('biaya_perjalanan_dinas')
        lapkeu.biaya_diklat = lapkeu_data.pop('biaya_diklat')
        lapkeu.honor_pengurus = lapkeu_data.pop('honor_pengurus')
        lapkeu.biaya_pembinaan = lapkeu_data.pop('biaya_pembinaan')
        lapkeu.biaya_org_lain = lapkeu_data.pop('biaya_org_lain')
        lapkeu.gaji_karyawan = lapkeu_data.pop('gaji_karyawan')
        lapkeu.tunjangan = lapkeu_data.pop('tunjangan')
        lapkeu.konsumsi = lapkeu_data.pop('konsumsi')
        lapkeu.biaya_transport_dinas = lapkeu_data.pop('biaya_transport_dinas')
        lapkeu.biaya_pendidikan = lapkeu_data.pop('biaya_pendidikan')
        lapkeu.biaya_karyawan_lain = lapkeu_data.pop('biaya_karyawan_lain')
        lapkeu.biaya_alat_tulis = lapkeu_data.pop('biaya_alat_tulis')
        lapkeu.biaya_listrik = lapkeu_data.pop('biaya_listrik')
        lapkeu.biaya_telepon = lapkeu_data.pop('biaya_telepon')
        lapkeu.biaya_air = lapkeu_data.pop('biaya_air')
        lapkeu.biaya_ops_lain = lapkeu_data.pop('biaya_ops_lain')
        lapkeu.save()
        
        instance.save()
        return instance
    
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=Akun.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
#         extra_kwargs = {
#             'username': {'required': True},
#             'email': {'required': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             # nik=validated_data['nik'],
#             # telepon=validated_data['telepon'],
#             # nama_lengkap=validated_data['nama_lengkap']
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user