"""
Serializers for recipe APIs.
"""

from core.models import Recipe, Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        """Meta class for the serializer."""

        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        """Meta class for the serializer."""

        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""

        auth_user = self.context["request"].user

        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_object)

    def create(self, validated_data):
        """Overiding the baseMethod and Create a recipe."""

        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags=tags, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe"""

        tags = validated_data.pop("tags", None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        """Meta class for the serializer."""

        fields = RecipeSerializer.Meta.fields + ["description"]
