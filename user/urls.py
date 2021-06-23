from django.urls import path

from . import views



urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view(), name='activation_code'),
    path('forgot_password/<str:email>/', views.ForgotPassword.as_view()),
    path('forgot_password_complete/', views.ForgotPasswordComplete.as_view()),
]