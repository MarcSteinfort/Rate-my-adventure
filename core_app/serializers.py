from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

from .models import Game, Review
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, clean_data):
        user_obj = User.objects.create_user(email = clean_data['email'], username = clean_data['username'], password=clean_data['password'])
        user_obj.save()
        
        return user_obj

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    print('serializer run')
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        
        return token
    

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title', 'description', 'final_rating', 'image', 'id')

         

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    class Meta:
        model = Review
        fields = ('review', 'user', 'rating')