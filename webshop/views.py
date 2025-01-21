from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from .serializers import OrderSerializer
from .models import Order

class ProductViewSet(viewsets.ModelViewSet):
    # API Endpoint for Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer