from rest_framework import serializers
from .models import Customer, Product, Order

# serializer converts data between Python objects and JSON (or other formats) for your API

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'