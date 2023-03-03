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
4) We are now able to add new movies from the admin panel.

# Creating JSON Response with vanilla Django.

In order to understand why DRF is so usefull , let's first start by serving our movie data with the built-in logic that Django provides. Later , we can see how DRF will build and improve on that-

1) We will create a view in our ```views.py``` to return a list of the movies we have in our DB , this is what it looks like with "vanilla" Django:
```
from .models import Movie
from django.http import JsonResponse

def movie_list(request):
    # The next line will fetch all the movies from DB and store them in a queryset
    movies = Movie.objects.all()
    
    # Because we cannot send the response as a querset, we need to transform the queryset.
    data = {
        # Using .values() we get the values each object of the queryset as a dictionarie.
        # And then wrapping the queryset in a list to transform it into a list of dictionaries.
        'movies': list(movies.values())
    }
    
    #Finally we return our data dictionary as JSON object.
    return JsonResponse(data, status=200)
```

2) Now , let's see what it would look like with returning only a single movie of our choice:
```
def movie_detail(request, movie_id):
    # Filter the movie by movie id
    movie = Movie.objects.get(pk=movie_id)

    # Convert the movie object into a dictionary from queryset format
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    
    #Return our data dictionary as JSON object.
    return JsonResponse(data, status=200)
```

So, as you can see, most of our work is to transform the queryset we receive from Django ORM to a JSON object that the user will receive ! What if there was an easier way to do this ? There is... that's why we will use DRF instead.

# DRF Introduction

Let's implement DRF into our project.

1) Start by installing it : ```pip install djangorestframework```.
2) Add ```rest_framework``` to your ```INSTALLED_APPS``` in ```settings.py```.

2 important concepts to keep about DRF:
- Serialization
- Deserialization

> Serialization is the process through which we transfor complex data types (like Model Objects) into Python Native DataType ( like dictionary) and then into JSON. Basically is an easier way of converting QuerySets , like I showed above, into JSON that we can send to the client.


> Deserialization is just the opposite. Getting information from the user and then transforming into complex data type like Model Objects.

# Serializers - GET Request

Let's rewrite the views that we have wrote in the previous chapter with Vanilla Django, but this time using serializers.

There are a couple of different types of serializers , but we will start using the most basic : ```serializers.Serializer```.

On a file called ```serializers.py```, we will add :

```
from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    active = serializers.BooleanField()
```

Now that we have a serializer and we can automatically convert our Model's complex data type into JSON. Let's see how our views will change:

```
from watchlist.models import Movie
from watchlist.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view # <- This is the decorator that we need to use in function based views, it takes a list of acceptable methods for that view.

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
```

# Serializers - POST Request

If we receive a POST request, our serializers needs to handle those methods by  implementing the function "create(validated_data)".

We also need to add the acceptable method to our ```@api_view()``` list.

So , if we what we are dealing with , is a POST request, we would have to make the following changes to the serializer:

```
from rest_framework import serializers
from watchlist.models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """Create a new movie"""
        return Movie.objects.create(**validated_data)
```

And we also would have to change the view logic to something like this :

```
from watchlist.models import Movie
from watchlist.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

# Serializers - PUT Request

If it is a PUT request, we need to do the same thing.

First of all, add the PUT request to our list of aceptable methods in out ```@api_view()``` .

Second , we need to add the "update(instance, validated_data)" method to our ```MovieSerializer```.

This is our modified serializer :
```
from rest_framework import serializers
from watchlist.models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """Create a new movie"""
        return Movie.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        # instance carries the old values
        # validated_data carries the new values
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
```

And this is our modified view :

```
@api_view(['GET', 'PUT'])
def movie_detail(request, movie_id):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

# Serializers - DELETE Request

To handle the DELETE method, take a look at the changes.

No changes required in the serializer, only change the view to :

```
@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_id):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```
