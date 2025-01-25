from django.test import TestCase
from .models import Order
from .models import Inventory

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