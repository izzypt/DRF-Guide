from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# class Movie(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=255)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

class StreamPlatorm(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
        
class WatchList(models.Model):
    title = models.CharField(max_length=150)
    platform = models.ForeignKey(StreamPlatorm, on_delete=models.CASCADE, related_name="watchlist")
    storyline = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    rating = models.PositiveBigIntegerField(MinValueValidator(1), MaxValueValidator(5))
    description = models.CharField(max_length=255)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.rating + " - " + self.watchlist.title