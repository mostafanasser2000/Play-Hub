from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("playgrounds/", views.PlaygroundsList.as_view(), name="playground_list"),
    path(
        "playgrounds/<int:pk>/<slug:name>/",
        views.PlaygroundDetail.as_view(),
        name="playground_detail",
    ),
    path(
        "playgrounds/create/",
        views.PlaygroundCreate.as_view(),
        name="playground_create",
    ),
    path(
        "playgrounds/update/<int:pk>/<slug:name>/",
        views.PlaygroundUpdate.as_view(),
        name="playground_update",
    ),
    path(
        "playgrounds/delete/<int:pk>/<slug:name>/",
        views.PlaygroundDelete.as_view(),
        name="playground_delete",
    ),
    path("playground-filter/", views.filter, name="playground_filter"),
]
