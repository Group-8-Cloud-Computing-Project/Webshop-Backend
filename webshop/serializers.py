from rest_framework import serializers
from .models import Product, Category
from .models import Order
from .models import MockPayment
from .models import Inventory
from .models import EmailNotification

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),  # Needed for write operations
        slug_field='name'
    )
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for Inventory model
    """
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = '__all__'

    def get_is_low_stock(self, obj):
        """
        Method to dynamically generate the `is_low_stock` field.
        """
        return obj.is_low_stock()

class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MockPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockPayment
        fields = "__all__"