from django.shortcuts import render, redirect
from django.urls import reverse
import json
import os
from django.conf import settings

# 🔁 Fonction pour charger les données du fichier JSON contenant les quizz
# 📦 Fonction pour charger les données du fichier JSON contenant les questions de quizz
def charger_quizz():
    # 🗂️ Création du chemin absolu vers le fichier 'quizz_data.json' situé dans quizz/data/
    #settings.BASE_DIR : c'est la racine du projet Django (par exemple, là où se trouve manage.py).
    #os.path.join(...) : permet de créer un chemin correct vers un fichier, quel que soit le système d’exploitation (Windows, Linux, etc.).
    chemin = os.path.join(settings.BASE_DIR, 'quizz', 'data', 'quizz_data.json')
    
    # 📖 Ouverture du fichier JSON en mode lecture ('r'), avec encodage UTF-8 pour bien gérer les caractères spéciaux
    with open(chemin, 'r', encoding='utf-8') as fichier:
        # 🔄 Chargement du contenu du fichier JSON et conversion en dictionnaire Python
        return json.load(fichier)


# 🏠 Page d’accueil
def accueil(request):
    return render(request, "quizz/accueil.html")


# 📚 Vue pour afficher la page des catégories de quizz
def categories(request):
    # 🔄 Chargement des données du fichier JSON contenant les quizz
    QUIZZ = charger_quizz()
    
    # 🧾 Création d'une liste de catégories à partir des clés du dictionnaire JSON
    # Chaque élément contient :
    #   - "nom" : le nom lisible de la catégorie (ex. : "Prière")
    #   - "slug" : la clé utilisée dans l'URL (ex. : "priere")
    liste_categories = [
        {"nom": QUIZZ[key]["nom"], "slug": key}
        for key in QUIZZ.keys()
    ]
    
    # 🖥️ Envoi des catégories vers le template 'categories.html' pour affichage
    return render(request, "quizz/categories.html", {"categories": liste_categories})


# ❓ Vue pour afficher une question du quizz (1 question à la fois)
def quizz(request, slug, index=0, score=0, total=0):
    # 🔄 Chargement des données du fichier JSON contenant les quizz
    QUIZZ = charger_quizz()
    categorie = QUIZZ.get(slug)

    # Vérification que la catégorie existe
    if not categorie:
        return redirect('categories')

    questions = categorie["questions"]
    categorie["slug"] = slug  # On garde le slug pour les liens et l’image

    # Si on a atteint la fin du quizz → redirection vers la page de fin
    if index >= len(questions):
        return redirect(reverse('quizz_fin', args=[slug, score, total]))

    question = questions[index]  # Récupère la question actuelle
    reponse_donnee = None
    est_correct = None
    bonne_reponse = question["bonne_reponse"]

    # ⚡ Si le formulaire est soumis (POST)
    if request.method == "POST":
        reponse_donnee = request.POST.get("reponse")
        est_correct = (reponse_donnee == bonne_reponse)  # Vérifie si la réponse est correcte
        if est_correct:
            score += 1
        total += 1

        # Affiche la page avec la correction (pas de redirection immédiate)
        return render(request, "quizz/quizz.html", {
            "categorie": categorie,
            "question": question,
            "reponse_donnee": reponse_donnee,
            "est_correct": est_correct,
            "bonne_reponse": bonne_reponse,
            "index": index,
            "score": score,
            "total": total
        })

    # 🖼️ Si GET : on affiche la question sans correction
    return render(request, "quizz/quizz.html", {
        "categorie": categorie,
        "question": question,
        "reponse_donnee": None,
        "est_correct": None,
        "bonne_reponse": bonne_reponse,
        "index": index,
        "score": score,
        "total": total
    })


# ⏭️ Fonction pour passer à la question suivante
def quizz_suivant(request, slug):
    QUIZZ = charger_quizz()

    # Vérifie que le slug de catégorie est bien valide
    if slug not in QUIZZ:
        return redirect('categories')

    # On augmente l'index de la question actuelle dans la session
    request.session['index'] = request.session.get('index', 0) + 1

    # Redirige vers la prochaine question
    return redirect(reverse('quizz', args=[slug]))


# ✅ Page de fin du quizz avec le message personnalisé selon le score
def quizz_fin(request, slug, score, total):
    QUIZZ = charger_quizz()
    categorie = QUIZZ.get(slug)

    # Si la catégorie n'existe pas, on retourne aux catégories
    if not categorie:
        return redirect('categories')

    # On réinitialise le score pour permettre un nouveau quizz propre
    request.session["score"] = 0
    request.session["total"] = 0

    # 📝 Message final en fonction de la performance du joueur
    if total == 0:
        message = "Aucune question répondue."
    else:
        ratio = score / total
        if ratio == 1:
            message = "🌟 Excellent ! Tu as tout juste !"
        elif ratio >= 0.8:
            message = "👍 Très bon travail !"
        elif ratio >= 0.5:
            message = "🙂 Pas mal, mais tu peux encore progresser."
        else:
            message = "💡 Courage ! Il faut encore réviser un peu."

    # Affiche la page de fin avec les résultats et le message
    return render(request, "quizz/fin.html", {
        "categorie": categorie,
        "score": score,
        "total": total,
        "message": message
    })
