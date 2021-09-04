from django.db import models
from datetime import date, datetime

class UsersManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    if len(postData['name']) < 4:
      errors["name"] = "User name should be at least 4 characters"        
    if len(postData['email']) < 4:
      errors["email"] = "Invalid E-mail address. It should be at least 4 characters"        
    if len(postData['password']) < 6:
      errors["password"] = "Invalid password, it should be at least 4 characters"        
    if postData['password'] != postData['password_confirm']:
      errors["password"] = "Passwords didn't match. Please try again"        
    return errors
    

class ShowManager(models.Manager):    
  def basic_validator(self, postData):
    errors = {}
    if len(postData['show_title']) < 2:
      errors["title"] = "Title should have at least 2 characters"
    if len(postData['network_id']) == 'Choose a Network...':
      errors["network"] = "please select an option"
    try:             
      if datetime.strptime(postData['r_date'],"%Y-%m-%d").date() > datetime.today().date():                 
        errors['r_date'] = 'The release time should be today or earlier'         
    except ValueError:
      errors['r_date'] = 'You should pick a date'
    if len(postData['desc']) < 10:
      errors["desc"] = "description should have at least 10 characters"
    return errors

class Users(models.Model):
  name = models.CharField(max_length=150)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=30)
  allowed = models.BooleanField(default=True)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UsersManager()

  def __repr__(self) -> str:
    return f'{self.id}: {self.name}' 

class Network(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __repr__(self):
    return f"<Tv object: {self.title} ({self.id})>"

class Show(models.Model):
  title = models.CharField(max_length=255)
  network = models.ForeignKey(Network, related_name="network", on_delete = models.CASCADE)
  release_date = models.DateTimeField()
  img_show = models.URLField(default='https://www.pngkey.com/png/full/331-3315307_our-insert-name-here-meme.png')
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects=ShowManager()

  def __repr__(self):  
    return f"<Tv object: {self.title} ({self.id})>"


