from django.urls import path
from . import views
import requests
from django.http import JsonResponse

urlpatterns = [
    path('chessBackend/', views.hello, name='hello'),
    path('stats/<str:username>/', views.get_chess_api, name='get_stats'),
    path('mostplayed/<str:username>/', views.get_openings_by_result, name='get_openings'),
    path('games/<str:username>/', views.get_month_games, name='get_games'),
]