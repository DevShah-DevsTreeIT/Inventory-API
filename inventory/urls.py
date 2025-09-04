# Admin
"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})

urlpatterns = [
    # path("csrf/", ensure_csrf_cookie(get_csrf_token)),
    path("admin/", admin.site.urls),
    
    # users app (register, login, me)
    path("users/", include("users.urls")),  # <--- important
    
    # products app (categories, products)
    path("products/", include("products.urls")),  # <--- important

    # global csrf
    path("csrf/", csrf, name="csrf"),
]


# from django.contrib import admin
# from django.urls import path
# from users import views as user_views
# from products import views as product_views

# urlpatterns = [
#     path("admin/", admin.site.urls),

#     # ---- User Auth ----
#     path("users/register/", user_views.register, name="register"),
#     path("users/login/", user_views.login, name="login"),
#     path("users/me/", user_views.me, name="me"),

#     # ---- Category ----
#     path("categories/", product_views.categories, name="categories"),

#     # ---- Product ----
#     path("products/", product_views.products, name="products"),
# ]
