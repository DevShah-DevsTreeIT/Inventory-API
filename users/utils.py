from django.http import JsonResponse
from django.conf import settings
import jwt

SECRET = getattr(settings, "JWT_SECRET", "mysecret")


def is_authenticated(view_func):
    """
    Custom decorator to enforce JWT authentication.
    """
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"error": "Missing or invalid token"}, status=401)

        token = auth.split()[1]
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            request.user_payload = payload   # attach user info
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper
