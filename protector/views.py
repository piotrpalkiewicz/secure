from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from protector import services
from protector.forms import ResourceForm
from protector.models import Resource


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.protected_url = services.generate_protected_url()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("protector-resource_detail", args=(self.object.pk,))


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource

    def dispatch(self, request, *args, **kwargs):
        # it is good to use permissions library like guardian - but it's overhead right now
        if self.get_object().author != request.user and not request.user.is_superuser:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ResourceProtectedDetailView(DetailView):
    model = Resource
    fields = ()
    template_name = "protector/resource_protection_form.html"
    slug_field = "protected_url"
