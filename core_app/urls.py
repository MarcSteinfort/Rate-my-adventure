from django.urls import path

from . import views

urlpatterns = [
    # authentication
    path('register/', views.UserRegister.as_view(), name = 'register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name = 'register'),
    path('user/', views.UserDetails.as_view(), name = 'user'),

    # games
    path('games/', views.Games.as_view(), name = 'games'),
    path('game-details/<int:pk>/', views.GameDetail.as_view(), name = 'game-detail'),
    path('create-game/', views.CreateGameView.as_view(), name = 'create-game'),
    path('create-comment/', views.CreateCommentView.as_view(), name = 'create-comment'),

]