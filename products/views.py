from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import json

from .models import Category, ProductDetail
from .utils import is_authenticated


# ---------------- CATEGORY ----------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class CategoryView(View):

    def get(self, request):
        """ List all categories (only non-deleted) """
        cats = list(Category.objects.values())
        return JsonResponse(cats, safe=False)

    def post(self, request):
        """ Create a category """
        try:
            body = json.loads(request.body or "{}")
            name = body.get("category")
            if not name:
                return JsonResponse({"error": "category field is required"}, status=400)

            c = Category.objects.create(
                category=name,
                category_descrip=body.get("category_descrip", "")
            )
            return JsonResponse({"msg": "created", "id": c.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request):
        """ Update a category """
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"error": "id is required"}, status=400)

            c = Category.objects.get(id=category_id)
            c.category = body.get("category", c.category)
            c.category_descrip = body.get("category_descrip", c.category_descrip)
            c.save()
            return JsonResponse({"msg": "updated"})
        except Category.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        """ Soft delete a category """
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"error": "id is required"}, status=400)

            c = Category.objects.get(id=category_id)
            c.delete()  # soft delete
            return JsonResponse({"msg": "soft deleted"})
        except Category.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request):
        """ Restore a soft deleted category """
        try:
            body = json.loads(request.body or "{}")
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"error": "id is required"}, status=400)

            c = Category.all_objects.get(id=category_id)  # includes deleted
            c.restore()
            return JsonResponse({"msg": "restored"})
        except Category.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# ---------------- PRODUCT ----------------
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(is_authenticated, name="dispatch")
class ProductView(View):

    def get(self, request):
        """ List all products (only non-deleted) """
        prods = list(ProductDetail.objects.values())
        return JsonResponse(prods, safe=False)

    def post(self, request):
        """ Create a product """
        try:
            body = json.loads(request.body or "{}")
            cat_id = body.get("category_id")
            if not cat_id:
                return JsonResponse({"error": "category_id is required"}, status=400)

            product_name = body.get("product_name")
            if not product_name:
                return JsonResponse({"error": "product_name is required"}, status=400)

            product_price = body.get("product_price")
            if product_price is None:
                return JsonResponse({"error": "product_price is required"}, status=400)

            cat = Category.objects.get(id=cat_id)
            p = ProductDetail.objects.create(
                category=cat,
                product_name=product_name,
                product_description=body.get("product_description", ""),
                available_quantity=body.get("available_quantity", 0),
                product_price=product_price
            )
            return JsonResponse({"msg": "created", "id": p.id})
        except Category.DoesNotExist:
            return JsonResponse({"error": "invalid category"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request):
        """ Update a product """
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"error": "id is required"}, status=400)

            p = ProductDetail.objects.get(id=product_id)
            p.product_name = body.get("product_name", p.product_name)
            p.product_description = body.get("product_description", p.product_description)
            p.available_quantity = body.get("available_quantity", p.available_quantity)
            p.product_price = body.get("product_price", p.product_price)
            p.save()
            return JsonResponse({"msg": "updated"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        """ Soft delete a product """
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"error": "id is required"}, status=400)

            p = ProductDetail.objects.get(id=product_id)
            p.delete()  # soft delete
            return JsonResponse({"msg": "soft deleted"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request):
        """ Restore a soft deleted product """
        try:
            body = json.loads(request.body or "{}")
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"error": "id is required"}, status=400)

            p = ProductDetail.all_objects.get(id=product_id)  # includes deleted
            p.restore()
            return JsonResponse({"msg": "restored"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)










# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_protect
# import json
# from .models import Category, ProductDetail
# from .utils import is_authenticated   # ✅ auth decorator


# # ----------- CATEGORY CRUD -----------------
# @csrf_protect
# @is_authenticated
# def categories(request):
#     if request.method == "GET":  # public
#         cats = list(Category.objects.values())
#         return JsonResponse(cats, safe=False)

#     # protected routes
#     return protected_categories(request)


# @csrf_protect
# @is_authenticated
# def protected_categories(request):
#     try:
#         body = json.loads(request.body or "{}")
#     except Exception:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)

#     if request.method == "POST":
#         try:
#             category_name = body.get("category")
#             if not category_name:
#                 return JsonResponse({"error": "category field is required"}, status=400)

#             c = Category.objects.create(
#                 category=category_name,
#                 category_descrip=body.get("category_descrip", "")
#             )
#             return JsonResponse({"msg": "created", "id": c.id})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     if request.method == "PUT":
#         try:
#             category_id = body.get("id")
#             if not category_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             c = Category.objects.get(id=category_id)
#             c.category = body.get("category", c.category)
#             c.category_descrip = body.get("category_descrip", c.category_descrip)
#             c.save()
#             return JsonResponse({"msg": "updated"})
#         except Category.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     if request.method == "DELETE":
#         try:
#             category_id = body.get("id")
#             if not category_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             c = Category.objects.get(id=category_id)
#             c.delete()
#             return JsonResponse({"msg": "deleted"})
#         except Category.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "method not allowed"}, status=405)


# # ----------- PRODUCT CRUD -----------------
# def products(request):
#     if request.method == "GET":  # public
#         prods = list(ProductDetail.objects.values())
#         return JsonResponse(prods, safe=False)

#     # protected routes
#     return protected_products(request)


# @csrf_protect
# @is_authenticated
# def protected_products(request):
#     try:
#         body = json.loads(request.body or "{}")
#     except Exception:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)

#     if request.method == "POST":
#         try:
#             cat_id = body.get("category_id")
#             if not cat_id:
#                 return JsonResponse({"error": "category_id is required"}, status=400)

#             product_name = body.get("product_name")
#             if not product_name:
#                 return JsonResponse({"error": "product_name is required"}, status=400)

#             product_price = body.get("product_price")
#             if product_price is None:
#                 return JsonResponse({"error": "product_price is required"}, status=400)

#             cat = Category.objects.get(id=cat_id)
#             p = ProductDetail.objects.create(
#                 category=cat,
#                 product_name=product_name,
#                 product_description=body.get("product_description", ""),
#                 available_quantity=body.get("available_quantity", 0),
#                 product_price=product_price
#             )
#             return JsonResponse({"msg": "created", "id": p.id})
#         except Category.DoesNotExist:
#             return JsonResponse({"error": "invalid category"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     if request.method == "PUT":
#         try:
#             product_id = body.get("id")
#             if not product_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             p = ProductDetail.objects.get(id=product_id)
#             p.product_name = body.get("product_name", p.product_name)
#             p.product_description = body.get("product_description", p.product_description)
#             p.available_quantity = body.get("available_quantity", p.available_quantity)
#             p.product_price = body.get("product_price", p.product_price)
#             p.save()
#             return JsonResponse({"msg": "updated"})
#         except ProductDetail.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     if request.method == "DELETE":
#         try:
#             product_id = body.get("id")
#             if not product_id:
#                 return JsonResponse({"error": "id is required"}, status=400)

#             p = ProductDetail.objects.get(id=product_id)
#             p.delete()
#             return JsonResponse({"msg": "deleted"})
#         except ProductDetail.DoesNotExist:
#             return JsonResponse({"error": "not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "method not allowed"}, status=405)