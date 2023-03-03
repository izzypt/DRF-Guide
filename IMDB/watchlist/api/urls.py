from django.db import models
from django.urls import path, include
from watchlist.api.views import movie_list, movie_detail


urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
]

