from django.shortcuts import render, redirect, HttpResponse
from django.db import IntegrityError
from django.contrib import messages

def login_rq(func):
  def wrapper(request, *args, **kwargs):
    if 'user' not in request.session:
      messages.error(request,'Please, sign in or register')
      return redirect ('/register')
    log_rq = func(request, *args, **kwargs)
    return log_rq
  return wrapper

