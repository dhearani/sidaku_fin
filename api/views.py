import os
import hashlib
from django.contrib.auth import login
import cloudinary

cloudinary.config( 
  cloud_name = "dndznnstu", 
  api_key = "414626631279137", 
  api_secret = "bMKAlxFTTpIKkCe_1CtiEVvJKz8",
  secure = True
)

import cloudinary.uploader
import cloudinary.api
import json
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from base.models import ProdukHukum, RapatKoordinasi, Paparan, Berita, Fakta, LaporanKeuangan, Koperasi, UMKM, JenisProdukKoperasi, JenisProdukUMKM, PermintaanProduk, PermintaanPemasok, PenilaianPemasok, TenagaKerja, Perijinan, BahanBaku, PemakaianEnergi, AlatProduksi, Fasilitas, Pelatihan
from .serializers import ProdukHukumSerializer, RapatKoordinasiSerializer, PaparanSerializer, BeritaSerializer, FaktaSerializer, TokenPairSerializer, ChangePasswordSerializer, RegisterSerializer, LaporanKeuanganSerializer, KoperasiSerializer, UMKMSerializer, JenisProdukKoperasiSerializer, JenisProdukUMKMSerializer, PermintaanProdukSerializer, PermintaanPemasokSerializer, PenilaianPemasokSerializer, TenagaKerjaSerializer, PerijinanSerializer, BahanBakuSerializer, PemakaianEnergiSerializer, AlatProduksiSerializer, FasilitasSerializer, PelatihanSerializer, GambarSerializer
from rest_framework import status, generics, permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from base.permissions import IsUMKM, IsKoperasi, IsAdminSI, IsOwnerOrReadOnly

class RegisterViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username']  # Replace with the fields you want to filter on
    search_fields = ['username']
    
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data['refresh_token']

            # Create a RefreshToken object from the refresh token
            token = RefreshToken(refresh_token)

            # Blacklist the refresh token to prevent its use
            token.blacklist()

            return Response({'message': 'Berhasil Logout'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'message':'Gagal Logout'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

class ProdukHukumViewSet(ModelViewSet):
    queryset = ProdukHukum.objects.all()
    serializer_class = ProdukHukumSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama', 'kategori', 'tahun']  # Replace with the fields you want to filter on
    search_fields = ['nama', 'kategori', 'tahun']

class RapatKoordinasiViewSet(ModelViewSet):
    queryset = RapatKoordinasi.objects.all()
    serializer_class = RapatKoordinasiSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama', 'kategori']  # Replace with the fields you want to filter on
    search_fields = ['nama', 'kategori']

class PaparanViewSet(ModelViewSet):
    queryset = Paparan.objects.all()
    serializer_class = PaparanSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama']  # Replace with the fields you want to filter on
    search_fields = ['nama']

class BeritaViewSet(ModelViewSet):
    queryset = Berita.objects.all()
    serializer_class = BeritaSerializer
    permission_classes = [IsAdminUser | IsAdminSI | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['judul']  # Replace with the fields you want to filter on
    search_fields = ['judul']
    
    def retrieve(self, request, pk):
        article = Berita.objects.get(id=pk)
        article.views_count += 1
        article.save()
        serializer = BeritaSerializer(article)

        return Response(serializer.data)

class GambarViewSet(generics.ListCreateAPIView):
    queryset = Berita.objects.all()
    serializer_class = GambarSerializer
    
class FaktaViewSet(ModelViewSet):
    queryset = Fakta.objects.all()
    serializer_class = FaktaSerializer
    permission_classes = [IsAdminUser | IsOwnerOrReadOnly]
    
class KoperasiViewSet(ModelViewSet):
    queryset = Koperasi.objects.all()
    serializer_class = KoperasiSerializer
    permission_classes = [IsAdminUser | IsKoperasi | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama']  # Replace with the fields you want to filter on
    search_fields = ['nama']

class UMKMViewSet(ModelViewSet):
    queryset = UMKM.objects.all()
    serializer_class = UMKMSerializer
    permission_classes = [IsAdminUser | IsUMKM | IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama_usaha']  # Replace with the fields you want to filter on
    search_fields = ['nama_usaha']

class LaporanKeuanganViewSet(ModelViewSet):
    queryset = LaporanKeuangan.objects.all()
    serializer_class = LaporanKeuanganSerializer
    permission_classes = [IsAdminUser | IsUMKM | IsKoperasi | IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nama_KUMKM']  # Replace with the fields you want to filter on
    search_fields = ['nama_KUMKM']


class UMKMListView(generics.ListCreateAPIView):
    queryset = UMKM.objects.all()
    serializer_class = UMKMSerializer

class UMKMView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UMKMSerializer
    queryset = UMKM.objects.all()
    
class JenisProdukUMKMListView(generics.ListCreateAPIView):
    queryset = JenisProdukUMKM.objects.all()
    serializer_class = JenisProdukUMKMSerializer

class JenisProdukUMKMView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JenisProdukUMKMSerializer
    queryset = JenisProdukUMKM.objects.all()
    
class PermintaanProdukListView(generics.ListCreateAPIView):
    queryset = PermintaanProduk.objects.all()
    serializer_class = PermintaanProdukSerializer

class PermintaanProdukView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PermintaanProdukSerializer
    queryset = PermintaanProduk.objects.all()
    
class PermintaanPemasokListView(generics.ListCreateAPIView):
    queryset = PermintaanPemasok.objects.all()
    serializer_class = PermintaanPemasokSerializer

class PermintaanPemasokView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PermintaanPemasokSerializer
    queryset = PermintaanPemasok.objects.all()
    
class PenilaianPemasokListView(generics.ListCreateAPIView):
    queryset = PenilaianPemasok.objects.all()
    serializer_class = PenilaianPemasokSerializer

class PenilaianPemasokView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PenilaianPemasokSerializer
    queryset = PenilaianPemasok.objects.all()

class TenagaKerjaListView(generics.ListCreateAPIView):
    queryset = TenagaKerja.objects.all()
    serializer_class = TenagaKerjaSerializer

class TenagaKerjaView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenagaKerjaSerializer
    queryset = TenagaKerja.objects.all()
    
class PerijinanListView(generics.ListCreateAPIView):
    queryset = Perijinan.objects.all()
    serializer_class = PerijinanSerializer

class PerijinanView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerijinanSerializer
    queryset = Perijinan.objects.all()
    
class BahanBakuListView(generics.ListCreateAPIView):
    queryset = BahanBaku.objects.all()
    serializer_class = BahanBakuSerializer

class BahanBakuView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BahanBakuSerializer
    queryset = BahanBaku.objects.all()
    
class PemakaianEnergiListView(generics.ListCreateAPIView):
    queryset = PemakaianEnergi.objects.all()
    serializer_class = PemakaianEnergiSerializer

class PemakaianEnergiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PemakaianEnergiSerializer
    queryset = PemakaianEnergi.objects.all()
    
class AlatProduksiListView(generics.ListCreateAPIView):
    queryset = AlatProduksi.objects.all()
    serializer_class = AlatProduksiSerializer

class AlatProduksiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlatProduksiSerializer
    queryset = AlatProduksi.objects.all()
    
class FasilitasListView(generics.ListCreateAPIView):
    queryset = Fasilitas.objects.all()
    serializer_class = FasilitasSerializer

class FasilitasView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FasilitasSerializer
    queryset = Fasilitas.objects.all()
    
class PelatihanListView(generics.ListCreateAPIView):
    queryset = Pelatihan.objects.all()
    serializer_class = PelatihanSerializer

class PelatihanView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PelatihanSerializer
    queryset = Pelatihan.objects.all()

class KoperasiListView(generics.ListCreateAPIView):
    queryset = Koperasi.objects.all()
    serializer_class = KoperasiSerializer

class KoperasiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KoperasiSerializer
    queryset = Koperasi.objects.all()
    
class JenisProdukKoperasiListView(generics.ListCreateAPIView):
    queryset = JenisProdukKoperasi.objects.all()
    serializer_class = JenisProdukKoperasiSerializer

class JenisProdukKoperasiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JenisProdukKoperasiSerializer
    queryset = JenisProdukKoperasi.objects.all()

class LaporanKeuanganListView(generics.ListCreateAPIView):
    queryset = LaporanKeuangan.objects.all()
    serializer_class = LaporanKeuanganSerializer

class LaporanKeuanganView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LaporanKeuanganSerializer
    queryset = LaporanKeuangan.objects.all()

class GrafikKUMKMView(APIView):
    def get(self, request, format=None):
        # Perform the calculation and retrieve the graphic value
        koperasi = Koperasi.objects.count()
        umkm = UMKM.objects.count()
        
        # Prepare data for the pie chart
        labels = ['Koperasi', 'UMKM'] #label
        sizes = np.array([koperasi, umkm]) #data
        
        # Check if any counts are NaN
        if np.isnan(sizes).any():
            return HttpResponse("Data is not available for creating the pie chart.")
                
        plt.figure(figsize=(8, 8))
        plt.pie(sizes.flatten(), labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Pie Chart')  
        
        # Save the chart to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        # Return the chart as the response
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type='image/png')


# komoditi koperasi dan UMKM

# Skala UMKM

# Omzet Kumulatif

# Permintaan Produk UMKM

# Bullwhip Effect KUMKM

# Rata" Kinerja Pemasok UMKM




# @api_view(['POST'])
# def tes(request):
#     serializer = AlbumSerializer(data=request.data)
#     if serializer.is_valid():
#         # Access the validated data
#         combined_data = serializer.validated_data
#         serializer.data['isi'] = combined_data['model_contoh1']
#         serializer.data['deskripsi'] = combined_data['model_contoh2']

#         # Perform further operations or save the data
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CombinedView(APIView):
#     def post(self, request):
#         serializer = CombinedSerializer(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def uploadGambar(request, format=None):
#     permission_classes = [IsAuthenticated]
#     serializer = GambarSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
    
#     data_gambar = serializer.data["gambar"]
#     string_gambar = json.dumps(data_gambar)
#     gambar = str(string_gambar[2:-1]) 
    
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1]) 
        
#     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
#     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
#     url_gambar = srcURL_gambar + ".png"
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"

#     upload = Gambar(id=serializer.data["id"], gambar=serializer.data["gambar"], dokumen=serializer.data["dokumen"], gambar_url=serializer.data["gambar_url"], dok_url=serializer.data["dok_url"])
#     serializer = GambarSerializer(upload, data={'gambar_url': url_gambar, 'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(gambar)
#         os.remove(dok)
#         return Response(new_data)
    
#     return Response(serializer.data)

# @api_view(['GET'])
# def getGambar(request):
#     items = Gambar.objects.all()
#     serializer = GambarSerializer(items, many=True)
#     return Response(serializer.data) 

# @api_view(['PUT'])
# def editGambar(request, pk):
#     items = Gambar.objects.get(pk=pk)                  
#     serializer = GambarSerializer(items, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
        
#     data_gambar = serializer.data["gambar"]
#     string_gambar = json.dumps(data_gambar)
#     gambar = str(string_gambar[2:-1]) 
    
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1]) 
        
#     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
#     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
#     url_gambar = srcURL_gambar + ".png"
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"

#     serializer = GambarSerializer(items, data={'gambar_url': url_gambar, 'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(gambar)
#         os.remove(dok)
#         return Response(new_data)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#SAYANG DIBUANG SEBELUM FIX

#Produk Hukum
# def list(self, request, pk=None):
    #     items = ProdukHukum.objects.all()
    #     serializer = ProdukHukumSerializer(items, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk, *args, **kwargs):
    #     items = ProdukHukum.objects.get(pk=pk)
    #     serializer = ProdukHukumSerializer(items)
    #     return Response(serializer.data)

    # @parser_classes([MultiPartParser])
    # def create(self, request, *args, **kwargs):
    #     serializer = ProdukHukumSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
            
    #     data_dok = serializer.data["dokumen"]
    #     string_dok = json.dumps(data_dok)
    #     dok = str(string_dok[2:-1])
        
    #     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    #     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    #     url_dok = srcURL_dokumen + ".pdf"
        
    #     upload = ProdukHukum(id=serializer.data["id"], nama=serializer.data["nama"], kategori=serializer.data["kategori"], tahun=serializer.data["tahun"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
    #     serializer = ProdukHukumSerializer(upload, data={'dok_url': url_dok}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(dok)
    #         return Response(new_data)
        
    #     return Response(serializer.data)

    # def update(self, request, pk, *args, **kwargs):
    #     items = ProdukHukum.objects.get(pk=pk)                  
    #     serializer = ProdukHukumSerializer(items, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
        
    #     data_dok = serializer.data["dokumen"]
    #     string_dok = json.dumps(data_dok)
    #     dok = str(string_dok[2:-1]) 
        
    #     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    #     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    #     url_dok = srcURL_dokumen + ".pdf"

    #     serializer = ProdukHukumSerializer(items, data={'dok_url': url_dok}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(dok)
    #         return Response(new_data)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({
    #             "code": 200,
    #             "message": "data berhasil dihapus"
    #         },status=status.HTTP_204_NO_CONTENT)
    
    #Rapat Koordinasi
    # def list(self, request, pk=None):
#     items = RapatKoordinasi.objects.all()
#     serializer = RapatKoordinasiSerializer(items, many=True)
#     return Response(serializer.data)

# def retrieve(self, request, pk, *args, **kwargs):
#         items = RapatKoordinasi.objects.get(pk=pk)
#         serializer = RapatKoordinasiSerializer(items)
#         return Response(serializer.data)

# @parser_classes([MultiPartParser])
# def create(self, request, *args, **kwargs):
#     serializer = RapatKoordinasiSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
        
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1])
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"
    
