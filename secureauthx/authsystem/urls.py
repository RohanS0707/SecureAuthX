from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'), 
    path('register/',views.register,name='register'),
    path('forgot_password/',views.forgot_password,name='forgot_password'), 
    path('verify-otp/', views.verify_otp, name='verify_otp'),# To be built next
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-verify-otp/', views.reset_verify_otp, name='reset_verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

]
