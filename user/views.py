from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from user.send_mail import send_confirmation_email 

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


<<<<<<< HEAD
=======
    
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
>>>>>>> 9d90a02bab683a1ae2a7b952301031832d4bae77

