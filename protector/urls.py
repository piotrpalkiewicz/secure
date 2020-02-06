from django.urls import path

from protector.views import (
    ResourceCreateView,
    ResourceDetailView,
    ResourceProtectedDetailView,
)

urlpatterns = [
    path("create/", ResourceCreateView.as_view(), name="protector-resource_create"),
    path("detail/<pk>", ResourceDetailView.as_view(), name="protector-resource_detail"),
    path(
        "protected/<protected_url>",
        ResourceProtectedDetailView.as_view(),
        name="protector-resource_protected",
    ),
]
