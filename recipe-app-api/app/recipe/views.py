"""
Views for the recipe APIs.
"""

from core.models import (
    Ingredient,
    Recipe,
    Tag,
)
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter.",
            ),
            OpenApiParameter(
                "ingredients",
                OpenApiTypes.STR,
                description="Comma separated list of ingredient IDs to filter.",
            ),
            OpenApiParameter(
                "mine",
                OpenApiTypes.INT,
                enum=[0, 1],
                description="1 = only show recipes created by the logged-in user.",
            ),
        ],
        tags=["recipes"],
    ),
    retrieve=extend_schema(tags=["recipes"]),
    create=extend_schema(tags=["recipes"]),
    update=extend_schema(tags=["recipes"]),
    partial_update=extend_schema(tags=["recipes"]),
    destroy=extend_schema(tags=["recipes"]),
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a comma separated string to a list of integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """
        Return recipes.
        - Default: ALL recipes in the database (so users can browse everything)
        - ?mine=1: only the authenticated user's own recipes
        """
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        mine = bool(int(self.request.query_params.get("mine", 0)))

        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # Filter to user's own recipes only when ?mine=1
        if mine:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by("-id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer
        if self.action == "upload_image":
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe — always owned by the logged-in user."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Only the recipe owner may update."""
        recipe = self.get_object()
        if recipe.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to edit this recipe.")
        serializer.save()

    def perform_destroy(self, instance):
        """Only the recipe owner may delete."""
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this recipe.")
        instance.delete()

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe — only the recipe owner may do this."""
        recipe = self.get_object()
        if recipe.user != request.user:
            return Response(
                {"detail": "You do not have permission to upload an image to this recipe."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "assigned_only",
                OpenApiTypes.INT,
                enum=[0, 1],
                description="Filter by items assigned to recipes.",
            )
        ]
    )
)
class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for recipe attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get("assigned_only", 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by("-name").distinct()


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "assigned_only",
                OpenApiTypes.INT,
                enum=[0, 1],
                description="Filter by items assigned to recipes.",
            )
        ],
        tags=["tags"],
    ),
    update=extend_schema(tags=["tags"]),
    partial_update=extend_schema(tags=["tags"]),
    destroy=extend_schema(tags=["tags"]),
)
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "assigned_only",
                OpenApiTypes.INT,
                enum=[0, 1],
                description="Filter by items assigned to recipes.",
            )
        ],
        tags=["ingredients"],
    ),
    update=extend_schema(tags=["ingredients"]),
    partial_update=extend_schema(tags=["ingredients"]),
    destroy=extend_schema(tags=["ingredients"]),
)
class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
# Already handled above — appending nothing
