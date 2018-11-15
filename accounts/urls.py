from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import logout_then_login
# from django.contrib.auth.views import *

from accounts import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    # do  logout-then-redirect
    path('logout-then-login/', logout_then_login, name='logout_then_login'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit')
]
