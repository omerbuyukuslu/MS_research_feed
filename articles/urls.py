from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token  # For token-based authentication
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.homepage, name='homepage'),  # Home page view
    path('api/articles/', views.article_feed, name='article_feed'),  # API endpoint for articles
    path('api/login/', obtain_auth_token, name='api_login'),  # Login endpoint
    path('update-articles/', views.update_articles, name='update_articles'),
    path('api/stream-output/', views.stream_output, name='stream_output'),
    
]
