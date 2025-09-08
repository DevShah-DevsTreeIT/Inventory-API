from django.db import models
from django.utils import timezone


# ------------------ Custom Manager for Soft Delete ------------------
class SoftDeleteManager(models.Manager):
    """Default manager: only return rows that are NOT soft deleted"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


# ------------------ CATEGORY ------------------
class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    category_descrip = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Managers
    objects = SoftDeleteManager()   # hides soft-deleted rows
    all_objects = models.Manager()  # shows everything (even deleted)

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard delete"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore a soft deleted row"""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return self.category


# ------------------ PRODUCT ------------------
class ProductDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=150)
    product_description = models.TextField(blank=True, null=True)
    available_quantity = models.PositiveIntegerField(default=0)  # ✅ matches "stock levels"
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ matches "price"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Managers
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        # ✅ Ensure no duplicate product names inside same category
        constraints = [
            models.UniqueConstraint(fields=["category", "product_name"], name="uniq_product_per_category")
        ]

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard delete"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore a soft deleted row"""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return self.product_name

######################## Previous ########################


# from django.db import models
# from django.utils import timezone


# # Manager that hides soft deleted rows
# class SoftDeleteManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(deleted_at__isnull=True)


# class Category(models.Model):
#     category = models.CharField(max_length=100, unique=True)
#     category_descrip = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     # managers
#     objects = SoftDeleteManager()   # hides soft deleted
#     all_objects = models.Manager()  # shows everything, even deleted

#     def delete(self, using=None, keep_parents=False):
#         """ Soft delete: mark as deleted instead of removing """
#         self.deleted_at = timezone.now()
#         self.save(update_fields=["deleted_at"])

#     def restore(self):
#         """ Restore a previously soft deleted row """
#         self.deleted_at = None
#         self.save(update_fields=["deleted_at"])

#     def __str__(self):
#         return self.category


# class ProductDetail(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
#     product_name = models.CharField(max_length=150)
#     product_description = models.TextField(blank=True, null=True)
#     available_quantity = models.PositiveIntegerField(default=0)
#     product_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

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
#         return self.product_name

######################## -------xx---xx------- ########################
