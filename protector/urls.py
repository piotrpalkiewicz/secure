from django.urls import path

from protector.views import ResourceCreateView, ResourceDetailView

urlpatterns = [
    path("create/", ResourceCreateView.as_view(), name="protector-resource_create"),
    path("create/", ResourceDetailView.as_view(), name="protector-resource_detail"),
]
