from django.urls import path
from . import views

urlpatterns = [
    path('slots/', views.SlotList.as_view(), name='slot-list'),
    path('slots/create/', views.SlotCreate.as_view(), name='slot-create'),
    path('slots/update/<int:pk>/', views.SlotUpdate.as_view(), name='slot-update'),
    path('slots/delete/<int:pk>/', views.SlotDelete.as_view(), name='slot-delete'),
]
