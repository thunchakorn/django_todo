from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinLengthValidator

class Priority(models.Model):
    CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    level = models.CharField(max_length=64, choices=CHOICES)

    def __str__(self) -> str:
        return self.level

class Todo(models.Model):
    PUBLICITY_CHOICES = [
        (False, 'No'),
        (True, 'Yes')
    ]

    name = models.CharField(max_length=128)
    detail = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='todo_owned')
    due = models.DateTimeField()

    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(choices=PUBLICITY_CHOICES, default=False)

    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='todo_comment')

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Participant', related_name='participants')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.owner.username}:{self.name}"

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(1, "Comment must be greater than 1 character.")]
    )

    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_owned')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if len(self.text) > 10:
            return self.text[:10] + '...'
        else:
            return self.text

class Following(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')

    def __str__(self) -> str:
        return f"{self.user} -> {self.following_user}"

class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'todo')

    def __str__(self) -> str:
        return self.user + "->" + self.following_user
