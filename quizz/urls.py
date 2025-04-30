# 📦 Import des fonctions nécessaires depuis Django
from django.urls import path

# 📥 Import des vues définies dans le fichier views.py du même module
from . import views

# 🧭 Définition des URLs disponibles pour l'application 'quizz'
urlpatterns = [
    # 🏠 Page d’accueil du quizz
    path('', views.accueil, name='accueil'),

    # 📚 Page listant toutes les catégories disponibles
    path('categories/', views.categories, name='categories'),

    # ❓ Affichage d'une question du quizz (1ère question d'une catégorie)
    # Exemple : /quizz/priere/
    path('quizz/<slug:slug>/', views.quizz, name='quizz'),

    # 🔁 Affichage d'une question spécifique avec les paramètres d’état du quizz
    # - slug : identifiant de la catégorie (ex : priere)
    # - index : numéro de la question en cours
    # - score : score actuel du joueur
    # - total : nombre total de questions répondues
    # Exemple : /quizz/priere/2/1/2/
    path('quizz/<slug:slug>/<int:index>/<int:score>/<int:total>/', views.quizz, name='quizz'),

    # 🏁 Page finale du quizz avec score et message personnalisé
    # Exemple : /quizz_fin/priere/5/7/
    path('quizz_fin/<slug:slug>/<int:score>/<int:total>/', views.quizz_fin, name='quizz_fin'),
]
