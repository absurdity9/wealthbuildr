from django.urls import path
from .import views
from .views  import index, create_user_profile, create_fmodel, create_income, create_expense, create_assets, create_profile_page, register_view, login_view, edit_fmodel
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
    path('edit_fmodel/<int:fmodel_id>/', views.edit_fmodel, name='edit_fmodel'),
    path('add/', views.add, name='add'),
    path('get_fmodel_data/<int:fmodel_id>/', views.get_fmodel_data, name='get_fmodel_data'),
    path('pages/<slug:slug>/', views.published_page_view, name='published_page'),
    path('publish/', views.create_or_update_published_page, name='create_or_update_published_page'),
    path('check-published-page/<int:fmodel_id>/', views.check_published_page, name='check_published_page'),
    path('toggle_public/', views.toggle_public, name='toggle_public'),
    ] 