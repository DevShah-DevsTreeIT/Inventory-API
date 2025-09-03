from django.db import models
from django.db import models
import uuid


# User Table
class User(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)  #here when we use unique=True it will not allow duplicate emails 
    user_password = models.CharField(max_length=255)  # Later you can hash this
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #This field is designed to store Universally Unique Identifiers (UUIDs) and possesses specific characteristics
    # auth_token = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name    


