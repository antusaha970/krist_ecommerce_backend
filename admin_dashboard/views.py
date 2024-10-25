from rest_framework.decorators import api_view
from rest_framework.response import Response
from order.models import Order
from account.models import Account
from product.models import Product


@api_view(['GET'])
def admin_overview(request):
    total_order = Order.objects.count()
    total_account = Account.objects.count()
    total_product = Product.objects.count()

    return Response({'total_order': total_order, 'total_account': total_account, 'total_product': total_product})
