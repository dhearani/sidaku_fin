from django.urls import path
from . import views
from api.views import LogoutView, MyObtainTokenPairView, GrafikKUMKMView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
     path('login/', MyObtainTokenPairView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('pie-chart/', GrafikKUMKMView.as_view()),
]

