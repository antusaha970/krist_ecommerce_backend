from rest_framework.views import APIView
from .serializers import AccountSerializer
from .models import Account
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AccountView(APIView):
    def post(self, request, *args, **kwargs):
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
