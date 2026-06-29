"""
Models for the comments app.
"""

from django.conf import settings
from django.db import models


class Comment(models.Model):
    """Comment on a recipe."""

    recipe = models.ForeignKey(
        "core.Recipe",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.email} on {self.recipe.title}"
