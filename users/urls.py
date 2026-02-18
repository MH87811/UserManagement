from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', Register_View.as_view(), name='register'),
    path('login/', Login_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    # path('profile/', ProfileView, name='profile'),
    path('dashboard/', DashboardView, name='dashboard'),
]