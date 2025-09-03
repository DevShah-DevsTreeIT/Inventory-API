from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Whatever your user model exposes (username/user_name/email, etc.)
        return Response({
            "id": request.user.id,
            "username": getattr(request.user, "username", None) or getattr(request.user, "user_name", None),
            "email": getattr(request.user, "email", None),
        })
    
    