from django.urls import path

from protector.views import ResourceCreateView

urlpatterns = [
    path("create/", ResourceCreateView.as_view(), name="resources-create"),
]
