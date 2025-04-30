from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('categories/', views.categories, name='categories'),
    path('quizz/<slug:slug>/', views.quizz, name='quizz'),  # Index est optionnel ici
    path('quizz/<slug:slug>/<int:index>/', views.quizz, name='quizz_index'),
    path('quizz/<slug:slug>/fin/', views.quizz_fin, name='quizz_fin'),
]
