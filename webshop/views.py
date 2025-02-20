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

def send_low_stock_email(self, product_name, quantity):
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
    # API Endpoint for Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """
        Creates a product and automatically creates an associated inventory object.
        """
        product = serializer.save()

        # If no inventory exists, create one
        inventory, created = Inventory.objects.get_or_create(product=product, defaults={"quantity": 10})
        if created:
            print(f"Inventory created for {product.name} with default quantity 10.")
        else:
            print(f"Inventory for {product.name} already exists.")

    def perform_update(self, serializer):
        """
        Updates the product and ensures that the associated inventory object exists.
        """
        product = serializer.save()

        # If Inventory is missing, create it
        inventory, created = Inventory.objects.get_or_create(product=product)

        if created:
            print(f"Inventory created for {product.name} subsequently.")

    def perform_destroy(self, instance):
        """
        Deletes the product and also removes the associated inventory object.
        """
        Inventory.objects.filter(product=instance).delete()
        print(f"Inventory for {instance.name} deleted.")

        instance.delete()
        print(f"Product {instance.name} deleted.")
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        """
        Create a MockPayment object after order confirmation.
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

                    products = payment.order.products
                    if isinstance(products, dict):
                        products = [products]
                    if not isinstance(products, list):
                        return Response({"error": "Products data must be a list or a valid dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # Update inventory
                    for product_data in products:
                        product_name = product_data["name"]
                        quantity = int(product_data["quantity"])

                        inventory_item = Inventory.objects.get(product__name=product_name)
                        inventory_item.quantity -= quantity
                        inventory_item.save()
                        print(f"Inventory updated for {product_name}, new quantity: {inventory_item.quantity}")

                        if inventory_item.is_low_stock():
                            send_low_stock_email(self, product_name, inventory_item.quantity)

                    send_order_confirmation(payment.order)
                    print(f"Payment {payment.payment_id} successful, order completed.")

                elif payment.status == "FAILED":
                    if payment.order:
                        payment.order.status = "CANCELLED"
                        payment.order.save()
                        print(f"Payment {payment.payment_id} failed, order {payment.order.id} cancelled.")
                    return Response({"error": "Payment failed, order cancelled."}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"message": f"Payment status updated: {payment.status}"}, status=status.HTTP_200_OK)