from django.db import models
from django.urls import path, include
from watchlist.api.views import WatchListView, WatchListViewDetail, StreamPlatormView


urlpatterns = [
    path('list/', WatchListView.as_view(), name='movie_list'),
    path('<int:movie_id>/', WatchListViewDetail.as_view(), name='movie_detail'),
    path('stream/', StreamPlatormView.as_view(), name='stream_platform'),
]

