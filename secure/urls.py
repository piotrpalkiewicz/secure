from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from rest_framework import routers
from rest_framework.reverse import reverse_lazy

from protector import api_views as protector_views

router = routers.DefaultRouter()
router.register(r"resource", protector_views.ResourceViewset, basename="resource")
router.register(
    r"protected", protector_views.ProtectedResourceViewset, basename="protected"
)

urlpatterns = [
;
    path("admin/", admin.site.urls),
    path("protector/", include("protector.urls")),
    path("api/v1/", include(router.urls)),
    path("", RedirectView.as_view(url=reverse_lazy('protector-resource_create')), name="home")
]
