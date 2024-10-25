from rest_framework.views import APIView
from .models import WishList
from .serializers import WishListSerializer, WishListForDisplaySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class WishListView(APIView):
    """This class creates wishlist items for logged in users"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all wishlist items for logged in users"""
        user = request.user
        all_wishlist_data = WishList.objects.filter(account=user)
        serializer = WishListForDisplaySerializer(
            all_wishlist_data, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """Add wishlist items for logged in users"""
        user = request.user
        data = request.data
        data['account'] = user.id
        serializer = WishListSerializer(data=data, many=False)

        if serializer.is_valid():
            products = serializer.validated_data['products']
            is_already_exits_same_product = WishList.objects.filter(
                account=user, products=products).exists()

            if is_already_exits_same_product:
                return Response({'statusCode': status.HTTP_304_NOT_MODIFIED, 'message': "Already added"})

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def delete(self, request, pk=None):
        """delete wishlist items for logged in users"""
        account = request.user

        wishlistItem = get_object_or_404(WishList, account=account, pk=pk)
        wishlistItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
