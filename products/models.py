from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     category_id = models.CharFieldc(max_length=50)
#     category = models.CharFieldc(max_length=50)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField()


#     def __str__(self):
#         return self.name
    

# Category Table
class Category(models.Model):
    # category_id = models.AutoField(primary_key=True)   #AutoField(primary_key=True):- This will Auto incremente the primary key
    category = models.CharField(max_length=100, unique=True)  # Unique category name
    category_descrip = models.TextField(blank=True, null=True)  #if we use blank=True, null=True it will make the description Optional
    created_at = models.DateTimeField(auto_now_add=True)   # Auto set when created
    updated_at = models.DateTimeField(auto_now=True)       # Auto update when saved
    deleted_at = models.DateTimeField(blank=True, null=True)   # For soft delete

    def __str__(self):
        return self.category


# Product Table
class ProductDetail(models.Model):
    # product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,   # If category is deleted → delete its products
        related_name="products"
    )
    product_name = models.CharField(max_length=150)
    product_description = models.TextField(blank=True, null=True)
    available_quantity = models.PositiveIntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # up to 99999999.99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.product_name
















# # --- Base mixins -------------------------------------------------------------

# class TimeStampedModel(models.Model):
#     """
#     Gives every table:
#     - created_at: set once when the row is inserted
#     - updated_at: updated on every save()
#     """
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True  # don't create a table for this class


# class SoftDeleteQuerySet(models.QuerySet):
#     """
#     QuerySet helpers for soft-deletion.
#     - delete(): mark rows as deleted (sets deleted_at)
#     - hard_delete(): actually removes rows from DB
#     - alive(): only not-deleted rows
#     - dead(): only soft-deleted rows
#     """
#     def delete(self):
#         return super().update(deleted_at=timezone.now())

#     def hard_delete(self):
#         return super().delete()

#     def alive(self):
#         return self.filter(deleted_at__isnull=True)

#     def dead(self):
#         return self.exclude(deleted_at__isnull=True)


# class SoftDeleteManager(models.Manager):
#     """
#     Default manager that hides soft-deleted rows.
#     Use Product.all_objects to see everything.
#     """
#     def get_queryset(self):
#         return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

# # --- Actual tables -----------------------------------------------------------

# class Category(TimeStampedModel):
#     """
#     CATEGORY table (implicit in your ERD because product has CATEGORY_ID FK)
#     """
#     category_id = models.BigAutoField(primary_key=True, db_column='category_id')
#     name = models.CharField(max_length=80, unique=True, db_column='category_name')
#     description = models.TextField(blank=True, db_column='category_descrip')

#     class Meta:
#         db_table = 'category'  # physical table name

#     def __str__(self):
#         return self.name


# class Product(TimeStampedModel):
#     """
#     PRODUCT_DETAIL table from your ERD
#     """
#     # PRODUCT_ID (PK)
#     product_id = models.BigAutoField(primary_key=True, db_column='product_id')

#     # CATEGORY_ID (FK) -> Category.category_id
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.PROTECT,              # don't allow deleting a category if products exist
#         related_name='products',               # category.products.all()
#         db_column='category_id'
#     )

#     # PRODUCT_NAME, PRODUCT_DESCRIPTION
#     name = models.CharField(max_length=120, db_column='product_name')
#     description = models.TextField(blank=True, db_column='product_description')

#     # AVAILABLE_QUANTITY (non-negative) and PRODUCT_PRICE (non-negative monetary)
#     available_quantity = models.PositiveIntegerField(
#         default=0,
#         validators=[MinValueValidator(0)],
#         db_column='available_quantity'
#     )
#     price = models.DecimalField(
#         max_digits=10, decimal_places=2,
#         validators=[MinValueValidator(0)],
#         db_column='product_price'
#     )

#     # DELETED_AT (soft delete marker)
#     deleted_at = models.DateTimeField(null=True, blank=True, default=None, db_column='deleted_at')

#     # Managers: objects hides soft-deleted; all_objects shows everything
#     objects = SoftDeleteManager()
#     all_objects = SoftDeleteQuerySet.as_manager()

#     class Meta:
#         db_table = 'product_detail'  # physical table name to match ERD (lowercase is safer in Postgres)
#         # Prevent the same product name twice inside one category
#         constraints = [
#             models.UniqueConstraint(fields=['category', 'name'], name='uniq_product_per_category')
#         ]
#         indexes = [
#             models.Index(fields=['category', 'name']),
#         ]

#     def __str__(self):
#         return self.name

#     # Make instance.delete() perform a soft delete
#     def delete(self, using=None, keep_parents=False):
#         self.deleted_at = timezone.now()
#         self.save(update_fields=['deleted_at'])

#     # Helper to undo a soft delete
#     def restore(self):
#         self.deleted_at = None
#         self.save(update_fields=['deleted_at'])




 














# # Category Model
# class Category(models.Model):
#     category_id = models.AutoField(primary_key=True)   # Auto-increment primary key
#     category = models.CharField(max_length=100, unique=True)  # Name of category
#     category_descrip = models.TextField(blank=True, null=True)  # Optional description
#     created_at = models.DateTimeField(auto_now_add=True)   # Auto set when created
#     updated_at = models.DateTimeField(auto_now=True)       # Auto update when saved
#     deleted_at = models.DateTimeField(blank=True, null=True)   # If soft-deleted

#     def __str__(self):
#         return self.category


# # Product Model
# class ProductDetail(models.Model):
#     product_id = models.AutoField(primary_key=True)   # Auto-increment PK
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,   # If category is deleted, delete products
#         related_name="products"
#     )
#     product_name = models.CharField(max_length=150)
#     product_description = models.TextField(blank=True, null=True)
#     available_quantity = models.PositiveIntegerField(default=0)
#     product_price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g. 99999999.99
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return self.product_name


# # User Model
# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=100)
#     user_email = models.EmailField(unique=True)
#     user_password = models.CharField(max_length=255)   # Later you can hash it
#     auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     created_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user_name

