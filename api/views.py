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
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from base.models import ProdukHukum, RapatKoordinasi, Paparan, Berita, Akun, Details
from .serializers import ProdukHukumSerializer, RapatKoordinasiSerializer, PaparanSerializer, BeritaSerializer, AkunSerializer, TokenPairSerializer, RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, DetailsSerializer
from rest_framework import status, generics, permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    
@api_view(['POST'])
@parser_classes([MultiPartParser])
def register(request):
    serializer = AkunSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    data_password = serializer.data["password"]
    string_password = json.dumps(data_password)
    password = str(string_password[1:-1])
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()    
    
    regist = Akun(id=serializer.data["id"], nik=serializer.data["nik"], telepon=serializer.data["telepon"], username=serializer.data["username"], email=serializer.data["email"], password=serializer.data["password"], nama_lengkap=serializer.data["nama_lengkap"])
    serializer = AkunSerializer(regist, data={'password': hashed_password}, partial=True)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    data_password = request.data.get('password')
    string_password = json.dumps(data_password)
    password = str(string_password[1:-1])
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # user = Akun.objects.get(username=username)
    # hashed_password = check_password(password, user.password)
    
    valid_username= Akun.objects.filter(username=username).first()
    valid_password = Akun.objects.filter(password=hashed_password).first()
    if valid_username and valid_password:
        refresh = RefreshToken.for_user(valid_username)
        serializer = TokenPairSerializer({'access': str(refresh.access_token), 'refresh': str(refresh)})
        return Response(serializer.data)
    return HttpResponse({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    # return Response(str(hashed_password))

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

@api_view(['PUT'])
@parser_classes([MultiPartParser])
def editDetails(request, pk):
    items = Details.objects.get(pk=pk)                  
    serializer = DetailsSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    data_foto_profil = serializer.data["foto_profil"]
    string_foto_profil = json.dumps(data_foto_profil)
    foto_profil = str(string_foto_profil[2:-1])
    
    cloudinary.uploader.upload(foto_profil, public_id=foto_profil, unique_filename = False, overwrite=True)
    srcURL_foto_profil = cloudinary.CloudinaryImage(foto_profil).build_url()
    url_foto_profil = srcURL_foto_profil + ".png"

    upload = Details(id=serializer.data["id"], nik=serializer.data["nik"], telepon=serializer.data["telepon"], nama_lengkap=serializer.data["nama_lengkap"], foto_profil=serializer.data["foto_profil"], foto_profil_url=serializer.data["foto_profil_url"])
    serializer = DetailsSerializer(upload, data={'foto_profil_url': url_foto_profil}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(foto_profil)
        return Response(new_data)    
        
    return Response(serializer.data)

# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CustomTokenObtainPairSerializer

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def registerAkun(request):
#     serializer = AkunSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
        
#     data_fp = serializer.data["foto_profil"]
#     string_fp = json.dumps(data_fp)
#     fp = str(string_fp[2:-1])
    
#     cloudinary.uploader.upload(fp, public_id=fp, unique_filename = False, overwrite=True)
#     srcURL_fp = cloudinary.CloudinaryImage(fp).build_url()
#     url_fp = srcURL_fp + ".png"
    
#     upload = Akun(nik=serializer.data["nik"], nama=serializer.data["nama"], telepon=serializer.data["telepon"], email=serializer.data["email"], password=serializer.data["password"], username=serializer.data["username"], foto_profil=serializer.data["foto_profil"], foto_profil_url=serializer.data["foto_profil_url"], is_superadmin=serializer.data["is_superadmin"], is_adminsi=serializer.data["is_adminsi"], is_kumkm=serializer.data["is_kumkm"])
#     serializer = AkunSerializer(upload, data={'foto_profil_url': url_fp}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         new_data = serializer.data
#         os.remove(fp)
#         return Response(new_data)
    
#     return Response(serializer.data)

@api_view(['GET'])
def getProdukHukum(request):
    items = ProdukHukum.objects.all()
    serializer = ProdukHukumSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def addProdukHukum(request):
    serializer = ProdukHukumSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1])
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"
    
    upload = ProdukHukum(id=serializer.data["id"], nama=serializer.data["nama"], kategori=serializer.data["kategori"], tahun=serializer.data["tahun"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
    serializer = ProdukHukumSerializer(upload, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)
    
    return Response(serializer.data)

@api_view(['PUT'])
def editProdukHukum(request, pk):
    items = ProdukHukum.objects.get(pk=pk)                  
    serializer = ProdukHukumSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1]) 
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"

    serializer = ProdukHukumSerializer(items, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProdukHukum(request, pk):
    items = ProdukHukum.objects.get(pk=pk)
    items.delete()
    return Response('ok')

@api_view(['GET'])
def getRapatKoordinasi(request):
    items = RapatKoordinasi.objects.all()
    serializer = RapatKoordinasiSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def addRapatKoordinasi(request):
    serializer = RapatKoordinasiSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1])
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"
    
    upload = RapatKoordinasi(id=serializer.data["id"], nama=serializer.data["nama"], kategori=serializer.data["kategori"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
    serializer = RapatKoordinasiSerializer(upload, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)
    
    return Response(serializer.data)

@api_view(['PUT'])
def editRapatKoordinasi(request, pk):
    items = RapatKoordinasi.objects.get(pk=pk)                  
    serializer = RapatKoordinasiSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1]) 
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"

    serializer = RapatKoordinasiSerializer(items, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteRapatKoordinasi(request, pk):
    items = RapatKoordinasi.objects.get(pk=pk)
    items.delete()
    return Response('ok')

@api_view(['GET'])
def getPaparan(request):
    items = Paparan.objects.all()
    serializer = PaparanSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def addPaparan(request):
    serializer = PaparanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1])
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"
    
    upload = Paparan(id=serializer.data["id"], nama=serializer.data["nama"], dokumen=serializer.data["dokumen"], dok_url=serializer.data["dok_url"])
    serializer = PaparanSerializer(upload, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)    
        
    return Response(serializer.data)

