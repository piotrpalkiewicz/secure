from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from protector import services
from protector.models import Resource
from protector.serializers import (
    ResourceSerializer,
    ProtectedResourceSerializer,
    ResourceStatsSerializer,
)


class ResourceViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        qs = Resource.objects.visit_statistics()
        serializer = ResourceStatsSerializer(qs, many=True)
        return Response(serializer.data)


class ProtectedResourceViewset(viewsets.ViewSet):
    lookup_field = "protected_url"
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["post"])
    def authorize(self, request, protected_url):
        resource = Resource.objects.filter(protected_url=protected_url).first()
        password = request.POST.get("password")
        print(request.POST)
        print(request.POST)
        print(request.POST)
        print(request.POST)
        if not resource or not services.is_valid_link(resource.created_at):
            raise NotFound()
        if not password or not services.is_password_match(
            protected_url=protected_url, password=password
        ):
            raise ValidationError()
        serializer = ProtectedResourceSerializer(instance=resource)
        services.increment_resource_visits(resource)
        return Response(serializer.data)
