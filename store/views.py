from django.shortcuts import render

# Create your views here.
# views are Python functions that take http requests and return http response, like HTML documents.

from rest_framework import viewsets
from .models import Customer, Product, Order
from .serializers import CustomersSerializer, ProductsSerializer, OrdersSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer