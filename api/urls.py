from django.urls import path
from . import views
from api.views import LogoutView, RegisterView, MyObtainTokenPairView, ChangePasswordView, UpdateProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
     path('register/', RegisterView.as_view(), name='register'),
     path('login/', MyObtainTokenPairView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
     path('update_profile/<int:pk>/', views.editDetails, name='auth_update_profile'),
     path('ProdukHukum/', views.getProdukHukum),
     path('addProdukHukum/', views.addProdukHukum),
     path('editProdukHukum/<int:pk>/', views.editProdukHukum),
     path('deleteProdukHukum/<int:pk>/', views.deleteProdukHukum),
     path('RapatKoordinasi/', views.getRapatKoordinasi),
     path('addRapatKoordinasi/', views.addRapatKoordinasi),
     path('editRapatKoordinasi/<int:pk>/', views.editRapatKoordinasi),
     path('deleteRapatKoordinasi/<int:pk>/', views.deleteRapatKoordinasi),
     path('Paparan/', views.getPaparan),
     path('addPaparan/', views.addPaparan),
     path('editPaparan/<int:pk>/', views.editPaparan),
     path('deletePaparan/<int:pk>/', views.deletePaparan),
     path('Berita/', views.getBerita),
     path('addBerita/', views.addBerita),
     path('editBerita/<int:pk>/', views.editBerita),
     path('deleteBerita/<int:pk>/', views.deleteBerita),
]

