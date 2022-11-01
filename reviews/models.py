from django.db import models

class Recomendation(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    NO_OPINION = "No Opinion"
    
class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    recomendation = models.CharField(max_length=50, choices = Recomendation.choices, default = Recomendation.NO_OPINION )
    movie = models.ForeignKey("movies.Movie", related_name="reviews", on_delete=models.CASCADE)
    critic = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)