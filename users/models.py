from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed
    profile = models.ImageField(upload_to="profile", null=True, blank=True)
    auth_token = models.TextField(null=True, blank=True, editable=False)  # store latest JWT
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.username
