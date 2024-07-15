# serializers.py
from rest_framework import serializers
from .models import Producto, Carrito, Ticket, PurchaseReceipt

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class PurchaseReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReceipt
        fields = '__all__'
