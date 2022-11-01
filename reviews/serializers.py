from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserSerializer


class CriticSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)
    class Meta:
        model = Review
        fields =["id", "stars", "review", "spoilers", "recomendation", "movie_id", "critic"]
    # id = serializers.IntegerField(read_only=True)
    # stars = serializers.IntegerField()
    # review = serializers.CharField(validators=[UniqueValidator(queryset=Review.objects.all())])
    # spoilers = serializers.BooleanField()
    # recomendation = serializers.CharField(required=False)
    # critic = UserSerializer()
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop('critic')
    #     user_obj= User.objects.get(user_data)
    #     review = Review.objects.create(**validated_data)
    #     # review.critic = (user_obj) 
    #     # review.save()
    #     return review