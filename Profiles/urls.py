from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('profile/doctor/', views.profile, name='doctor_profile'),
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.users_details, name='user_details'),
    path('users/<int:user_id>/diagnose/', views.diagnose, name='diagnose'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:doctor_id>', views.doctor_details, name='doctor-details'),
    path('doctors/<int:doctor_id>/ask/', views.ask, name='ask'),
]