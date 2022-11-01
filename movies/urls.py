from django.urls import path
from . import views
from reviews.views import ReviewView, ReviewDetailView

urlpatterns = [
    path('movies/', views.MoviesView.as_view()),
    path('movies/<int:movie_id>/', views.MoviesDetailView.as_view()),
    path('movies/<int:movie_id>/reviews/', ReviewView.as_view()),
    path('movies/<int:movie_id>/reviews/<int:review_id>/', ReviewDetailView.as_view())
]