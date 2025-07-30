from django.contrib import admin
from django.urls import path, include
from apps.accounts import views
from apps.orders import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('my_orders/', views.my_orders, name='my_orders'),
]