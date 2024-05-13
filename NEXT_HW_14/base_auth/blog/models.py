import datetime
from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    last_viewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="last_viewed_posts",
        null=True,
    )
    last_viewed_datetime = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    image_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.content


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscribers"
    )
