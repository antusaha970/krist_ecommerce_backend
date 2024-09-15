from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryAddress, OrderItem, Order
from .serializers import DeliveryAddressSerializer, OrderSerializer, OrderDisplaySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from product.models import Product
from rest_framework import status
from account.models import Account
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
import environ
env = environ.Env()
environ.Env.read_env()


stripe.api_key = env("STRIPE_SECRET_KEY")


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}/"


class OrderWithCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        YOUR_DOMAIN = get_current_host(request)
        account = request.user
        data = request.data
        data['account'] = account.email

        items = data['items']
        total_money = 0
        for item in items:
            pd = get_object_or_404(Product, pk=item['product'])
            total_money += (pd.price*item['quantity'])

        data['items'] = json.dumps(items)

        checkout_order_items = [{
            'price_data': {
                'currency': 'USD',
                'product_data': {
                    'name': "Total price of the t-shirts after discount",
                    'metadata': data
                },
                'unit_amount': int(total_money * 100)
            },
            'quantity': 1,
        }]

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=checkout_order_items,
            customer_email=account.email,
            mode='payment',
            success_url=f"{YOUR_DOMAIN}/api/orders/successful-payment/",
            cancel_url=f"{YOUR_DOMAIN}?cancel=true",
            metadata=data
        )

        return Response({'session_url': session.url})


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    """This is stripe webhook which will be called when a successful payment happens and create a book property object in database"""
    STRIPE_WEBHOOK_KEY = 'whsec_yhnZ7yQGTBKaVRobGDQ33P8AjN5PQTof'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_KEY)
    except ValueError as e:
        print('Value error ', e)
        return Response({'errors': "Invalid Payload"}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature ", e)
        return Response({'errors': "Invalid Signature"}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        data = session['metadata']

        items = json.loads(data['items'])
        account_email = data.pop('account', None)
        account = Account.objects.get(email=account_email)
        data['items'] = items
        print(items)
        print(data)
        print(account)

        order_items = []
        for pd in items:
            product = get_object_or_404(Product, pk=pd['product'])
            if product.stock < pd['quantity']:
                return Response({"errors": f"Not enough stock for product: {product.title}"})
            product.stock -= pd['quantity']
            product.save(update_fields=['stock'])
            new_order_item = OrderItem.objects.create(
                product=product, quantity=pd['quantity'])
            order_items.append(new_order_item.id)

        orderData = data
        orderData['account'] = account.id
        orderData['items'] = order_items
        orderData['payment_status'] = "paid"
        orderData['payment_mode'] = "CARD"
        serializer = OrderSerializer(data=orderData, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    print("unhandled event")
    return Response({'details': "Unhandled event"}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user
        return DeliveryAddress.objects.filter(account=account)

    def perform_create(self, serializer):
        account = self.request.user
        serializer.save(account=account)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user
        print("account: ", account)
        data = request.data
        print(data)
        items = data.pop('items')
        print(items)
        order_items = []
        for pd in items:
            product = get_object_or_404(Product, pk=pd['product'])
            if product.stock < pd['quantity']:
                return Response({"errors": f"Not enough stock for product: {product.title}"})
            product.stock -= pd['quantity']
            product.save(update_fields=['stock'])
            new_order_item = OrderItem.objects.create(
                product=product, quantity=pd['quantity'])
            order_items.append(new_order_item.id)

        print("Order items: ", order_items)
        orderData = data
        orderData['account'] = account.id
        orderData['items'] = order_items
        serializer = OrderSerializer(data=orderData, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        account = request.user
        orders = Order.objects.filter(account=account)
        serializer = OrderDisplaySerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def successful_payment(request):
    return render(request, 'successfulPayment.html')
