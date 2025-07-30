from django.contrib import admin
from django.urls import path, include
from apps.products import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_products, name='search_products'),
    path('search/results/', views.search_results, name='search_results'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/buy/', views.buy_cart, name='buy_cart'),
    path('add/', views.add_product, name='add_product'),
]