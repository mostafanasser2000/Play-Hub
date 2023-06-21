from typing import Type
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Playground
from .forms import PlaygroudnForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils.translation import gettext as _
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.forms import ImageField
# Create your views here.

def home(request):
    return render(request, 'home.html')


class OnwerRequiredMixin(AccessMixin):
    """Making sure that only owner of playground can only update playgrounds"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'Player':
            messages.error(request, "Permession Denied")
            return redirect('playground-list')
        
        obj = self.get_object()
        if   obj.owner != request.user:
            messages.error(request, "Permession Denied")
            return redirect('playground-list')
        return super(OnwerRequiredMixin,self).dispatch(request, *args, **kwargs)


class CreateMixin(AccessMixin):
    """Making sure that only owners can create playgrounds"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'Player':
            messages.error(request, "Permession Denied")
            return redirect('playground-list')
        return super(CreateMixin,self).dispatch(request, *args, **kwargs)
    
    
    
    
class PlaygroundsList(LoginRequiredMixin, ListView):
    model = Playground
    context_object_name = 'grounds'
    paginate_by = 3

    def get_queryset(self):
       name = self.request.GET.get('name','')
       capcity = self.request.GET.get('capcity','')
       ttype = self.request.GET.get('type','')
       
       print(name, capcity, ttype)
       qs = Playground.objects.all()
       if name:
           name = name.strip()
           qs = qs.filter(Q(name__icontains=name) | Q(city__icontains=name))
           print(qs)
       if capcity:
            qs = qs.filter(capcity=capcity)
            print(qs)
       if ttype:
            qs = qs.filter(grass_type=ttype)
            print(qs)
       if self.request.user.role == 'Owner':
           return qs.filter(owner=self.request.user)
       return qs
    


class PlaygroundDetail(LoginRequiredMixin,OnwerRequiredMixin,DetailView):
    model = Playground
    context_object_name = 'ground'
    
    def get_queryset(self):
        qs = super(PlaygroundDetail,self).get_queryset()
        if self.request.user.role == 'Owner':
            return qs.filter(owner=self.request.user)
        return qs
    

class PlaygroundCreate(LoginRequiredMixin,CreateMixin,CreateView):
    model = Playground
    form_class = PlaygroudnForm
    success_url = reverse_lazy('playground-list')
    
    def form_valid(self, form) :
        name = form.cleaned_data['name']
        city = form.cleaned_data['city']
        address = form.cleaned_data['address']
        playground = Playground.objects.filter(Q(name__iexact=name)& Q(city__iexact=city)&Q (address__iexact=address))
        if playground: 
            print("match")
            messages.error(self.request, "Playground with this information already exist")
            return redirect('playground-list')
        form.instance.owner = self.request.user
        messages.success(self.request, f"{name} Playground is added successfully")
        return super(PlaygroundCreate,self).form_valid(form)


class PlaygroundUpdate(LoginRequiredMixin,OnwerRequiredMixin,UpdateView):
    model = Playground
    form_class = PlaygroudnForm

    def get_form_class(self):
        obj = self.get_object()
        model_form = super().get_form_class()
        model_form.base_fields['image'] = ImageField(initial=obj.image)
        return model_form
    
    success_url = reverse_lazy('playground-list')
    context_object_name = 'ground'

    def form_valid(self, form):
        obj = self.get_object()
        name = form.cleaned_data['name']
        city = form.cleaned_data['city']
        address = form.cleaned_data['address']
        playground = Playground.objects.filter(Q(name__iexact=name)& Q(city__iexact=city)&Q (address__iexact=address))
        if playground and playground[0] != obj: 
            messages.error(self.request, "Playground with this information already exist")
            return redirect('playground-list')
        messages.info(self.request, "Playground info is updated sucessfully")
        return super(PlaygroundUpdate,self).form_valid(form)

    
    
        

class PlaygroundDelete(LoginRequiredMixin,OnwerRequiredMixin,DeleteView):
    model = Playground
    context_object_name = 'ground'
    success_url = reverse_lazy('playground-list')
    raise_exception = True
    
    def form_valid(self, form):
        messages.info(self.request, "Playground is deleted sucessfully")
        return super(PlaygroundDelete, self).form_valid(form)

    def get_queryset(self):
        qs = super(PlaygroundDelete, self).get_queryset()
        if self.request.user.role == 'Owner':
            return qs.filter(owner=self.request.user)
        return qs
    

@login_required()
def filter(request):
    return render(request, 'filter_form.html')


def resize_image(image):
    new_image = Image.open(image)
    new_image = new_image.resize((300,500))
    new_image.save()
    