# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.hashers import make_password, check_password
# from django.conf import settings
# import jwt
# import datetime, json
# from .models import User
# from .utils import is_authenticated
# # SECRET = getattr(settings, "JWT_SECRET")
# # SECRET = getattr(settings, "JWT_SECRET", "mysecret")
# SECRET = settings.JWT_SECRET


# @csrf_exempt
# def register(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST required"}, status=405)

#     body = json.loads(request.body)
#     try:
#         user = User.objects.create(
#             username=body["username"],
#             email=body["email"],
#             password=make_password(body["password"])
#         )
#         data = {
#                "id": str(user.id),  # convert UUID to string
#                 "name": user.username,
#             }
#         return JsonResponse({"msg": "User Successfully Registered", "id" "\nname":  data}, status=201)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)


# @csrf_exempt
# def login(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST required"}, status=405)

#     body = json.loads(request.body)
#     try:
#         user = User.objects.get(email=body["email"])
#     except User.DoesNotExist:
#         return JsonResponse({"error": "invalid credentials"}, status=401)

#     if not check_password(body["password"], user.password):
#         return JsonResponse({"error": "invalid credentials"}, status=401)

#     payload = {
#         "id": str(user.id),   # convert UUID
#         "email": user.email,
#         "role_slug": "basic-user",
#         "profile_id": f"usr-prf-{str(user.id)}",  # convert here too
#         "company": None,
#         "iat": datetime.datetime.utcnow().timestamp(),
#         "exp": int((datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp())
#         # "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
# }

#     token = jwt.encode(payload, SECRET, algorithm="HS256")

#     # ✅ store token in DB
#     user.auth_token = token
#     user.save()

#     return JsonResponse({"token": token}, status=200)


# @csrf_exempt
# # @is_authenticated
# def me(request):
#     auth = request.headers.get("Authorization", "")
#     if not auth.startswith("Bearer "):
#         return JsonResponse({"error": "no token"}, status=401)

#     token = auth.split()[1]
#     try:
#         print(token)
#         print(SECRET)
#         # print()
#         payload = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3MDIyMWYxLTQwM2ItNGQwZS1iMjk5LTQ4YjRkZGNiNjdiNCIsImVtYWlsIjoidDY4QGV4YW1wbGUuY29tIiwicm9sZV9zbHVnIjoiYmFzaWMtdXNlciIsInByb2ZpbGVfaWQiOiJ1c3ItcHJmLTk3MDIyMWYxLTQwM2ItNGQwZS1iMjk5LTQ4YjRkZGNiNjdiNCIsImNvbXBhbnkiOm51bGwsImlhdCI6MTc1Njk0NzU2NC4wMjQ5NjEsImV4cCI6MTc1Njk1MTE2NH0.NGOCmpsTSug6I-6CfpzrcC8BHJj6vTGZ462ah1vPGjc", "my_super_secret_key", algorithms=["HS256"])
#         return JsonResponse(payload)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"error": e}, status=401)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import jwt, datetime, json
from .models import User

SECRET = getattr(settings, "JWT_SECRET", "mysecret")

@csrf_protect
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        user = User.objects.create(
            username=body["username"],
            email=body["email"],
            profile=body["profile"],
            password=make_password(body["password"])
        )
        return JsonResponse(
            {"msg": "User Successfully Registered", "id": str(user.id)},
            status=201
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_protect
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    body = json.loads(request.body)
    try:
        user = User.objects.get(email=body["email"])
    except User.DoesNotExist:
        return JsonResponse({"error": "invalid credentials"}, status=401)

    if not check_password(body["password"], user.password):
        return JsonResponse({"error": "invalid credentials"}, status=401)

    payload = {
        "id": str(user.id),
        "email": user.email,
        "role_slug": "basic-user",
        "profile_id": f"usr-prf-{str(user.id)}",
        "company": None,
        "iat": datetime.datetime.utcnow().timestamp(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")

    # store token
    user.auth_token = token
    user.save()

    return JsonResponse({"token": token}, status=200)


def profile(request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JsonResponse({"error": "no token"}, status=401)

    token = auth.split()[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return JsonResponse(payload)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "bad token"}, status=401)
    except Exception as e :
        return JsonResponse({"Error": str(e)})