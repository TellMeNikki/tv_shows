from django.urls import path
from . import views

urlpatterns = [
  path("", views.register),
  path("register", views.register),
  path("login", views.login),
  path("logout", views.logout),
  path("shows/", views.shows),
  path("shows/create", views.create), 
  path("shows/<id_show>", views.desc),   
  path("shows/<id_show>/edit", views.edit),
  path("shows/<id_show>/update", views.update),
  path("<id_show>/destroy", views.delete), 
  path("second/<name>", views.second),
]
