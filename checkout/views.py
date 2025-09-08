# from django.http import JsonResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_protect
# import json

# from .models import CartDetail, Checkout
# from products.models import ProductDetail
# from users.models import User
# from .utils import is_authenticated


# # ---------------- CART ----------------
# @method_decorator(csrf_protect, name="dispatch")
# @method_decorator(is_authenticated, name="dispatch")
# class CartView(View):

#     def get(self, request):
#         """ List all cart items (non-deleted) """
#         carts = list(CartDetail.objects.values())
#         return JsonResponse(carts, safe=False)

#     def post(self, request):
#         """ Add product to cart """
#         try:
#             body = json.loads(request.body or "{}")
#             user_id = body.get("user_id")
#             product_id = body.get("product_id")
#             quantity = body.get("quantity", 1)

#             if not user_id or not product_id:
#                 return JsonResponse({"error": "user_id and product_id required"}, status=400)

#             user = User.objects.get(id=user_id)
#             product = ProductDetail.objects.get(id=product_id)

#             cart = CartDetail.objects.create(
#                 user=user,
#                 product=product,
#                 selected_product_name=product.product_name,
#                 selected_product_description=product.product_description,
#                 selected_quantity=quantity,
#                 selected_product_price=product.product_price,
#                 total_amount=quantity * product.product_price
#             )
#             return JsonResponse({"msg": "added to cart", "id": cart.id})
#         except User.DoesNotExist:
#             return JsonResponse({"error": "invalid user"}, status=400)
#         except ProductDetail.DoesNotExist:
#             return JsonResponse({"error": "invalid product"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     def put(self, request):
#         """ Update cart item quantity """
#         try:
#             body = json.loads(request.body or "{}")
#             cart_id = body.get("id")
#             quantity = body.get("quantity")

#             if not cart_id or quantity is None:
#                 return JsonResponse({"error": "id and quantity required"}, status=400)

#             cart = CartDetail.objects.get(id=cart_id)
#             cart.selected_quantity = quantity
#             cart.save()
#             return JsonResponse({"msg": "updated"})
#         except CartDetail.DoesNotExist:
#             return JsonResponse({"error": "cart item not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     def delete(self, request):
#         """ Remove item from cart (soft delete) """
#         try:
#             body = json.loads(request.body or "{}")
#             cart_id = body.get("id")
#             if not cart_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             cart = CartDetail.objects.get(id=cart_id)
#             cart.delete()
#             return JsonResponse({"msg": "soft deleted"})
#         except CartDetail.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)


# # ---------------- CHECKOUT ----------------
# @method_decorator(csrf_protect, name="dispatch")
# @method_decorator(is_authenticated, name="dispatch")
# class CheckoutView(View):

#     def get(self, request):
#         """ List all checkouts (non-deleted) """
#         checkouts = list(Checkout.objects.values())
#         return JsonResponse(checkouts, safe=False)

#     def post(self, request):
#         """ Place an order """
#         try:
#             body = json.loads(request.body or "{}")
#             user_id = body.get("user_id")
#             product_id = body.get("product_id")
#             quantity = body.get("quantity", 1)
#             payment_method = body.get("payment_method", "Cash")

#             if not user_id or not product_id:
#                 return JsonResponse({"error": "user_id and product_id required"}, status=400)

#             user = User.objects.get(id=user_id)
#             product = ProductDetail.objects.get(id=product_id)

#             checkout = Checkout.objects.create(
#                 user=user,
#                 product=product,
#                 quantity=quantity,
#                 total_amount=quantity * product.product_price,
#                 payment_method=payment_method,
#                 payment_status="pending"
#             )
#             return JsonResponse({"msg": "order placed", "id": checkout.id})
#         except User.DoesNotExist:
#             return JsonResponse({"error": "invalid user"}, status=400)
#         except ProductDetail.DoesNotExist:
#             return JsonResponse({"error": "invalid product"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     def put(self, request):
#         """ Update checkout (like payment status) """
#         try:
#             body = json.loads(request.body or "{}")
#             checkout_id = body.get("id")
#             payment_status = body.get("payment_status")

#             if not checkout_id or not payment_status:
#                 return JsonResponse({"error": "id and payment_status required"}, status=400)

#             checkout = Checkout.objects.get(id=checkout_id)
#             checkout.payment_status = payment_status
#             checkout.save()
#             return JsonResponse({"msg": "updated"})
#         except Checkout.DoesNotExist:
#             return JsonResponse({"error": "checkout not found"}, status=404)

#     def delete(self, request):
#         """ Cancel order (soft delete) """
#         try:
#             body = json.loads(request.body or "{}")
#             checkout_id = body.get("id")
#             if not checkout_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             checkout = Checkout.objects.get(id=checkout_id)
#             checkout.delete()
#             return JsonResponse({"msg": "soft deleted"})
#         except Checkout.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import json

from .models import CartDetail, Checkout
from products.models import ProductDetail
from users.models import UserProfile
from .utils import is_authenticated


