import boto3
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic.detail import BaseDetailView

from protector import utils, services
from protector.forms import ResourceForm, ResourcePermissionForm
from protector.models import Resource


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.protected_url = utils.generate_protected_url()
        form.instance.password = utils.generate_password()
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


class ResourceProtectedDetailView(FormView):
    template_name = "protector/resource_protection_form.html"
    slug_field = "protected_url"
    slug_url_kwarg = "protected_url"
    form_class = ResourcePermissionForm

    def get_object(self):
        return get_object_or_404(Resource, **self.kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {
            "protected_url": self.object.protected_url,
            "password": request.POST.get("password"),
        }
        form = self.form_class(data)
        if form.is_valid():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.get_object().url


class DownloadFileView(BaseDetailView):
    model = Resource

    def get(self, request, *args, **kwargs):
        file_url = services.get_file(self.get_object().file.name)
        return HttpResponseRedirect(file_url)
