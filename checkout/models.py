# from django.db import models
# from django.utils import timezone
# from products.models import ProductDetail
# from users.models import User
#     # from django.db import transaction
#     # Create your models here.



# class SoftDeleteManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(deleted_at__isnull=True)


# # Cart Table
# class CartDetail(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")   # If user is deleted → delete their cart    
#     product = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="cart")   # If product is deleted → delete checkout record
#     # product_category = models.CharField(max_length=110)
#     selected_product_name = models.CharField(max_length=150)
#     selected_product_description = models.TextField(blank=True, null=True)
#     selected_quantity = models.PositiveIntegerField(default=0)
#     selected_product_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_amount = models.DecimalField(max_digits=12, decimal_places=2) 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         self.total_amount = self.selected_quantity * self.selected_product_price
#         super().save(*args, **kwargs)



#     # managers
#     objects = SoftDeleteManager()
#     all_objects = models.Manager()

#     def delete(self, using=None, keep_parents=False):
#         """ Soft delete: mark as deleted instead of removing """
#         self.deleted_at = timezone.now()
#         self.save(update_fields=["deleted_at"])

#     def restore(self):
#         """ Restore a previously soft deleted row """
#         self.deleted_at = None
#         self.save(update_fields=["deleted_at"])

#     def __str__(self):
#         return self.selected_product_name



# class Checkout(models.Model):
#     # checkout_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="checkouts")  # If user is deleted → delete their checkouts
#     product = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,related_name="checkouts") # If product is deleted → delete checkout record
#     quantity = models.PositiveIntegerField(default=1)
#     total_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_method = models.CharField(max_length=50)   # e.g., "Cash", "Card", "UPI"
#     PAYMENT_STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("paid", "Paid"),
#         ("failed", "Failed"),
#     ]
#     payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")
#     purchased_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         self.total_amount = self.quantity * self.product.product_price
#         super().save(*args, **kwargs)


#     # managers
#     objects = SoftDeleteManager()
#     all_objects = models.Manager()

#     def delete(self, using=None, keep_parents=False):
#         """ Soft delete: mark as deleted instead of removing """
#         self.deleted_at = timezone.now()
#         self.save(update_fields=["deleted_at"])

#     def restore(self):
#         """ Restore a previously soft deleted row """
#         self.deleted_at = None
#         self.save(update_fields=["deleted_at"])


#     def __str__(self):
#         return f"Order {self.id} - {self.user.username} ({self.product.product_name})"

from django.db import models
from django.utils import timezone
from products.models import ProductDetail
from users.models import UserProfile


# Manager to hide soft-deleted rows
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


# ---------------- CART ----------------
class CartDetail(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, related_name="cart")
    selected_product_name = models.CharField(max_length=150)
    selected_product_description = models.TextField(blank=True, null=True)
    selected_quantity = models.PositiveIntegerField(default=0)
    selected_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_amount = float(self.selected_quantity) * float(self.selected_product_price)
        super().save(*args, **kwargs)

    # managers
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore"""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return self.selected_product_name


# ---------------- CHECKOUT ----------------
class Checkout(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="checkouts")
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, related_name="checkouts")
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50)   # e.g. Cash, Card, UPI

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")

    purchased_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_amount = float(self.quantity) * float(self.product.product_price)
        super().save(*args, **kwargs)

    # managers
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore"""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.product.product_name})"
