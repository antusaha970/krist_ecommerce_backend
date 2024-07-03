from rest_framework.views import APIView
from .serializers import AccountSerializer
from .models import Account
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class AccountView(APIView):
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
