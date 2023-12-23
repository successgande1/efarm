from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import uuid


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default='sample.jpg', upload_to='product_images')

    def __str__(self):
        return self.name


class Order(models.Model):
    reference_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)  # Indicates if the order has been paid
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generating a reference number
            date_str = timezone.now().strftime("%Y%m%d")  # Format: YYYYMMDD
            unique_id = random.randint(1000, 9999)  # 4 digit random number
            self.reference_number = f"{date_str}-{unique_id}"
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Cashier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Sale(models.Model):
    reference_number = models.CharField(max_length=100, unique=True, editable=False)
    cashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.reference_number} for Order {self.order.reference_number} by {self.cashier.user.username}"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generating a reference number with current date and a UUID
            date_str = timezone.now().strftime("%Y%m%d")  # Format: YYYYMMDD
            unique_id = uuid.uuid4().hex[:4]  # 4 character UUID
            self.reference_number = f"{date_str}-{unique_id}"
        super(Sale, self).save(*args, **kwargs)

        # Update the order's payment status when a sale is saved
        self.order.is_paid = True
        self.order.save()