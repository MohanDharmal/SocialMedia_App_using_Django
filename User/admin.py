from django.contrib import admin
from .models import Profile, Post, LikesPost, Followers

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikesPost)
admin.site.register(Followers)