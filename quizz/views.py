from django.shortcuts import render, redirect
from django.urls import reverse
import json
import os
from django.conf import settings


# Create your views here.
# view pour categorie

# Charger les données du fichier JSON
def charger_quizz():
    chemin = os.path.join(settings.BASE_DIR, 'quizz', 'data', 'quizz_data.json')
    with open(chemin, 'r', encoding='utf-8') as fichier:
        return json.load(fichier)

def categories(request):
    categories = [
        {"nom": "Prière", "slug": "priere"},
        {"nom": "Ramadan", "slug": "ramadan"},
        {"nom": "Prophètes", "slug": "prophetes"},
        {"nom": "Coran", "slug": "coran"},
        {"nom": "Comportement", "slug": "comportement"},
    ]
    return render(request, 'quizz/categories.html', {"categories": categories})



# Page d’accueil
def accueil(request):
    return render(request, "quizz/accueil.html")


# Page des catégories
def categories(request):
    QUIZZ = charger_quizz()
    liste_categories = [
        {"nom": QUIZZ[key]["nom"], "slug": key}
        for key in QUIZZ.keys()
    ]
    return render(request, "quizz/categories.html", {"categories": liste_categories})


# Page d'un quizz (1 question à la fois)
def quizz(request, slug, index=0):
    QUIZZ = charger_quizz()

    categorie = QUIZZ.get(slug)
    if not categorie:
        return redirect('categories')

    # Ajouter le slug manuellement à l'objet
    categorie["slug"] = slug

    questions = categorie["questions"]

    if index >= len(questions):
        return redirect(reverse('quizz_fin', args=[slug]))

    question = questions[index]
    reponse_donnee = None
    est_correct = None
    bonne_reponse = None

    if request.method == "POST":
        reponse_donnee = request.POST.get("reponse")
        bonne_reponse = question["bonne_reponse"]
        est_correct = (reponse_donnee == bonne_reponse)

    return render(request, "quizz/quizz.html", {
        "categorie": categorie,
        "question": question,
        "reponse_donnee": reponse_donnee,
        "est_correct": est_correct,
        "bonne_reponse": bonne_reponse,
        "index": index,
    })

# Pour passer à la question suivante
def quizz_suivant(request, slug):
    # Vérifie si le slug est valide avant de continuer
    QUIZZ = charger_quizz()
    if slug not in QUIZZ:
        return redirect('categories')  # Redirige vers les catégories si le slug est invalide

    request.session['index'] = request.session.get('index', 0) + 1
    return redirect(reverse('quizz', args=[slug]))

def quizz_fin(request, slug):
    QUIZZ = charger_quizz()
    categorie = QUIZZ.get(slug)
    if not categorie:
        return redirect('categories')

    return render(request, "quizz/fin.html", {"categorie": categorie})
