from django.urls import path
from .import views
from .views  import index, create_user_profile, create_fmodel, create_income, create_expense, create_assets, create_profile_page, register_view, login_view, edit_fmodel_name
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('create_user_profile/', create_user_profile, name='create_user_profile'),
    path('create_fmodel/', create_fmodel, name='create_fmodel'),
    path('create_income/', create_income, name='create_income'),
    path('create_expense/', create_expense, name='create_expense'),
    path('create_assets/', create_assets, name='create_assets'),
    path('create_profile_page/', create_profile_page, name='create_profile_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'), 
    path('edit_fmodel_name/<int:fmodel_id>/', views.edit_fmodel_name, name='edit_fmodel_name'),
] 