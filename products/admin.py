from django.contrib import admin
from .models import ProductDetail,Category

 
# Register your models here.

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ("product_name","available_quantity","product_description","product_price","created_at","updated_at","deleted_at")  # adjust fields as per your model


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category","category_descrip","created_at","updated_at","deleted_at")   