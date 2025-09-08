from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(User):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    # username = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=255)  # hashed
    # profile = models.ImageField(upload_to="profile", null=True, blank=True)
    auth_token = models.TextField(null=True, blank=True, editable=False)  # store latest JWT
    # created_at = models.DateTimeField(auto_now_add=True)    
    role = models.CharField(default="Basic")
    def __str__(self):  
        return self.username    