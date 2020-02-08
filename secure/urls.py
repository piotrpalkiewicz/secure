"""secure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers

from django.contrib import admin
from django.urls import include, path

from protector import api_views as protector_views


router = routers.DefaultRouter()
router.register(r"resource", protector_views.ResourceViewset, basename="resource")
router.register(
    r"protected", protector_views.ProtectedResourceViewset, basename="protected"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("protector/", include("protector.urls")),
    path("api/v1/", include(router.urls)),
]