@api_view(['PUT'])
def editPaparan(request, pk):
    items = Paparan.objects.get(pk=pk)                  
    serializer = PaparanSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    data_dok = serializer.data["dokumen"]
    string_dok = json.dumps(data_dok)
    dok = str(string_dok[2:-1]) 
    
    cloudinary.uploader.upload(dok, public_id=dok, unique_filename = False, overwrite=True)
    srcURL_dokumen = cloudinary.CloudinaryImage(dok).build_url()
    url_dok = srcURL_dokumen + ".pdf"

    serializer = PaparanSerializer(items, data={'dok_url': url_dok}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(dok)
        return Response(new_data)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletePaparan(request, pk):
    items = Paparan.objects.get(pk=pk)
    items.delete()
    return Response('ok')

@api_view(['GET'])
def getBerita(request):
    items = Berita.objects.all()
    serializer = BeritaSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def addBerita(request):
    serializer = BeritaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    data_gambar = serializer.data["gambar"]
    string_gambar = json.dumps(data_gambar)
    gambar = str(string_gambar[2:-1])
    
    cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    url_gambar = srcURL_gambar + ".png"

    upload = Berita(id=serializer.data["id"], judul=serializer.data["judul"], isi=serializer.data["isi"], gambar=serializer.data["gambar"], gambar_url=serializer.data["gambar_url"])
    serializer = BeritaSerializer(upload, data={'gambar_url': url_gambar}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(gambar)
        return Response(new_data)    
        
    return Response(serializer.data)

@api_view(['PUT'])
def editBerita(request, pk):
    items = Berita.objects.get(pk=pk)                  
    serializer = BeritaSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
        
    data_gambar = serializer.data["gambar"]
    string_gambar = json.dumps(data_gambar)
    gambar = str(string_gambar[2:-1]) 
        
    cloudinary.uploader.upload(gambar, public_id=gambar, unique_filename = False, overwrite=True)
    srcURL_gambar = cloudinary.CloudinaryImage(gambar).build_url()
    url_gambar = srcURL_gambar + ".png"

    serializer = BeritaSerializer(items, data={'gambar_url': url_gambar}, partial=True)
    if serializer.is_valid():
        serializer.save()
        new_data = serializer.data
        os.remove(gambar)
        return Response(new_data)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBerita(request, pk):
    items = Berita.objects.get(pk=pk)
    items.delete()
    return Response('ok')

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

