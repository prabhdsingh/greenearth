from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include, reverse_lazy
from apps.accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html'
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('history/', views.user_history_view, name='user_history'),
    path('contact_us/', views.contact_us, name='contact_us'),
]