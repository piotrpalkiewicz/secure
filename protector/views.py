from django.views.generic import CreateView

from protector.forms import ResourceForm
from protector.models import Resource


class ResourceCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
