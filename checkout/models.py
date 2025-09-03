from django.db import models
from users.models import User
from products.models import ProductDetail

# Create your models here.

# Checkout Table
class Checkout(models.Model):
    # checkout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # If user is deleted → delete their checkouts
        related_name="checkouts"
    )   
    product = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,   # If product is deleted → delete checkout record
        related_name="checkouts"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)   # e.g., "Cash", "Card", "UPI"
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"Order {self.id} - {self.user.user_name}"
    