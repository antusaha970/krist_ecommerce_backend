from rest_framework.views import APIView
from .models import Cart
from .serializers import CartSerializer, CartToDisplaySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes


class CartView(APIView):
    """This class handles the cart functionality"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This method used to create cart"""
        account = request.user
        data = request.data
        data['account'] = account.id
        serializer = CartSerializer(data=data, many=False)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            is_already_exist = Cart.objects.filter(
                product=product, account=account).exists()
            if is_already_exist:
                return Response(status=status.HTTP_304_NOT_MODIFIED)

            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """This method is used to retrieve cart product for specific account"""
        account = request.user
        data = Cart.objects.filter(account=account)
        serializer = CartToDisplaySerializer(data, many=True)
        return Response(serializer.data)

    def delete(self, request, product_id=None):
        """Delete a cart product by product id"""
        account = request.user

        cart_obj = get_object_or_404(
            Cart, account=account, product__id=product_id)
        cart_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_all_cart_products(request):
    account = request.user
    cart_product = Cart.objects.filter(account=account)
    cart_product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
