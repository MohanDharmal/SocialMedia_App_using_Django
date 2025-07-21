from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Profile model: extended user info
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)
    bio = models.TextField(blank=True, default='')
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username

# Post model
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Post"

# LikesPost model
class LikesPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

# Followers model
class Followers(models.Model):
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)  # The one being followed
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)  # The one following

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.id}"
    
User = get_user_model()
class Message(models.Model):
    sender = models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receive_message',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.sender.username} To {self.receiver.username}"
    
    
     