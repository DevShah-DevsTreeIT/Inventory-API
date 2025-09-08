from django.urls import path
from .views import CartView, CheckoutView, ReceiptView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("", CheckoutView.as_view(), name="checkout"),
    path("<int:checkout_id>/receipt/", ReceiptView.as_view(), name="receipt"),
]