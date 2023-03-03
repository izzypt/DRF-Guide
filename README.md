# DRF-Guide

This repo will cover the following topics and concepts about Django and , specifically, DRF:

- Serializers
  - serializers.Serializer
  - serializers.ModelSerializer
  - serializers.HyperlinkedModelSerializer
- Function Based View
  - @api_view()
- Class Based View
  - APIView
  - Generics Views
  - Mixins
  - Concrete View Classes
- Viewsets and Routers
- Permissions
  - IsAuthenticated
  - IsAdminUser
  - IsAuthenticatedOrReadOnly
  - CustomPermissions
- Authentication
  - Basic Authentication
  - Token Authentication
  - JWT Authentication
- Throttling
  - AnonRateThrottle
  - UserRateThrottle
  - ScopedRateThrottle
  - Custom Throttle
- Filtering
  - Filter
  - Search
  - Ordering
- Pagination
  - Page Number
  - Limit Offset
  - Cursor
- Automated API Testing

# What we will build ?

In order to cover all those topics , we will build an API that will serve movie data , like an IMDV or WatchMate clone.

# Installation

In order to use DRF , first we need to start a Django project. We can do it very simply, by following those steps:

1) Create a project folder for your app, let's call it ```DRF-Guide```
2) Create a virtual environment inside it , in order to keep our project packages isolated : ```python -m venv venv```
3) Activate virtual env by running ```.\venv\Scripts\activate``` or ```source venv/bin/activate``` if you are on Mac.
4) If the virtual env is installed and we run ```pip freeze``` we will be able to see that there are no packages installed in our virtualenv. So we will install everything from fresh.
5) So with a blank project and environment , let's install Django:  ```pip install Django```. 

# Starting project

1) Let's start our project inside the ```DRF-Guide```, running the command ```django-admin startproject IMDB```
2) Let's create a new app inside our project, to have our project's code dividide into modules : ```python manage.py startapp watchlist```
3) Add the newly create app in our ```settings.py``` file, in the ```INSTALLED_APPS```.

![image](https://user-images.githubusercontent.com/73948790/222804249-0373b994-5872-4241-8318-92a4a938fa1b.png)

4) Let's apply our migrations in order to create the first tables in our project DB: ```python manage.py makemigrations``` and then ```python manage.py migrate```
5) Next , let's create our superuser in order to access the admin panel: ```python manage.py createsuperuser```.
6) You check everything works fine by acessing the /admin endpoint on your running server.

# Models and Migrations

1) Let's start by creating a simple model in our ```models.py```, inside our ```watchlist``` app:

```
class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
```
2) Run the migrations for the newly created model : ```python manage.py makemigrations``` and then ```python manage.py migrate```
3) In order to access our newly created model from the admin panel, we need to register it in the ```admin.py``` file
```
from django.contrib import admin
from .models import Movie

# Register your models here.
admin.site.register(Movie)
```
