from typing import Type
from django.forms.models import BaseModelForm
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Slot
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SlotForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from core.models import Playground
import datetime
from django.db.models import Q


class OwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'Player':
            messages.error( request , "Permission Denied")
            return redirect('slot-list')
        
        slot = self.get_object()
        if slot.playground.owner != request.user:
            messages.error(self.request, 'Permission Denied')
            return redirect('slot-list')
        return super(OwnerRequiredMixin,self).dispatch(request, *args, **kwargs)


class CreateMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'Player':
            messages.error( request , "Permission Denied")
            return redirect('slot-list')
        return super().dispatch(request, *args, **kwargs)
    
    
class SlotList(LoginRequiredMixin,ListView):
    model = Slot
    context_object_name = 'slots'
    paginate_by = 5
    
    def get_queryset(self):
        qs = Slot.objects.filter(Q(day__gte=datetime.date.today()) & Q(status='FREE')).order_by('day')
        if self.request.user.role == 'Player':
            return  qs
        
        grounds = Playground.objects.filter(owner=self.request.user)
        return qs.filter(playground__in=grounds)


# class SlotDetail(LoginRequiredMixin,DetailView):
#     model = Slot
#     context_object_name = 'slot'
    

class SlotCreate(LoginRequiredMixin,CreateMixin, CreateView):
    model = Slot
    success_url = reverse_lazy('slot-list')
    form_class = SlotForm
    
    # limit playground to only those owned by owner
    def get_form_class(self):
        modelform =  super().get_form_class()
        modelform.base_fields['playground'].limit_choices_to = {'owner':self.request.user}
        return modelform
    
    
    def form_valid(self, form):
        day = form.cleaned_data['day']
        start = form.cleaned_data['start_hour']
        end = form.cleaned_data['end_hour']
        playground = form.cleaned_data['playground']
        slots = Slot.objects.filter(Q(day=day) & Q(start_hour=start) & Q(end_hour=end) & Q(playground=playground))
        if slots:
            messages.error(self.request, 'Slot with these information already exist')
            return redirect('slot-list')
        messages.success(self.request, "Slot is added successfully")
        return super(SlotCreate, self).form_valid(form)
    

class SlotUpdate(LoginRequiredMixin,OwnerRequiredMixin,UpdateView):
     model = Slot
     success_url = reverse_lazy('slot-list')
     context_object_name = 'ground'
     

    
     def form_valid(self, form):
        day = form.cleaned_data['day']
        start = form.cleaned_data['start_hour']
        end = form.cleaned_data['end_hour']
        playground = form.cleaned_data['playground']
        slots = Slot.objects.filter(Q(day=day) & Q(start_hour=start) & Q(end_hour=end) & Q(playground=playground))
        obj = self.get_object()
        if slots and slots[0] != obj:
            messages.error(self.request, 'Slot with these information already exist')
            return redirect('slot-list')
        messages.success(self.request, "Slot is updated sucessfully")
        return super(SlotUpdate, self).form_valid(form)


class SlotDelete(LoginRequiredMixin,OwnerRequiredMixin,DeleteView):
    model = Slot
    success_url = reverse_lazy('slot-list')
    
    def form_valid(self,form):
        messages.success(self.request, "Slot is deleted sucessfully")
        return super(SlotDelete, self).form_valid(form)