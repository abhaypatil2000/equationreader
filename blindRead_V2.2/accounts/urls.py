from django.urls import path, re_path, include
from django.contrib.auth import login, views as auth_views
from accounts import views
from accounts.forms import UserLoginForm
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm), name='login'),
    re_path(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
]
