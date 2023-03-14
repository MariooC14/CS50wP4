from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    poster = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    message = models.TextField(
        blank=False,
        max_length=500
    )

    like_count = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(
        auto_now_add=True)

    # For JSON
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "message": self.message,
            "timestamp": self.last_edited.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.like_count
        }

    def __str__(self):
        return f"{self.poster}'s post last created on {self.date_created.strftime('%b %d %Y, %I:%M %p')}"


# TODO: Like count
class UserLikesPosts(models.Model):
    id = models.BigAutoField(primary_key=True)
    likee = models.ManyToManyField(Post)
    liker = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.liker} likes {self.likee}"