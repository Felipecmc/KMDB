
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from movies.models import Movie
from reviews.models import Review
import ipdb
from reviews.serializers import ReviewSerializer
from users.models import User
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer

class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request:Request, movie_id):
        review = Review.objects.filter(movie_id =movie_id)
        serializer = ReviewSerializer(review, many=True)
        
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request:Request, movie_id):
        user = request.user
        movie = get_object_or_404(Movie, id=movie_id)
        review_already_exists = Review.objects.filter(movie=movie, critic = user).exists()
        if not user.is_superuser and user.is_critic == False:
            return Response({"detail": "User not authorized to review movies"}, status=403)
        if review_already_exists:
            return Response({"detail": "User already have a review to that movie"}, status=403)
        
        serializer = ReviewSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(critic=user, movie_id= movie_id)
              
        return Response(serializer.data, status.HTTP_201_CREATED)
        

class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request:Request, movie_id, review_id):
        review =get_object_or_404(Review, id= review_id, movie_id = movie_id)
        serializer = ReviewSerializer(review)
        
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request:Request, movie_id, review_id):
        user_token_id = Token.objects.get(key= request.auth).user_id
        user = User.objects.get(id = user_token_id)
        review = get_object_or_404(Review, id= review_id, movie_id = movie_id)
        if user.is_superuser or user.id == review.critic_id:
            review.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": "User not authorized to delete this movie!"}, status.HTTP_401_UNAUTHORIZED)
        
       
        