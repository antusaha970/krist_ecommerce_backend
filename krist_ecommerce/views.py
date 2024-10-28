from rest_framework.decorators import api_view
from django.shortcuts import render


@api_view(['GET'])
def homePage(request):
    return render(request, 'homePage.html')
