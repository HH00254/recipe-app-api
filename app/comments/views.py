"""
Views for the comments API.
"""

from comments.models import Comment
from comments.serializers import CommentSerializer
from core.models import Recipe
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(tags=["comments"]),
    create=extend_schema(tags=["comments"]),
    destroy=extend_schema(tags=["comments"]),
)
class CommentViewSet(
    viewsets.GenericViewSet,
):
    """ViewSet for managing comments on recipes."""

    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def _get_recipe(self):
        """Retrieve the recipe from the URL kwarg, raise 404 if not found."""
        recipe_pk = self.kwargs.get("recipe_pk")
        try:
            return Recipe.objects.get(pk=recipe_pk)
        except Recipe.DoesNotExist:
            raise NotFound(detail="Recipe not found.")

    def get_queryset(self):
        recipe = self._get_recipe()
        return Comment.objects.filter(recipe=recipe)

    def list(self, request, *args, **kwargs):
        """List all comments for a recipe."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a comment on a recipe."""
        recipe = self._get_recipe()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a comment — only the comment author may do this."""
        recipe = self._get_recipe()
        try:
            comment = Comment.objects.get(pk=kwargs["pk"], recipe=recipe)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found.")

        if comment.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
