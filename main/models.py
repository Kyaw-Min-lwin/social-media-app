from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    # Add any other custom fields as needed

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, null=True, blank=True)

    @property
    def post_like_count(self):
        count = Like.objects.filter(post=self).count()
        return count


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
