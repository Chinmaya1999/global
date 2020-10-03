from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('forgotPassword', auth_views.PasswordResetView.as_view(template_name='./globalCert/forgotPassword.html'), name='forgotPassword'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='./globalCert/forgotPassword.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact', views.contact, name='contact'),
    path('viewCert', views.viewCert, name='viewCert'),
    path('handleLogout',views.handleLogout,name='handleLogout'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(),name='activate'),
    path('set-new-password/<uidb64>/<token>', views.SetNewPasswordView.as_view(),name='set-new-password'),


]
