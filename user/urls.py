from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from user.apps import UserConfig
from user.views import RegisterView, ProfileView, email_verification, reset

app_name = UserConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('reset/', reset, name='reset'),

]
