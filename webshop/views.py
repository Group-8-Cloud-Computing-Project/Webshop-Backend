from rest_framework import viewsets, status
from .serializers import ProductSerializer, PaymentSerializer
from .models import Product
from .serializers import OrderSerializer
from .models import Order
import random
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment
from .serializers import InventorySerializer
from .models import Inventory
from django.core.mail import send_mail
from .serializers import EmailNotificationSerializer
from .models import EmailNotification

def send_order_confirmation(order):
    """
    Sends an order confirmation to the customer.
    """
    try:
        send_mail(
            subject=f"Order Confirmation - #{order.id}",
            message=f"Dear {order.customer_name},\n\n"
                    f"Thank you for your order!\n"
                    f"Order ID: #{order.id}\n"
                    f"Total Price: ${order.total_price}\n\n"
                    f"We will notify you once your order is shipped.\n\n"
                    f"Best regards,\nWebshop Team",
            from_email="no-reply@webshop.com",
            recipient_list=[order.customer_email],
            fail_silently=False,
        )
        print(f"Order confirmation email sent to {order.customer_email}.")
    except Exception as e:
        print(f"Error sending order confirmation email: {e}")

def send_shipping_notification(order):
    """
    Sends a shipping notification to the customer.
    """
    try:
        send_mail(
            subject=f"Shipping Notification - #{order.id}",
            message=f"Dear {order.customer_name},\n\n"
                    f"Your order (ID: #{order.id}) has been shipped.\n\n"
                    f"Thank you for shopping with us!\n\n"
                    f"Best regards,\nWebshop Team",
            from_email="no-reply@webshop.com",
            recipient_list=[order.customer_email],
            fail_silently=False,
        )
        print(f"Shipping notification email sent to {order.customer_email}.")
    except Exception as e:
        print(f"Error sending shipping notification email: {e}")

class ProductViewSet(viewsets.ModelViewSet):
    # API Endpoint for Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        """
        Send email confirmation after order creation.
        """
        order = serializer.save()
        send_order_confirmation(order)

    def perform_update(self, serializer):
        """
        Send email notifications when status changes.
        """
        order = serializer.save()
        if order.status == "SHIPPED":
            send_shipping_notification(order)

class InventoryViewSet(viewsets.ModelViewSet):
    # API Endpoint for Inventory
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class EmailNotificationViewSet(viewsets.ModelViewSet):

    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer

    def perform_create(self, serializer):
        """
        Override to send email when a notification is created.
        """
        email = serializer.save()
        try:
            send_mail(
                subject=email.subject,
                message=email.message,
                from_email='no-reply@webshop.com',
                recipient_list=[email.recipient],
            )
            email.status = 'SENT'
        except Exception as e:
            email.status = 'FAILED'
        email.save()



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