#     upload = RapatKoordinasi(id=serializer.data["id"], nama=serializer.data["nama"], kategori=serializer.data["kategori"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
#     serializer = RapatKoordinasiSerializer(upload, data={'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(dok)
#         return Response(new_data)
    
#     return Response(serializer.data)

# def update(self, request, pk, *args, **kwargs):
#     items = RapatKoordinasi.objects.get(pk=pk)                  
#     serializer = RapatKoordinasiSerializer(items, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
    
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1]) 
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"

#     serializer = RapatKoordinasiSerializer(items, data={'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(dok)
#         return Response(new_data)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def destroy(self, request, *args, **kwargs):
#     instance = self.get_object()
#     self.perform_destroy(instance)
#     return Response({
#             "code": 200,
#             "message": "data berhasil dihapus"
#         },status=status.HTTP_204_NO_CONTENT)
    
    #Paparan
    # def list(self, request, pk=None):
#     items = Paparan.objects.all()
#     serializer = PaparanSerializer(items, many=True)
#     return Response(serializer.data)

# def retrieve(self, request, pk, *args, **kwargs):
#         items = Paparan.objects.get(pk=pk)
#         serializer = PaparanSerializer(items)
#         return Response(serializer.data)

# @parser_classes([MultiPartParser])
# def create(self, request, *args, **kwargs):
#     serializer = PaparanSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
        
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1])
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"
    
