from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import json
# from users.views import role
from .models import Category, ProductDetail
from .utils import is_authenticated
from django.contrib.auth.decorators import login_required

# ------------------ CATEGORY CRUD ------------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class CategoryView(View):

    def get(self, request):
        
        try:
            # @login_required
            # def my_admin_view(request):
            if request.user.is_superuser:
                message = "Welcome, Administrator!"
                c = list(Category.all_objects.values(
                    "id", "category", "category_descrip", "created_at", "updated_at","deleted_at"
                ))  # includes deleted

            else:
                message = "Welcome, User!"
                # return JsonResponse({"success": True, "message": "created", "id": c.id})
                """List all categories (non-deleted only)"""
                cats = list(Category.objects.values(
                    "id", "category", "category_descrip", "created_at", "updated_at"
                ))
                return JsonResponse({"success": True, "data": cats}, safe=False)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)


        

    def post(self, request):
        """Create a category"""
        try:
            body = json.loads(request.body or "{}")
            name = body.get("category")
            if not name:
                return JsonResponse({"success": False, "message": "category field is required"}, status=400)

            c = Category.objects.create(
                category=name,
                category_descrip=body.get("category_descrip", "")
            )
            return JsonResponse({"success": True, "message": "created", "id": c.id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def put(self, request):
        """Update a category"""
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            c = Category.objects.get(id=category_id)
            c.category = body.get("category", c.category)
            c.category_descrip = body.get("category_descrip", c.category_descrip)
            c.save()
            return JsonResponse({"success": True, "message": "updated"})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def delete(self, request):
        """Soft delete a category"""
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            c = Category.objects.get(id=category_id)
            c.delete()
            return JsonResponse({"success": True, "message": "soft deleted"})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def patch(self, request):
        """Restore a soft deleted category"""
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            c = Category.all_objects.get(id=category_id)  # includes deleted
            c.restore()
            return JsonResponse({"success": True, "message": "restored"})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)


# ------------------ PRODUCT CRUD ------------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class ProductView(View):

    def get(self, request):
        """List all products (non-deleted only)"""
        prods = list(ProductDetail.objects.values(
            "id", "product_name", "product_description",
            "available_quantity", "product_price", "category_id",
            "created_at", "updated_at"
        ))
        return JsonResponse({"success": True, "data": prods}, safe=False)

    def post(self, request):
        """Create a product"""
        try:
            body = json.loads(request.body or "{}")
            cat_id = body.get("category_id")
            if not cat_id:
                return JsonResponse({"success": False, "message": "category_id is required"}, status=400)

            product_name = body.get("product_name")
            if not product_name:
                return JsonResponse({"success": False, "message": "product_name is required"}, status=400)

            product_price = body.get("product_price")
            if product_price is None:
                return JsonResponse({"success": False, "message": "product_price is required"}, status=400)

            # Validate stock
            available_quantity = int(body.get("available_quantity", 0))
            if available_quantity < 0:
                return JsonResponse({"success": False, "message": "available_quantity cannot be negative"}, status=400)

            cat = Category.objects.get(id=cat_id)
            p = ProductDetail.objects.create(
                category=cat,
                product_name=product_name,
                product_description=body.get("product_description", ""),
                available_quantity=available_quantity,
                product_price=product_price
            )
            return JsonResponse({"success": True, "message": "created", "id": p.id})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "message": "invalid category"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def put(self, request):
        """Update a product"""
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            p = ProductDetail.objects.get(id=product_id)

            if "available_quantity" in body:
                qty = int(body["available_quantity"])
                if qty < 0:
                    return JsonResponse({"success": False, "message": "available_quantity cannot be negative"}, status=400)
                p.available_quantity = qty

            p.product_name = body.get("product_name", p.product_name)
            p.product_description = body.get("product_description", p.product_description)
            p.product_price = body.get("product_price", p.product_price)
            p.save()
            return JsonResponse({"success": True, "message": "updated"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def delete(self, request):
        """Soft delete a product"""
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            p = ProductDetail.objects.get(id=product_id)
            p.delete()
            return JsonResponse({"success": True, "message": "soft deleted"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    def patch(self, request):
        """Restore a soft deleted product"""
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"success": False, "message": "id is required"}, status=400)

            p = ProductDetail.all_objects.get(id=product_id)  # includes deleted
            p.restore()
            return JsonResponse({"success": True, "message": "restored"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"success": False, "message": "product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)