from rest_framework import status,  permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
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



class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer



class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user.is_active = False
            user.create_activation_code()
            user.save()
            send_activation_code(user)
            return Response('Вам отправлено письмо', status=200)
        except CustomUser.DoesNotExist:
            return Response({'msg': 'User doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=200)

