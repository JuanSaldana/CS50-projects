from django.contrib import admin
from .models import (Auction, Comment, User)

# Register your models here.
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(User)
