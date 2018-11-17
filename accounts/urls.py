from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
# from django.contrib.auth.views import *

from accounts import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # login
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    # do  logout-then-redirect
    path('logout-then-login/', logout_then_login, name='logout_then_login'),

    # password
    path('password-change/',
         PasswordChangeView.as_view(template_name='accounts/registration/password_change_form.html'),
         name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name='accounts/registration/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(template_name='accounts/registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_complete.html'),
         name='password_reset_complete'),

    # user &profile
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit')
]
