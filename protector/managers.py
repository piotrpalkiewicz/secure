from django.db import models


class ResourceManager(models.Manager):
    def visit_statistics(self):
        return (
            (
                self.get_queryset()
                .filter(visits__gt=0)
                .values("created_at")
                .annotate(
                    is_file=models.Case(models.When(url="", then=1), output_field=models.IntegerField(),),
                )
                .annotate(
                    is_url=models.Case(models.When(file="", then=1), output_field=models.IntegerField(),),
                )
                .annotate(links=models.Count("is_url"))
                .annotate(files=models.Count("is_file"))
                .values("created_at", "links", "files")
            )
            .annotate(models.Count("created_at"))
            .order_by("-created_at")
        )
