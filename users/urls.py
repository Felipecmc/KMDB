from django.urls import path
from . import views

urlpatterns = [
    path("users/login/", views.LoginUserView.as_view()),
    path("users/register/", views.UserRegistration.as_view()),
    path("users/", views.UserListView.as_view()),
    path("users/<int:user_id>/", views.UserDetailView.as_view())
]