from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from slots.models import Slot
from .models import Playground
from bookings.models import Booking


class OwnerRequiredMixin(AccessMixin):
    """Making sure that only owner of object can only update or delete it"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == "Player":
            raise PermissionDenied()

        obj = self.get_object()
        if isinstance(obj, Playground):
            if obj.owner != request.user:
                raise PermissionDenied()
        elif isinstance(obj, Slot):
            if obj.playground.owner != request.user:
                raise PermissionDenied()
        elif isinstance(obj, Booking):
            if obj.player != request.user:
                raise PermissionDenied
            
        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)


class CreateMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == "Player":
            raise PermissionDenied()
        return super(CreateMixin, self).dispatch(request, *args, **kwargs)
