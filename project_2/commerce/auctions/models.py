from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="last_winner")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.description} /nStarting Bid: {self.starting_bid}/n Created by: {self.created_by} at {self.created_at}"


class Comment(models.Model):
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"On listing: {self.listing.title}:\n{self.comment} /n Created by: {self.created_by} at {self.created_at}"
