from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from user.send_mail import send_confirmation_email, send_activation_code
from .serializers import CreateNewPasswordSerializer

CustomUser = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = serializers.RegisterApiSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = CustomUser.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Activated'}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'msg': 'Link expired'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(CustomUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code.delay(user.email, user.activation_code)
        return Response('We sent a letter', status=200)


class ForgotPasswordComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully recovered your password', status=200)
