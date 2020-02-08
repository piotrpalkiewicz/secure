from rest_framework import serializers

from protector.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    protected_url = serializers.HyperlinkedIdentityField(
        lookup_field="protected_url", view_name="protected-authorize", read_only=True
    )

    class Meta:
        model = Resource
        fields = (
            "id",
            "author",
            "created_at",
            "visits",
            "url",
            "file",
            "protected_url",
            "password",
        )
        read_only_fields = (
            "id",
            "created_at",
            "visits",
            "author",
            "protected_url",
            "password",
        )

    def validate(self, attrs):
        instance = Resource(**attrs)
        instance.clean()
        return attrs


class ResourceStatsSerializer(serializers.Serializer):
    created_at = serializers.DateField()
    files = serializers.IntegerField()
    links = serializers.IntegerField()


class ProtectedResourceSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="final_resource_url")

    class Meta:
        model = Resource
        fields = ("url",)
