from django.urls import path
from .import views
from .views  import index, create_user_profile, create_fmodel

urlpatterns = [
    path('', views.index, name="index"),
    path('create_user_profile/', create_user_profile, name='create_user_profile'),
    path('create_fmodel/', create_fmodel, name='create_fmodel'),
] 