from django.contrib.auth.models import User

from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer, GameSerializer, ReviewSerializer
from .validations import custom_validation
from .models import Game, Review


import json

# Create your views here.
# AUTHENTICATION
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(APIView):
    def post(self, request):
        print('data', request.data)
        clean_data = custom_validation(request.data)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(clean_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# USER DETAILS
class UserDetails(APIView):
     def post(self, request):
        data = json.load(request)

        if(not data or not data['user']): return Response({"error": "No data subitted"}, status= status.HTTP_404_NOT_FOUND)
        print(data)
        username = data['user']['username']
        user = User.objects.filter(user__username = username)

        if user[0].paid:
            return Response({'successMsg': 'Payment completed'},status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Please complete payment.'}, status=status.HTTP_403_FORBIDDEN)
        


class Games(APIView):
    def get(self, request):
        try:
            games_queryset = Game.objects.all()
            games = GameSerializer(games_queryset, many=True).data
        except:
            return Response({'errorMsg': 'Error happened while fetching games.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'data': games}, status=status.HTTP_200_OK)


class GameDetail(APIView):
    def get(self, request, pk):
        try: 
            game_queryset = Game.objects.filter(id = pk)
            if( not game_queryset): return Response({'errorMsg': 'Game not found in our database!'}, status=status.HTTP_404_NOT_FOUND)
            
            game = GameSerializer(game_queryset, many=True).data
            reviews_queryset = Review.objects.filter(game__id = pk).order_by('-datetime')
            reviews = ReviewSerializer(reviews_queryset, many=True).data

        except:
            return Response({'errorMsg': 'Error happened while fetching games.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'data': {"games": game, "reviews": reviews}}, status=status.HTTP_200_OK)


class CreateGameView(APIView):
    def post(self, request):
        data = json.loads(request.POST.get('post_data'))
        image = request.FILES.get('image')
        
        if(not data): return Response({"errorMsg": "No data submitted"}, status= status.HTTP_404_NOT_FOUND)
       

        username = data.get('user')
        title = data.get('title')
        description = data.get('description')
        

        if(not username): return Response({"errorMsg": "Not authenticated"}, status= status.HTTP_403_FORBIDDEN)

        user = User.objects.get(username = username)
        
        if(not user): return Response({"errorMsg": "Not authenticated"}, status= status.HTTP_403_FORBIDDEN)

        game = Game.objects.create(title = title, description = description, image = image)

        

        return Response({'data':game.pk}, status=status.HTTP_200_OK)
    

class CreateCommentView(APIView):
    def post(self, request):
        data = json.load(request)
        if(not data): return Response({"errorMsg": "No data submitted"}, status= status.HTTP_404_NOT_FOUND)
        username = data['user']
        game_id = data['game_id']
        try:
            comment = data['comment']
            comment_rating = data['rating']
        except KeyError:
            return Response({"errorMsg": "No review submitted"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

        if(not username): return Response({"errorMsg": "Not authenticated"}, status= status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username = username)
        game = Game.objects.get(id = game_id)

        rating = game.rating + comment_rating
        rated_by = game.rated_by + 1

        new_final_rating_rating = rating / rated_by
        
        
        game.rating = rating
        game.rated_by = rated_by
        game.final_rating = new_final_rating_rating
        game.save()

        if(not user): return Response({"errorMsg": "Not authenticated"}, status= status.HTTP_403_FORBIDDEN)
        if(not game):  return Response({"errorMsg": "Game not found"}, status= status.HTTP_404_NOT_FOUND)

        Review.objects.create(user = user, game = game, review = comment, rating = comment_rating)

        return Response({"gameFinalRating": new_final_rating_rating}, status=status.HTTP_200_OK)