#     upload = Paparan(id=serializer.data["id"], nama=serializer.data["nama"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
#     serializer = PaparanSerializer(upload, data={'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(dok)
#         return Response(new_data)    
        
#     return Response(serializer.data)

# def update(self, request, pk, *args, **kwargs):
#     items = Paparan.objects.get(pk=pk)                  
#     serializer = PaparanSerializer(items, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
    
#     data_dok = serializer.data["dokumen"]
#     string_dok = json.dumps(data_dok)
#     dok = str(string_dok[2:-1]) 
    
#     cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
#     srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
#     url_dok = srcURL_dokumen + ".pdf"

#     serializer = PaparanSerializer(items, data={'dok_url': url_dok}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(dok)
#         return Response(new_data)
        
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({
#                 "code": 200,
#                 "message": "data berhasil dihapus"
#             },status=status.HTTP_204_NO_CONTENT)
    
    #Berita
    # def list(self, request, pk=None):
    #     items = Berita.objects.all()
    #     serializer = BeritaSerializer(items, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk, *args, **kwargs):
    #     items = Berita.objects.get(pk=pk)
    #     serializer = BeritaSerializer(items)
    #     return Response(serializer.data)

    # @parser_classes([MultiPartParser])
    # def create(self, request, *args, **kwargs):
    #     serializer = BeritaSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
            
    #     data_gambar = serializer.data["gambar"]
    #     string_gambar = json.dumps(data_gambar)
    #     gambar = str(string_gambar[2:-1])
        
    #     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    #     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    #     url_gambar = srcURL_gambar + ".png"

    #     upload = Berita(id=serializer.data["id"], judul=serializer.data["judul"], isi=serializer.data["isi"], gambar=serializer.data["gambar"], gambar_url=serializer.data["gambar_url"])
    #     serializer = BeritaSerializer(upload, data={'gambar_url': url_gambar}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(gambar)
    #         return Response(new_data)
         
    #     return Response(serializer.data)

    # def update(self, request, pk, *args, **kwargs):
    #     items = Berita.objects.get(pk=pk)                  
    #     serializer = BeritaSerializer(items, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
            
    #     data_gambar = serializer.data["gambar"]
    #     string_gambar = json.dumps(data_gambar)
    #     gambar = str(string_gambar[2:-1]) 
            
    #     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    #     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    #     url_gambar = srcURL_gambar + ".png"

    #     serializer = BeritaSerializer(items, data={'gambar_url': url_gambar}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(gambar)
    #         return Response(new_data)  
           
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({
    #             "code": 200,
    #             "message": "data berhasil dihapus"
    #         },status=status.HTTP_204_NO_CONTENT)
    
    #Fakta
    # def list(self, request, pk=None):
    #     items = Fakta.objects.all()
    #     serializer = FaktaSerializer(items, many=True)
    #     return Response(serializer.data)

    # # def retrieve(self, request, pk, *args, **kwargs):
    # #     items = Fakta.objects.get(pk=pk)
    # #     serializer = FaktaSerializer(items)
    # #     return Response(serializer.data)

    # @parser_classes([MultiPartParser])
    # def create(self, request, *args, **kwargs):
    #     serializer = FaktaSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
            
    #     data_gambar = serializer.data["gambar"]
    #     string_gambar = json.dumps(data_gambar)
    #     gambar = str(string_gambar[2:-1])
        
    #     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    #     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    #     url_gambar = srcURL_gambar + ".png"

    #     upload = Fakta(id=serializer.data["id"], judul=serializer.data["judul"], isi=serializer.data["isi"], gambar=serializer.data["gambar"], gambar_url=serializer.data["gambar_url"])
    #     serializer = FaktaSerializer(upload, data={'gambar_url': url_gambar}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(gambar)
    #         return Response(new_data)
         
    #     return Response(serializer.data)

    # def update(self, request, pk, *args, **kwargs):
    #     items = Fakta.objects.get(pk=pk)                  
    #     serializer = FaktaSerializer(items, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
            
    #     data_gambar = serializer.data["gambar"]
    #     string_gambar = json.dumps(data_gambar)
    #     gambar = str(string_gambar[2:-1]) 
            
    #     cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    #     srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    #     url_gambar = srcURL_gambar + ".png"

    #     serializer = FaktaSerializer(items, data={'gambar_url': url_gambar}, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         new_data = serializer.data
    #         os.remove(gambar)
    #         return Response(new_data)  
           
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({
    #             "code": 200,
    #             "message": "data berhasil dihapus"
    #         },status=status.HTTP_204_NO_CONTENT)

