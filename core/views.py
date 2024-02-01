from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Playground, Attachment
from .forms import PlaygroundForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.forms import ImageField
from .mixins import OwnerRequiredMixin, CreateMixin


# Create your views here.


def home(request):
    return render(request, "home.html")


class PlaygroundsList(LoginRequiredMixin, ListView):
    model = Playground
    context_object_name = "playgrounds"
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name", "")
        capacity = self.request.GET.get("capacity", "")
        ttype = self.request.GET.get("type", "")

        qs = Playground.objects.all()

        if name:
            name = name.strip()
            qs = qs.filter(Q(name__icontains=name) | Q(city__icontains=name))
        if capacity:
            qs = qs.filter(capacity=capacity)
        if ttype:
            qs = qs.filter(grass_type=ttype)

        if self.request.user.role == "Owner":
            return qs.filter(owner=self.request.user)
        return qs


class PlaygroundDetail(LoginRequiredMixin, DetailView):
    model = Playground
    context_object_name = "playground"


class PlaygroundCreate(LoginRequiredMixin, CreateMixin, CreateView):
    model = Playground
    form_class = PlaygroundForm
    success_url = reverse_lazy("core:playground_list")

    def form_valid(self, form):
        playground = form.save(commit=False)
        playground.owner = self.request.user
        playground.save()

        additional_images = self.request.FILES.getlist("additional_images")
        if additional_images:
            for img in additional_images:
                Attachment.objects.create(playground=playground, image=img)
        messages.success(self.request, f"Playground is created successfully")
        return super(PlaygroundCreate, self).form_valid(form)


class PlaygroundUpdate(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Playground
    form_class = PlaygroundForm

    def get_form_class(self):
        obj = self.get_object()
        model_form = super().get_form_class()
        model_form.base_fields["image"] = ImageField(initial=obj.image)
        return model_form

    success_url = reverse_lazy("core:playground_list")
    context_object_name = "playground"

    def form_valid(self, form):
        messages.info(self.request, "Playground info is updated successfully")
        additional_images = self.request.FILES.getlist("additional_images")
        if additional_images:
            for img in additional_images:
                Attachment.objects.create(playground=form.instance, image=img)
        return super(PlaygroundUpdate, self).form_valid(form)


class PlaygroundDelete(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Playground
    context_object_name = "playground"
    success_url = reverse_lazy("core:playground_list")
    raise_exception = True

    def form_valid(self, form):
        messages.info(self.request, "Playground is deleted successfully")
        return super(PlaygroundDelete, self).form_valid(form)


@login_required()
def filter(request):
    return render(request, "filter_form.html")
