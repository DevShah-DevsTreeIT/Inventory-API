from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from .models import Category, ProductDetail
from .utils import is_authenticated   # ✅ auth decorator


# ----------- CATEGORY CRUD -----------------
@csrf_protect
@is_authenticated
def categories(request):
    if request.method == "GET":  # public
        cats = list(Category.objects.values())
        return JsonResponse(cats, safe=False)

    # protected routes
    return protected_categories(request)


@csrf_protect
@is_authenticated
def protected_categories(request):
    try:
        body = json.loads(request.body or "{}")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if request.method == "POST":
        try:
            category_name = body.get("category")
            if not category_name:
                return JsonResponse({"error": "category field is required"}, status=400)

            c = Category.objects.create(
                category=category_name,
                category_descrip=body.get("category_descrip", "")
            )
            return JsonResponse({"msg": "created", "id": c.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "PUT":
        try:
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

    if request.method == "DELETE":
        try:
            category_id = body.get("id")
            if not category_id:
                return JsonResponse({"error": "id is required"}, status=400)

            c = Category.objects.get(id=category_id)
            c.delete()
            return JsonResponse({"msg": "deleted"})
        except Category.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "method not allowed"}, status=405)


# ----------- PRODUCT CRUD -----------------
def products(request):
    if request.method == "GET":  # public
        prods = list(ProductDetail.objects.values())
        return JsonResponse(prods, safe=False)

    # protected routes
    return protected_products(request)


@csrf_protect
@is_authenticated
def protected_products(request):
    try:
        body = json.loads(request.body or "{}")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if request.method == "POST":
        try:
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

    if request.method == "PUT":
        try:
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

    if request.method == "DELETE":
        try:
            product_id = body.get("id")
            if not product_id:
                return JsonResponse({"error": "id is required"}, status=400)

            p = ProductDetail.objects.get(id=product_id)
            p.delete()
            return JsonResponse({"msg": "deleted"})
        except ProductDetail.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "method not allowed"}, status=405)