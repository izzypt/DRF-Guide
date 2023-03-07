from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     # The next line will fetch all the movies from DB and store them in a queryset
#     movies = Movie.objects.all()
#     # Because we cannot send the response as a querset, we need to transform the queryset.
#     data = {
#         # Using .values() we get the values each object of the queryset as a dictionarie.
#         # And then wrapping the queryset in a list to transform it into a list of dictionaries.
#         'movies': list(movies.values())
#     }
#     print(data)
#     #Finally we return our data dictionary as JSON object.
#     return JsonResponse(data, status=200)

# def movie_detail(request, movie_id):
#     # Filter the movie by movie id
#     movie = Movie.objects.get(pk=movie_id)

#     # Convert the movie object into a dictionary from queryset format
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
    
#     #Return our data dictionary as JSON object.
#     return JsonResponse(data, status=200)
