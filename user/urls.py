from django.urls import path

from . import views
from .views import ForgotPassword, ForgotPasswordComplete

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view(), name='activation_code'),
    path('forgot_password/', ForgotPassword.as_view()),
    path('forgot_password_complete/', ForgotPasswordComplete.as_view()),

]

