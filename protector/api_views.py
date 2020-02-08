from django.db.models import Case, IntegerField, When, Count
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from protector import services
from protector.models import Resource
from protector.serializers import ResourceSerializer, ProtectedResourceSerializer, ResourceStatsSerializer


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
        qs = (
            Resource.objects.filter(visits__gt=0)
            .values("created_at")
            .annotate(is_file=Case(When(url="", then=1), output_field=IntegerField(),),)
            .annotate(is_url=Case(When(file="", then=1), output_field=IntegerField(),),)
            .annotate(links=Count("is_url"))
            .annotate(files=Count("is_file"))
            .values("created_at", "links", "files")
        ).annotate(Count("created_at")).order_by("-created_at")
        serializer = ResourceStatsSerializer(qs, many=True)
        return Response(serializer.data)


class ProtectedResourceViewset(viewsets.ViewSet):
    lookup_field = "protected_url"
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["post"])
    def authorize(self, request, protected_url):
        resource = Resource.objects.filter(protected_url=protected_url).first()
        if not resource or not services.is_valid_link(resource.created_at):
            raise NotFound()
        serializer = ProtectedResourceSerializer(instance=resource)
        services.increment_resource_visits(resource)
        return Response(serializer.data)
