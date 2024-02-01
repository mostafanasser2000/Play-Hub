from django.urls import path
from . import views

app_name = "slots"
urlpatterns = [
    path("", views.SlotList.as_view(), name="slot_list"),
    path("slots/create/", views.SlotCreate.as_view(), name="slot_create"),
    path("slots/update/<int:pk>/", views.SlotUpdate.as_view(), name="slot_update"),
    path("slots/delete/<int:pk>/", views.SlotDelete.as_view(), name="slot_delete"),
]
