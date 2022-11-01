from rest_framework import serializers
from genres.models import Genre

from genres.serializers import GenreSerializer
from .models import Movie
from rest_framework.validators import UniqueValidator

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(validators=[UniqueValidator(queryset=Movie.objects.all())])
    duration = serializers.CharField()
    premiere = serializers.DateTimeField()
    classification = serializers.IntegerField() 
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)
    
    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre in genres_data:
            genre_obj, _ = Genre.objects.get_or_create(**genre)
            movie.genres.add(genre_obj)
            
        return movie
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'genres':
                for genre in value:
                    genre_obj, _ = Genre.objects.get_or_create(**genre)
                    instance.genres.add(genre_obj)
            else:
                setattr(instance, key, value)
            
        instance.save()
        
        return instance
    