from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Slot
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SlotForm
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import CreateMixin, OwnerRequiredMixin


class SlotList(LoginRequiredMixin, ListView):
    model = Slot
    context_object_name = "slots"
    paginate_by = 10

    def get_queryset(self):
        qs = Slot.free_slots.all()
        if self.request.user.role == "Player":
            return qs

        return qs.filter(playground__in=self.request.user.playgrounds.all())


class SlotCreate(LoginRequiredMixin, CreateMixin, CreateView):
    model = Slot
    success_url = reverse_lazy("slots:slot_list")
    form_class = SlotForm

    # limit playground to only those owned by owner
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields["playground"].limit_choices_to = {
            "owner": self.request.user
        }
        return modelform

    def form_valid(self, form):
        messages.success(self.request, "Slot is added successfully")
        return super(SlotCreate, self).form_valid(form)


class SlotUpdate(LoginRequiredMixin, UpdateView):
    model = Slot
    success_url = reverse_lazy("slots:slot_list")
    context_object_name = "slot"
    form_class = SlotForm

    def form_valid(self, form):
        messages.success(self.request, "Slot is updated successfully")
        return super(SlotUpdate, self).form_valid(form)


class SlotDelete(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Slot
    success_url = reverse_lazy("slots:slot_list")

    def form_valid(self, form):
        messages.success(self.request, "Slot is deleted successfully")
        return super(SlotDelete, self).form_valid(form)
