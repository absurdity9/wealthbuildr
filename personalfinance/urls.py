from django.urls import path
from .import views
from .views  import index, create_user_profile, create_fmodel, create_income, create_expense, create_asset, create_profile_page

urlpatterns = [
    path('', views.index, name="index"),
    path('create_user_profile/', create_user_profile, name='create_user_profile'),
    path('create_fmodel/', create_fmodel, name='create_fmodel'),
    path('create_income/', create_income, name='create_income'),
    path('create_expense/', create_expense, name='create_expense'),
    path('create_asset/', create_asset, name='create_asset'),
    path('create_profile_page/', create_profile_page, name='create_profile_page'),

] 