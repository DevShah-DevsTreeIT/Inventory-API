from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import jwt, datetime, json
from .models import User

SECRET = getattr(settings, "JWT_SECRET", "mysecret")

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    body = json.loads(request.body)
    try:
        user = User.objects.create(
            username=body["username"],
            email=body["email"],
            password=make_password(body["password"])
        )
        return JsonResponse({"msg": "User Successfully Registered", "id": user.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
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
        "id": user.id,
        "email": user.email,
        "role_slug": "basic-user",  # static role for now
        "profile_id": f"usr-prf-{user.id}",
        "company": None,
        "iat": datetime.datetime.utcnow().timestamp(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")

    # ✅ store token in DB
    user.auth_token = token
    user.save()

    return JsonResponse({"token": token}, status=200)


@csrf_exempt
def me(request):
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