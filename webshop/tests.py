from django.test import TestCase
from .models import Order

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