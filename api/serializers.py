from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from base.models import ProdukHukum, RapatKoordinasi, Paparan, Berita, Akun, Details, Koperasi, JenisProdukKoperasi, UMKM, JenisProdukUMKM, PermintaanProduk, PermintaanPemasok, PenilaianPemasok, TenagaKerja, Perijinan, BahanBaku, PemakaianEnergi, AlatProduksi, Fasilitas, Pelatihan, LaporanKeuangan
from django.contrib.auth.models import User

class ProdukHukumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdukHukum
        fields = '__all__'

class RapatKoordinasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapatKoordinasi
        fields = '__all__'
        
class PaparanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paparan
        fields = '__all__'
        
class BeritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Berita
        fields = '__all__'
    
class AkunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Akun
        fields = ('id', 'nik', 'nama_lengkap', 'telepon', 'email', 'username', 'password')
        
class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ('id', 'nik', 'nama_lengkap', 'telepon','foto_profil', 'foto_profil_url')
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Akun.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # nik=validated_data['nik'],
            # telepon=validated_data['telepon'],
            # nama_lengkap=validated_data['nama_lengkap']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

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
        user = Akun.objects.filter(nik=attrs.get("nik"))
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

# berhasil di postman, tp ga keupdate di database
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ('nik', 'telepon', 'nama_lengkap')
        extra_kwargs = {
            'nik': {'required': True},
            'telepon': {'required': True},
        }

    def validate_nik(self, value):
        user = self.context['request'].user
        if Details.objects.exclude(pk=user.pk).filter(nik=value).exists():
            raise serializers.ValidationError({"email": "This nik is already in use."})
        return value

    def validate_telepon(self, value):
        user = self.context['request'].user
        if Details.objects.exclude(pk=user.pk).filter(telepon=value).exists():
            raise serializers.ValidationError({"username": "This telepon is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.nik = validated_data['nik']
        instance.telepon = validated_data['telepon']
        instance.nama_lengkap = validated_data['nama_lengkap']

        instance.save()

        return instance

class LaporanKeuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaporanKeuangan
        fields = '__all__'
        
class JenisProdukKoperasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisProdukKoperasi
        fields = ('id', 'koperasi', 'foto_produk', 'foto_produk_url', 'komoditi', 'volume', 'satuan', 'harga', 'total')        
            
class KoperasiSerializer(serializers.ModelSerializer):
    jenis_produk_koperasi = JenisProdukKoperasiSerializer(many=True)
    lapkeu_koperasi = LaporanKeuanganSerializer()
    
    class Meta:
        model = Koperasi
        fields = ('id', 'nama', 'alamat', 'foto_profil', 'foto_profil_url', 'jenis', 'badan_hukum', 'ketua', 'sekretaris', 'bendahara', 'pengelola', 'pengawas', 'jml_anggota', 'jml_karyawan', 'tgl_rat', 'jml_hadir_rat', 'produk_unggulan', 'produk_unggulan_url', 'simpanan', 'simpanan_url', 'pinjaman', 'pinjaman_url', 'latitude', 'longitude', 'tgl_penginputan', 'nama_pemilik', 'nib', 'nik', 'dok_ketua', 'dok_ketua_url', 'dok_sekretaris', 'dok_sekretaris_url', 'dok_bendahara', 'dok_bendahara_url', 'dok_pengelola', 'dok_pengelola_url', 'dok_pengawas', 'dok_pengawas_url', 'jenis_produk_koperasi', 'lapkeu_koperasi')
        
    def create(self, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_koperasi')
        lapkeu_data = validated_data.pop('lapkeu_koperasi')
        koperasi = Koperasi.objects.create(**validated_data)
        for jenis_produk_data in jenis_produks_data:
            JenisProdukKoperasi.objects.create(koperasi=koperasi, **jenis_produk_data)
        LaporanKeuangan.objects.create(koperasi=koperasi, **lapkeu_data)
        return koperasi

class JenisProdukUMKMSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisProdukUMKM
        fields = ('id', 'koperasi', 'foto_produk', 'foto_produk_url', 'komoditi', 'volume', 'satuan', 'harga', 'total')

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
        fields = ('nama_pemilik', 'nomor_anggota', 'alamat_domisili', 'no_ktp_sim', 'telepon', 'email', 'foto_profil', 'foto_profil_url', 'nama_usaha', 'alamat_usaha', 'bentuk', 'tahun_berdiri', 'bidang', 'wilayah_pemasaran', 'omzet', 'total_aset', 'skala', 'uraian_masalah', 'jenis_produk_umkm', 'permintaan_produk_umkm', 'permintaan_pemasok_umkm', 'penilaian_pemasok_umkm', 'tenaga_kerja_umkm', 'perijinan_umkm', 'bahan_baku_umkm', 'pemakaian_energi_umkm', 'alat_produksi_umkm', 'fasilitas_umkm', 'pelatihan_umkm', 'lapkeu_umkm')
        
    def create(self, validated_data):
        jenis_produks_data = validated_data.pop('jenis_produk_umkm')
        permintaan_produks_data = validated_data.pop('permintaan_produk_umkm')
        permintaan_pemasoks_data = validated_data.pop('permintaan_pemasok_umkm')
        penilaian_pemasoks_data = validated_data.pop('penilaian_pemasok_umkm')
        tenaga_kerjas_data = validated_data.pop('tenaga_kerja_umkm')
        perijinans_data = validated_data.pop('perijinan_umkm')
        bahan_bakus_data = validated_data.pop('bahan_baku_umkm')
        pemakaian_energis_data = validated_data.pop('pemakaian_energi_umkm')
        alat_produksis_data = validated_data.pop('alat_produksi_umkm')
        fasilitass_data = validated_data.pop('fasilitas_umkm')
        pelatihans_data = validated_data.pop('pelatihan_umkm')
        lapkeu_data = validated_data.pop('lapkeu_umkm')
        umkm = UMKM.objects.create(**validated_data)
        for jenis_produk_data in jenis_produks_data:
            JenisProdukUMKM.objects.create(umkm=umkm, **jenis_produk_data)
        for permintaan_produk_data in permintaan_produks_data:
            PermintaanProduk.objects.create(umkm=umkm, **permintaan_produk_data)
        for permintaan_pemasok_data in permintaan_pemasoks_data:
            PermintaanPemasok.objects.create(umkm=umkm, **permintaan_pemasok_data)
        for penilaian_pemasok_data in penilaian_pemasoks_data:
            PenilaianPemasok.obejcts.create(umkm=umkm, **penilaian_pemasok_data)
        for tenaga_kerja_data in tenaga_kerjas_data:
            TenagaKerja.objects.create(umkm=umkm, **tenaga_kerja_data)
        for perijinan_data in perijinans_data:
            Perijinan.objects.create(umkm=umkm, **perijinan_data)
        for bahan_baku_data in bahan_bakus_data:
            BahanBaku.objects.create(umkm=umkm, **bahan_baku_data)
        for pemakaian_energi_data in pemakaian_energis_data:
            PemakaianEnergi.objects.create(umkm=umkm, **pemakaian_energi_data)
        for alat_produksi_data in alat_produksis_data:
            AlatProduksi.objects.create(umkm=umkm, **alat_produksi_data)
        for fasilitas_data in fasilitass_data:
            Fasilitas.objects.create(umkm=umkm, **fasilitas_data)
        for pelatihan_data in pelatihans_data:
            Pelatihan.objects.create(umkm=umkm, **pelatihan_data)
        LaporanKeuangan.objects.create(umkm=umkm, **lapkeu_data)
        return umkm
        
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from base.models import Akun

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
    # def get_token(cls, user):
    #     # Use the 'nik' attribute of the user as the token subject
    #     token = super().get_token(user)
    #     token['sub'] = user.email
    #     return token
    
    # def validate(self, attrs):
    #     # Here, you can retrieve the user using a different primary key
    #     user = Akun.objects.get(email=attrs.get("email"))
    #     data = super().validate(attrs)
    #     refresh = self.get_token(user)
    #     data["refresh"] = str(refresh)
    #     data["access"] = str(refresh.access_token)
    #     return data
    
    # def create(self, attrs):
    #     # Check that the attrs parameter contains a valid nik value
    #     nik = attrs.get('nik')
    #     if not nik:
    #         raise serializers.ValidationError('Missing nik value')

    #     # Check that there is an instance of the Akun model with the given nik value
    #     try:
    #         user = Akun.objects.get(nik=nik)
    #     except Akun.DoesNotExist:
    #         raise serializers.ValidationError('Akun with given nik does not exist')

    #     data = super().create(attrs)

    #     # Use the user instance to generate the token pair
    #     refresh = self.get_token(user)
    #     data["refresh"] = str(refresh)
    #     data["access"] = str(refresh.access_token)

    #     return data
