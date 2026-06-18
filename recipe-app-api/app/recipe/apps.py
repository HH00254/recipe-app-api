"""
App configuration for the recipe app.
"""

from django.apps import AppConfig


class RecipeConfig(AppConfig):
    """Configuration for the recipe app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipe"
