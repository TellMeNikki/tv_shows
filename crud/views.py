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

    request.session['user'] = {
      'id': user.id,
      'name': user.name,
      'email': user.email,      
    }
    # messages.success(request, 'User created successful!')
    return redirect('/shows', )


def login(request):
  email = request.POST['email']
  password = request.POST['password']
  try:
    user = Users.objects.get(email=email)
  except Users.DoesNotExist:
    messages.error(request, 'User or Password does not exist!')
    return redirect('/register')
    
  if not bcrypt.checkpw(password.encode(), user.password.encode()): 
    messages.error(request, 'User or Password does not exist!')
    return redirect('/register')
    
  request.session['user'] = {
    'id': user.id,
    'name': user.name,
    'email': user.email,      
  }
  # messages.success(request, 'User created successful!')
  return redirect('/shows')


def logout (request):
  del  request.session['user']
  return redirect('/register')


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

  errors = Show.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect(request.META.get('HTTP_REFERER'))
  else:
    s_title=request.POST['show_title']
    network_id=int(request.POST['network_id'])
    release_date=request.POST['r_date']
    img_show=request.POST['url_img']
    description=request.POST['desc']

    Show.objects.create(
      title=s_title,
      network_id=network_id,
      release_date=release_date,
      img_show=img_show,
      description=description
    )
    messages.success(request, 'The show has been created successfully!')
    return redirect( '/shows')


def desc(request,id_show):
  show = Show.objects.get(id=id_show)
  network = Network.objects.all()
  date_st = show.release_date.strftime("%B %d , %Y")
  last_up = show.updated_at.strftime("%B %d , %Y  %I:%S %p") 
  context = {
    "show": show, 
    "network":network,
    "date_st":date_st,
    "last_up":last_up,

  }
  return render(request, "desc.html", context)


def edit(request, id_show):
  show = Show.objects.get(id=id_show)
  networks = Network.objects.all()
  date_st = show.release_date.strftime('%Y-%m-%d')
  context = {
    "show": show, 
    "networks":networks,
    "date_st":date_st
  }
  return render(request, "update.html", context)


def update(request,id_show):
  if request.method == 'GET':
    show = Show.objects.get(id=id_show)
    networks = Network.objects.all()
    date_st = show.release_date.strftime('%Y-%m-%d')
    context = {
      "show": show, 
      "networks":networks,
      "date_st":date_st
    }
    return render(request, "update.html", context)
  else: 
        show = Show.objects.get(id=id_show)
        show.title=request.POST['show_title']
        show.network_id=int(request.POST['network_id'])
        show.release_date=request.POST['r_date']
        show.img_show=request.POST['url_img']
        show.description=request.POST['desc']

        show.save()
        messages.success(request, f'The show was modified successful!')
        return redirect('/shows')


def delete (request, id_show):
  show=Show.objects.get (id=id_show)
  show.delete()
  return redirect('/shows')

def second(request, name):
    return HttpResponse("Hola " + name)
