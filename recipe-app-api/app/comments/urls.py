"""
URL mappings for the comments API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from comments import views

router = DefaultRouter()
router.register("", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
]
