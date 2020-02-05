from django.views.generic import CreateView


class ResourceCreateView(CreateView):
    form_class = ResourceForm
