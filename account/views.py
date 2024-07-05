from rest_framework.views import APIView
from .serializers import AccountSerializer, AccountUpdateSerializer
from .models import Account, AccountPasswordResetProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from random import randint
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


class AccountRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        """This method do registration for an account with valid information"""
        data = request.data
        serializer = AccountSerializer(data=data, many=False)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            response_data = {
                'user': serializer.data,
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = AccountUpdateSerializer(
            instance=user, data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = AccountUpdateSerializer(
            instance=user, data=data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'details': "Account deleted"}, status=status.HTTP_204_NO_CONTENT)


class AccountLoginView(APIView):
    def post(self, request, *args, **kwargs):
        """This method do login with credentials"""
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            return Response({'email': 'This field is required', 'password': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            serializer = AccountSerializer(user, many=False)
            response_data = {
                'user': serializer.data,
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"errors": "No users found with the given credentials"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def send_forgot_password(request):
    """This function send the OTP to user mail for forgot password"""
    data = request.data
    email = data.get('email')
    if email is None:
        return Response({"errors": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    account = get_object_or_404(Account, email=email)

    OTP = randint(100000, 999999)
    expire_time = datetime.now()+timedelta(minutes=30)

    account.ResetPassword.reset_password_otp = OTP
    account.ResetPassword.reset_password_expire = expire_time

    account.ResetPassword.save()

    message = f"Your password reset OTP is {OTP}."
    send_mail("Password Reset OTP for Krist e-commerce",
              message, "noreply@gmail.com", [email])

    return Response({"details": "password reset OTP has been sent successfully"})


@api_view(["POST"])
def reset_password_using_otp(request):
    data = request.data
    email = data.get("email")
    otp = data.get("OTP")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if email is None or password is None or confirm_password is None:
        return Response({"details": "Email,password,confirm password is required"}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"details": "Passwords did not match"}, status=status.HTTP_400_BAD_REQUEST)

    if otp is None:
        return Response({"details": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)

    passwordResetProfile = get_object_or_404(
        AccountPasswordResetProfile, reset_password_otp=otp)

    expire_time = passwordResetProfile.reset_password_expire.replace(
        tzinfo=None)

    if expire_time < datetime.now():
        return Response({"details": "OTP expired"}, status=status.HTTP_403_FORBIDDEN)

    account = passwordResetProfile.account

    account.password = make_password(password)
    account.save()

    passwordResetProfile.reset_password_otp = None
    passwordResetProfile.reset_password_expire = None
    passwordResetProfile.save()

    return Response({"details": "Password changed successful"}, status=status.HTTP_200_OK)
