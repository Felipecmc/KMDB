from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from movies.models import Movie
from movies.serializers import MovieSerializer
from users.models import User

class MoviesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request:Request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        
        if not movies:
            return Response({"detail": "No movies found"}, status=404)
        
        return Response(serializer.data, status=200)
    
    def post(self, request:Request):

        user_token_id = Token.objects.get(key= request.auth).user_id
        user = User.objects.get(id = user_token_id)
        
        if not user.is_superuser:
            return Response({"detail": "User not authorized to create movies"}, status=403)
        else:
            serializer = MovieSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            serializer.save()
            
            return Response(serializer.data, status.HTTP_201_CREATED)


class MoviesDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request:Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        
        return Response(serializer.data, status.HTTP_200_OK)
    def delete(self, request:Request, movie_id):
        user_token_id = Token.objects.get(key= request.auth).user_id
        user = User.objects.get(id = user_token_id)
        
        if not user.is_superuser:
            return Response({"detail": "User not authorized to delete movies"}, status=403)
        
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        
        return Response(status.HTTP_204_NO_CONTENT)
    
    def patch(self, request:Request, movie_id):
        user_token_id = Token.objects.get(key= request.auth).user_id
        user = User.objects.get(id = user_token_id)
        
        if not user.is_superuser:
            return Response({"detail": "User not authorized to update movies"}, status=403)
        
        
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception= True)
        
        serializer.save()
        return Response(serializer.data)
        

