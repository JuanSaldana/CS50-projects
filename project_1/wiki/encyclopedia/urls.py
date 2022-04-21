from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search/", views.search_results, name="search_results"),
    path("create/", views.create_entry, name="create_page"),
    path("save/<str:state>/", views.save_entry, name="save_entry"),
    path("edit/<str:entry_name>", views.edit_entry, name="edit_entry")
]
