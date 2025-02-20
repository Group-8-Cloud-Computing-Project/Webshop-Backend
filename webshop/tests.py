from django.test import TestCase
from .models import Order, Inventory, EmailNotification, MockPayment
from django.urls import reverse
from rest_framework import status

class OrderTestCase(TestCase):
    def setUp(self):
        Order.objects.create(
            customer_name="Max Mustermann",
            customer_email="manx-mustermann@example.com",
            products=[{"name": "Keyboard", "quantity": 1}],
            total_price=50.00,
            status="PENDING"
        )

    def test_order_creation(self):
        order = Order.objects.get(customer_name="Max Mustermann")
        self.assertEqual(order.status, "PENDING")


class InventoryTestCase(TestCase):
    def setUp(self):
        Inventory.objects.create(
            product_name="Keyboard",
            product_description="Mechanical keyboard with RGB backlight.",
            quantity=20,
            low_stock_threshold=5
        )

    def test_is_low_stock(self):
        # Retrieve the inventory item
        item = Inventory.objects.get(product_name="Keyboard")

        # Check when the quantity is above the low stock threshold
        self.assertFalse(item.is_low_stock(), "Item should not be flagged as low stock.")

        # Update quantity to a low stock level
        item.quantity = 3
        item.save()

        # Check when the quantity is below the low stock threshold
        self.assertTrue(item.is_low_stock(), "Item should be flagged as low stock.")

class EmailNotificationTestCase(TestCase):
    def test_email_sent_successfully(self):
        notification = EmailNotification.objects.create(
            recipient='test@example.com',
            subject='Test Email',
            message='This is a test email.',
        )
        self.assertEqual(notification.status, 'PENDING')

        # Simulate sending email
        notification.status = 'SENT'
        notification.save()

        self.assertEqual(notification.status, 'SENT')

    def test_email_failed(self):
        notification = EmailNotification.objects.create(
            recipient='invalid-email',
            subject='Test Email',
            message='This is a test email.',
        )
        self.assertEqual(notification.status, 'PENDING')

        # Simulate failure
        notification.status = 'FAILED'
        notification.save()

        self.assertEqual(notification.status, 'FAILED')

class PaymentProcessingTestCase(TestCase):
    def setUp(self):
        """
        Set up a test order with a MockPayment.
        """
        self.order = Order.objects.create(
            customer_name="Max Mustermann",
            customer_email="max-mustermann@example.com",
            products=[{"name": "Keyboard", "quantity": 1}],
            total_price=50.00,
            status="PENDING"
        )

        self.payment = MockPayment.objects.create(
            order=self.order,
            amount=self.order.total_price,
            provider="stripe",
            status="PENDING"
        )

    def test_mockpayment_creation(self):
        """
        Tests whether a MockPayment is created correctly.
        """
        payment = MockPayment.objects.get(order=self.order)
        self.assertEqual(payment.status, "PENDING")
        self.assertEqual(payment.amount, self.order.total_price)
        self.assertEqual(payment.provider, "stripe")

    def test_payment_webhook_success(self):
        """
        Simulates a successful payment receipt via the webhook.
            - The payment is set to "COMPLETED".
            - The order is set to "COMPLETED"
        """
        webhook_url = reverse("payment-webhook")

        response = self.client.post(webhook_url, {
            "payment_id": self.payment.payment_id,
            "status": "COMPLETED"
        }, format="json")

        self.payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payment.status, "COMPLETED")
        self.assertEqual(self.order.status, "COMPLETED")

    def test_payment_webhook_failed(self):
        """
        Simulates a failed payment via the webhook.
            - The payment is set to "FAILED".
            - The order remains on "PENDING".
        """
        webhook_url = reverse("payment-webhook")

        response = self.client.post(webhook_url, {
            "payment_id": self.payment.payment_id,
            "status": "FAILED"
        }, format="json")

        self.payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payment.status, "FAILED")
        self.assertEqual(self.order.status, "PENDING")