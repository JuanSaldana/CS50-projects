from re import A
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    created_at = models.TimeField(auto_now=True)
    body = models.TextField(blank=False)