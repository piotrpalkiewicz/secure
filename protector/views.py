from django.views.generic import CreateView

from protector.forms import ResourceForm


class ResourceCreateView(CreateView):
    form_class = ResourceForm
