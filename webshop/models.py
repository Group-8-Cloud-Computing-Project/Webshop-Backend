from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


def __str__(self):
    return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    products = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.status})"


class Inventory(models.Model):
    """
    Model to represent inventory items.
    """
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        """
        Returns True if the stock is below the low stock threshold.
        """
        return self.quantity <= self.low_stock_threshold

    def __str__(self):
        """
        String representation for the model.
        """
        return f"{self.product_name} - Quantity: {self.quantity}"


class EmailNotification(models.Model):
    """
    Model to store email notification logs.
    """
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('PENDING', 'Pending'),
            ('SENT', 'Sent'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING',
    )

    def __str__(self):
        return f"Email to {self.recipient} - {self.status} at {self.sent_at}"
