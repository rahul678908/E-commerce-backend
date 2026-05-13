from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

import random

from django.contrib.auth import get_user_model

User = get_user_model()

# STORE OTP TEMPORARILY
otp_storage = {}


# GENERATE JWT TOKENS
def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# CUSTOMER REGISTER
class CustomerRegisterView(APIView):

    def post(self, request):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # CHECK USERNAME
        if User.objects.filter(username=username).exists():

            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # CHECK EMAIL
        if User.objects.filter(email=email).exists():

            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({
            'message': 'Customer registered successfully'
        }, status=status.HTTP_201_CREATED)


# CUSTOMER LOGIN
class CustomerLoginView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None and not user.is_superuser:

            tokens = get_tokens_for_user(user)

            return Response({
                'message': 'Login successful',
                'tokens': tokens,
                'user_id': user.id,
                'username': user.username,
            })

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


# FORGOT PASSWORD - SEND OTP
class ForgotPasswordView(APIView):

    def post(self, request):

        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response({
                'error': 'Email not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # GENERATE OTP
        otp = random.randint(100000, 999999)

        # STORE OTP
        otp_storage[email] = otp

        # SEND EMAIL
        send_mail(
            'Password Reset OTP',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({
            'message': 'OTP sent to email'
        })


# VERIFY OTP + RESET PASSWORD
class ResetPasswordView(APIView):

    def post(self, request):

        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        # CHECK OTP
        if email not in otp_storage:

            return Response({
                'error': 'OTP not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        if str(otp_storage[email]) != str(otp):

            return Response({
                'error': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # SET NEW PASSWORD
        user.set_password(new_password)
        user.save()

        # REMOVE OTP
        del otp_storage[email]

        return Response({
            'message': 'Password reset successful'
        })