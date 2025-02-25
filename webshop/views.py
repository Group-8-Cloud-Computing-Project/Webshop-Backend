from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .serializers import ProductSerializer, InventorySerializer
from .models import Product
from .serializers import OrderSerializer
from .models import Order
from rest_framework.response import Response
from .models import Inventory
from django.core.mail import send_mail
from .serializers import EmailNotificationSerializer
from .models import EmailNotification
from .serializers import MockPaymentSerializer
from .models import MockPayment

def send_order_confirmation(order):
    """
    Sends an order confirmation to the customer.
    """
    email = EmailNotification.objects.create(
        recipient=order.customer_email,
        subject=f"Order Confirmation - #{order.id}",
        message=f"Dear {order.customer_name},\n\n"
                f"Thank you for your order!\n"
                f"Order ID: #{order.id}\n"
                f"Total Price: ${order.total_price}\n\n"
                f"We will notify you once your order is shipped.\n\n"
                f"Best regards,\nWebshop Team",
    )

    try:
        send_mail(
            subject=email.subject,
            message=email.message,
            from_email="no-reply@webshop.com",
            recipient_list=[email.recipient],
            fail_silently=False,
        )
        email.status = "SENT"
        print(f"Order confirmation email sent to {order.customer_email}.")
    except Exception as e:
        print(f"Error sending order confirmation notification email: {e}")
        email.status = "FAILED"
    email.save()

def send_shipping_notification(order):
    """
    Sends a shipping notification to the customer.
    """
    email = EmailNotification.objects.create(
        recipient=order.customer_email,
        subject=f"Shipping Notification - #{order.id}",
        message=f"Dear {order.customer_name},\n\n"
                f"Your order (ID: #{order.id}) has been shipped.\n\n"
                f"Thank you for shopping with us!\n\n"
                f"Best regards,\nWebshop Team",
    )

    try:
        send_mail(
            subject=email.subject,
            message=email.message,
            from_email="no-reply@webshop.com",
            recipient_list=[email.recipient],
            fail_silently=False,
        )
        email.status = "SENT"
        print(f"Shipping notification email sent to {order.customer_email}.")
    except Exception as e:
        print(f"Error sending shipping notification email: {e}")
        email.status = "FAILED"
    email.save()

def send_low_stock_email(product_name, quantity):
    """
    Sends a notification to the admin when a product's stock is low.
    """
    email = EmailNotification.objects.create(
        recipient="admin@webshop.com",
        subject=f"Low Stock Alert: {product_name}",
        message=f"Stock for {product_name} is low ({quantity} left). Consider restocking.",
    )

    try:
        send_mail(
            subject=email.subject,
            message=email.message,
            from_email='no-reply@webshop.com',
            recipient_list=[email.recipient],
            fail_silently=False,
        )
        email.status = 'SENT'
    except Exception as e:
        print(f"{e}")
        email.status = 'FAILED'
    email.save()
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        """
        Send email notifications when status to SHIPPED changes.
        """
        order = serializer.save()
        if order.status == "COMPLETED":
            send_order_confirmation(order)
        elif order.status == "SHIPPED":
            send_shipping_notification(order)

class InventoryViewSet(viewsets.ModelViewSet):
    # API Endpoint for Inventory
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def perform_update(self, serializer):
        """
        Send email notifications when status to SHIPPED changes.
        """
        inventory = serializer.save()
        if inventory.is_low_stock():
            send_low_stock_email(inventory.product.name, inventory.quantity)

class EmailNotificationViewSet(viewsets.ModelViewSet):

    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer

class MockPaymentViewSet(viewsets.ModelViewSet):
    queryset = MockPayment.objects.all()
    serializer_class = MockPaymentSerializer

class MockPaymentWebhookView(APIView):
    def post(self, request, *args, **kwargs):

            payment_id = request.data.get("payment_id")
            status_update = request.data.get("status", "PENDING")

            if not payment_id:
                return Response({"error": "Missing payment_id"}, status=status.HTTP_400_BAD_REQUEST)

            if status_update not in ["COMPLETED", "FAILED", "PENDING"]:
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                payment = MockPayment.objects.get(payment_id=payment_id)
            except MockPayment.DoesNotExist:
                return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

            with transaction.atomic():

                payment.status = status_update
                payment.save()

                if payment.status == "COMPLETED":
                    if not payment.order:
                        return Response({"error": "Order not associated with this payment"}, status=status.HTTP_400_BAD_REQUEST)

                    payment.order.status = "COMPLETED"
                    payment.order.save()
                    print(f"Payment {payment.payment_id} successful, order completed.")

                elif payment.status == "FAILED":
                    if payment.order:
                        payment.order.status = "CANCELLED"
                        payment.order.save()
                        print(f"Payment {payment.payment_id} failed, order {payment.order.id} cancelled.")
                    return Response({"error": "Payment failed, order cancelled."}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"message": f"Payment status updated: {payment.status}"}, status=status.HTTP_200_OK)