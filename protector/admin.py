from django.contrib import admin

from protector.models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "__str__",
        "visits",
    )
    readonly_fields = (
        "author",
        "visits",
    )
