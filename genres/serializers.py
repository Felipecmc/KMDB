from rest_framework import serializers
from .models import Genre
from rest_framework.validators import UniqueValidator

class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()