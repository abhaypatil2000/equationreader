

from .views import *
from django.urls import path,include
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [

    path('' , login_attempt , name="login"),
    path('register' , register , name="register"),
    path('otp' , otp , name="otp"),
    path('login-otp', login_otp , name="login_otp"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
]