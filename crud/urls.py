from django.urls import path
from . import views

urlpatterns = [
  path("", views.register),
  path("register", views.register),
  path("login", views.login),
  path("shows/", views.shows),
  path("shows/create", views.create), 
  path("shows/<id>", views.desc),   
  path("shows/<id>/update", views.edit), 
  path("second/<name>", views.second),
]
