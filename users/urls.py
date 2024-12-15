from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Any custom views
from .views import csrf_token_view
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), 
    path('csrf/', csrf_token_view, name='csrf_token'), 
]
