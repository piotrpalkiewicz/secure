from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from protector.forms import ResourceForm
from protector.models import Resource


class ResourceCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
    success_url = reverse_lazy("protector-resource_detail")


class ResourceDetailView(DetailView):
    model = Resource
    fields = ()
