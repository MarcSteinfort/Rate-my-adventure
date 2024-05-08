from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    image = models.ImageField(upload_to='games-thumbnail/')
    rated_by = models.IntegerField(default=0)
    final_rating = models.IntegerField(default=0)


    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f'Game:{self.game.title} User:{self.user.username} Rating: {self.rating}'