from django.contrib import messages
from django.views.generic.list import ListView
from .models import Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Playground 
from slots.models import Slot
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

class BookingList(LoginRequiredMixin,ListView):
    model = Booking
    context_object_name = 'bookings'
    paginate_by = 5
    def get_queryset(self) :
        
        if self.request.user.role == 'Owner':
            playgrounds = Playground.objects.filter(owner=self.request.user)
            palygrounds_slots = Slot.objects.filter(playground__in=playgrounds)
            return Booking.objects.filter(slot__in=palygrounds_slots)
        return Booking.objects.filter(player=self.request.user).order_by('slot')

@login_required()
def create_booking(request, id):
    if request.user.role == 'Owner':
        messages.error(request, "only palyers can make bookings")
        return redirect('slot-list')

    slot_to_book = Slot.objects.get(pk=id)
    booking_before = Booking.objects.filter(Q(player=request.user) & Q(slot=slot_to_book))
    if booking_before :
        messages.info(request,"Your already make a request for this slot")
        return redirect('bookings')
    
    booking = Booking.objects.create(player=request.user, slot=slot_to_book)
    booking.save()
    return redirect('bookings')


@login_required()
def accept_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    if booking.slot.playground.owner != request.user:
        messages.error(request, "You are not allowed to do that")
        return redirect('bookings')
    slot = Slot.objects.get(pk=booking.slot.id)
    slot.status = 'BOOKED'
    slot.save()
    booking.status = 'accepted'
    booking.save()
    return redirect('bookings')


@login_required()
def reject_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    if booking.slot.playground.owner != request.user:
        messages.error(request, "You are not allowed to do that")
        return redirect('bookings')
    booking.status = 'rejected'
    booking.save()
    return redirect('bookings')


@login_required()
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    if request.user != booking.player:
        messages.error(request, "You are not allowed to do that")
        return redirect('bookings')
    booking.delete()
    messages.info(request, 'boooking is canceled')
    return redirect('bookings')


