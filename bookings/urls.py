from django.urls import path
from . import views

app_name = "bookings"
urlpatterns = [
    path("", views.BookingList.as_view(), name="booking_list"),
    path("bookings/make-booking/<int:id>/", views.create_booking, name="make_booking"),
    path("bookings/accept/<int:id>/", views.accept_booking, name="booking_accept"),
    path("bookings/reject/<int:id>/", views.reject_booking, name="booking_reject"),
    path("bookings/cancel/<int:id>/", views.cancel_booking, name="booking_cancel"),
]
