from .serializers import ClientMessageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from order.models import Order
from account.models import Account
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework import viewsets, permissions
from .models import ClientMessage
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ClientMessageViewSet(viewsets.ModelViewSet):
    queryset = ClientMessage.objects.all()
    serializer_class = ClientMessageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]


@api_view(['GET'])
def admin_overview(request):
    total_order = Order.objects.count()
    total_account = Account.objects.count()
    total_product = Product.objects.count()

    return Response({'total_order': total_order, 'total_account': total_account, 'total_product': total_product})


@api_view(['GET'])
def admin_latest_products(request):
    recent_products = cache.get("recent_products")
    if recent_products is None:
        recent_products = Product.objects.order_by("-created_on")[:5]
        cache.set("recent_products", recent_products, timeout=60*3)
    serializer = ProductSerializer(recent_products, many=True)
    return Response(serializer.data)
