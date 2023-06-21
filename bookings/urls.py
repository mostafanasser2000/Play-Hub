from django.urls import path
from . import views


urlpatterns = [
    path('bookings/',views.BookingList.as_view(), name='bookings'),
    path('bookings/make-booking/<int:id>/',views.create_booking, name='make-booking'),
    path('bookings/accept/<int:id>/',views.accept_booking, name='booking-accept'),
    path('bookings/reject/<int:id>/',views.reject_booking, name='booking-reject'),
]
