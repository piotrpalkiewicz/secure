from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from protector import services
from protector.forms import ResourceForm
from protector.models import Resource


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    success_url = reverse_lazy("protector-resource_detail")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.protected_url = services.generate_protected_url()
        return super().form_valid(form)


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    fields = ()


class ResourceProtectedDetailView(DetailView):
    model = Resource
    fields = ()
    template_name = "protector/resource_protection_form.html"
    slug_field = "protected_url"
