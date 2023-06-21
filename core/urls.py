from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('playgrounds/', views.PlaygroundsList.as_view(), name='playground-list'),
    path('playgrounds/<int:pk>/', views.PlaygroundDetail.as_view(), name='playground-detail'),
    path('playgrounds/create/', views.PlaygroundCreate.as_view(), name='playground-create'),
    path('playgrounds/update/<int:pk>/', views.PlaygroundUpdate.as_view(), name='playground-update'),
    path('playgrounds/delete/<int:pk>', views.PlaygroundDelete.as_view(), name='playground-delete'),
    path('playground-filter/', views.filter, name='playground-filter')

 
]
