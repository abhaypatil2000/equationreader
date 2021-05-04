

from .views import *
from django.urls import path,include
from django.contrib.auth import views as auth_views

app_name = 'interface'

urlpatterns = [
    path('common', CommonBooksView.as_view(), name='common')
]