import uuid
from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView

from .serializers import ProductSerializer, InventorySerializer
from .models import Product
from .serializers import OrderSerializer
from .models import Order
import random
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

def send_low_stock_email(self, product_name, quantity):
    """
    Sends a notification to the admin when a product's stock is low.
    """
    email = EmailNotification.objects.create(
        recipient="admin@webshop.com",
        subject=f"Low Stock Alert: {product_name}",
        message=f"Stock for {product_name} is low ({quantity} left). Consider restocking."
    )

    try:
        send_mail(
            subject=email.subject,
            message=email.message,
            from_email='no-reply@webshop.com',
            recipient_list=[email.recipient],
        )
        email.status = 'SENT'
    except Exception:
        email.status = 'FAILED'
    email.save()
class ProductViewSet(viewsets.ModelViewSet):
    # API Endpoint for Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        """
        Create a MockPayment object after order confirmation and update inventory.
        """
        order = serializer.save()

        # Create a MockPayment
        MockPayment.objects.create(
            order=order,
            amount=order.total_price
        )
        print(f"MockPayment with status 'PENDING' created for Order {order.id}.")


    def perform_update(self, serializer):
        """
        Send email notifications when status to SHIPPED changes.
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

class MockPaymentViewSet(viewsets.ModelViewSet):
    # API Endpoint for mock payment
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

        # Update payment status
        payment.status = status_update
        payment.save()

        if payment.status == "COMPLETED":
            if not payment.order:
                return Response({"error": "Order not associated with this payment"}, status=status.HTTP_400_BAD_REQUEST)
            payment.order.status = "COMPLETED"
            payment.order.save()

            # Update inventory
            for product_data in payment.order.products:
                product_name = product_data["name"]
                quantity = product_data["quantity"]

                try:
                    inventory_item = Inventory.objects.get(product_name=product_name)
                    inventory_item.quantity -= quantity
                    inventory_item.save()
                    if inventory_item.is_low_stock():
                        self.send_low_stock_email(product_name, inventory_item.quantity)
                        print(f"Inventory updated for {product_name}, new quantity: {inventory_item.quantity}")

                        # Low stock notification
                        if inventory_item.is_low_stock():
                            EmailNotification.objects.create(
                                recipient="admin@webshop.com",
                                subject=f"Low Stock Alert: {product_name}",
                                message=f"Stock for {product_name} is low ({inventory_item.quantity} left). Consider restocking."
                            )
                    else:
                        raise serializers.ValidationError(f"Not enough stock for {product_name}")
                except Inventory.DoesNotExist:
                    raise serializers.ValidationError(f"Product {product_name} not found in inventory")

            send_order_confirmation(payment.order)
            print(f"Payment {payment.payment_id} successful, order completed.")
        elif payment.status == "FAILED":
            if payment.order:
                payment.order.status = "CANCELLED"
                payment.order.save()
                print(f"Payment {payment.payment_id} failed, order {payment.order.id} cancelled.")
            return Response({"error": "Payment failed, order cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Payment status updated: {payment.status}"}, status=status.HTTP_200_OK)