# ---------------- CART ----------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class CartView(View):

    def get(self, request):
        """List all cart items"""
        carts = list(CartDetail.objects.values())
        return JsonResponse({"success": True, "data": carts})

    def post(self, request):
        """Add product to cart"""
        try:
            body = json.loads(request.body or "{}")
            user_id = body.get("user_id")
            product_id = body.get("product_id")
            quantity = body.get("quantity", 1)

            if not user_id or not product_id:
                return JsonResponse({"success": False, "message": "user_id and product_id required"}, status=400)

            user = UserProfile.objects.get(id=user_id)
            product = ProductDetail.objects.get(id=product_id)

            cart = CartDetail.objects.create(
                user=user,
                product=product,
                selected_product_name=product.product_name,
                selected_product_description=product.product_description,
                selected_quantity=quantity,
                selected_product_price=product.product_price
            )
            return JsonResponse({"success": True, "message": "Product Added to cart", "data": {"id": cart.id}})
        except UserProfile.DoesNotExist:
            return JsonResponse({"success": False, "message": "Sorry, Invalid user"}, status=400)
        except ProductDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid product"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def put(self, request):
        """Update cart quantity"""
        try:
            body = json.loads(request.body or "{}")
            cart_id = body.get("id")
            quantity = body.get("quantity")

            if not cart_id or quantity is None:
                return JsonResponse({"success": False, "message": "id and quantity required"}, status=400)

            cart = CartDetail.objects.get(id=cart_id)
            cart.selected_quantity = quantity
            cart.save()
            return JsonResponse({"success": True, "message": "Cart updated"})
        except CartDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cart item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def delete(self, request):
        """Soft delete cart item"""
        try:
            body = json.loads(request.body or "{}")
            cart_id = body.get("id")
            if not cart_id:
                return JsonResponse({"success": False, "message": "id required"}, status=400)

            cart = CartDetail.objects.get(id=cart_id)
            cart.delete()
            return JsonResponse({"success": True, "message": "Cart item removed"})
        except CartDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "Not found"}, status=404)


# ---------------- CHECKOUT ----------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class CheckoutView(View):

    def get(self, request):
        """List all checkouts"""
        checkouts = list(Checkout.objects.values())
        return JsonResponse({"success": True, "data": checkouts})

    def post(self, request):
        """Place an order"""
        try:
            body = json.loads(request.body or "{}")
            user_id = body.get("user_id")
            product_id = body.get("product_id")
            quantity = int(body.get("quantity", 1))
            payment_method = body.get("payment_method", "Cash")

            if not user_id or not product_id:
                return JsonResponse({"success": False, "message": "user_id and product_id required"}, status=400)

            user = UserProfile.objects.get(id=user_id)
            product = ProductDetail.objects.get(id=product_id)

            # stock validation
            if product.available_quantity < quantity:
                return JsonResponse({"success": False, "message": "Not enough stock"}, status=400)

            checkout = Checkout.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                payment_method=payment_method,
                payment_status="pending"
            )

            # reduce stock
            product.available_quantity -= quantity
            product.save()

            return JsonResponse({"success": True, "message": "Order placed", "data": {"id": checkout.id}})
        except UserProfile.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid user"}, status=400)
        except ProductDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid product"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def put(self, request):
        """Update checkout (like payment status)"""
        try:
            body = json.loads(request.body or "{}")
            checkout_id = body.get("id")
            payment_status = body.get("payment_status")

            if not checkout_id or not payment_status:
                return JsonResponse({"success": False, "message": "id and payment_status required"}, status=400)

            checkout = Checkout.objects.get(id=checkout_id)
            checkout.payment_status = payment_status
            checkout.save()
            return JsonResponse({"success": True, "message": "Checkout updated"})
        except Checkout.DoesNotExist:
            return JsonResponse({"success": False, "message": "Checkout not found"}, status=404)

    def delete(self, request):
        """Soft delete order"""
        try:
            body = json.loads(request.body or "{}")
            checkout_id = body.get("id")
            if not checkout_id:
                return JsonResponse({"success": False, "message": "id required"}, status=400)

            checkout = Checkout.objects.get(id=checkout_id)
            checkout.delete()
            return JsonResponse({"success": True, "message": "Order cancelled"})
        except Checkout.DoesNotExist:
            return JsonResponse({"success": False, "message": "Not found"}, status=404)


# ---------------- RECEIPT ----------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class ReceiptView(View):
    def get(self, request, checkout_id):
        """Get receipt for an order"""
        try:
            checkout = Checkout.objects.get(id=checkout_id)
            receipt = {
                "order_id": checkout_id,
                "user": checkout.user.username,
                "product": checkout.product.product_name,
                "quantity": checkout.quantity,
                "total_amount": float(checkout.total_amount),
                "payment_method": checkout.payment_method,
                "payment_status": checkout.payment_status,
                "purchased_at": checkout.purchased_at,
            }
            return JsonResponse({"success": True, "data": receipt})
        except Checkout.DoesNotExist:
            return JsonResponse({"success": False, "message": "Checkout not found"}, status=404)
