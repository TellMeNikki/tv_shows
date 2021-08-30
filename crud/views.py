import bcrypt
from django.http import request
from crud.models import Network, Show,Users
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages


def register (request):    
  if request.method == 'GET':
    return render(request, 'login.html')
  else:
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']

    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
      for key, msg_error in errors.items():
        messages.error(request, msg_error)
      return redirect('/register')
        
    user = Users.objects.create(
      name=name,
      email=email,
      password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )
    messages.success(request, 'User created successful!')
    
    request.session['user'] = {
      'id': user.id,
      'name': user.name,
      'email': user.email,      
    }
    return redirect('/shows')


def login (request):
  pass

def shows(request):
    tvshows = Show.objects.all()
    networks = Network.objects.all()
    context = {
      "tvshows": tvshows, 
      "networks": networks, 
      }
    return render(request, "index.html", context)


def create(request):
  if request.method=='GET':
    networks = Network.objects.all()
    context = {
      "networks": networks,
    }
    return render(request, "create.html", context)

  if request.method=='POST':
    title=request.POST['show_title']
    network_id=int(request.POST['network_id'])
    release_date=request.POST['r_date']
    img_show=request.POST['url_img']
    description=request.POST['desc']
    Show.objects.create(
      title=title,network_id=network_id,release_date=release_date,img_show=img_show,description=description
    )
    messages.success(request, f'The show "{title}" has been created successfully!')
    return redirect('/shows')


def desc(request):
    context = {"saludo": "Hola new"}
    return render(request, "index.html", context)


def edit(request):
    context = {"saludo": "editando"}
    return render(request, "index.html", context)


def second(request, name):
    return HttpResponse("Hola " + name)
