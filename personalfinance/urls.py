from django.urls import path
from .views import create_user_profile

urlpatterns = [
    path('create_user_profile/', create_user_profile, name='create_user_profile'),
]