# App - Products
from django.urls import path
from .views import categories, products
from . import views

urlpatterns = [
    path("categories/", views.categories, name="categories"),
    # path("categories/", categories),
    path("products/", views.products, name="products"),
    # path("products/", products),
]
