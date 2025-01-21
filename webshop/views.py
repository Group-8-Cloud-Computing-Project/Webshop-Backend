from rest_framework import viewsets, status
from .serializers import ProductSerializer, PaymentSerializer
from .models import Product
from .serializers import OrderSerializer
from .models import Order
import random
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment

class ProductViewSet(viewsets.ModelViewSet):
    # API Endpoint for Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewSet(viewsets.ViewSet):
    """
        Simulated payment processing
    """

    def initiate_payment(self, request):
        """
            Simulates a payment transaction
        """
        data = request.data
        amount = data.get('amount')
        order_id = data.get('order_id')
        user_id = data.get('user_id')

        # Simulate payment (successful or failed)
        status_choice = random.choice(['success', 'failed'])

        # Create a Payment object (Mock)
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            status=status_choice
        )

        # Use the serializer
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def verify_payment(self, request, pk=None):
        """
            Checks the status of a simulated payment
        """
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
            )