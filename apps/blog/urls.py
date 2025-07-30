from django.urls import path
from apps.blog import views

urlpatterns = [
    path('create/', views.create_blog, name='create_blog'),
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    # API endpoints
    path('api/blogs/', views.api_blog_list, name='api_blog_list'),
    path('api/blogs/<int:blog_id>/', views.api_blog_detail, name='api_blog_detail'),
]