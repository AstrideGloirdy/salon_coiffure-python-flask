# fixtures.py

from faker import Faker
import random

from .models import Categorie, Produit, db

fake = Faker()


# def generate_fake_categories():
#     categories = []
#     for i in range(1, 7):  # Générer 6 catégories
#         categorie = Categorie(nom=f"Categorie {i}")
#         categories.append(categorie)
#     return categories

def generate_fake_categories():
    categories = []
    for i in range(1, 4):  # Générer 10 catégories
        # Utilisez le modulo (%) pour obtenir un nom de catégorie différent
        categorie_name = f"Categorie {i}"
        categorie = Categorie(nom=categorie_name)
        categories.append(categorie)
    return categories

def generate_fake_produits():
    categories = Categorie.query.all()
    produits = []
    for i in range(1, 3):  # Générer 15 produits
        # Utilisez le modulo (%) pour obtenir une catégorie différente pour chaque produit
        categorie_index = (i - 1) % len(categories)
        produit = Produit(nom=f"Produit {i}",
                          photo=fake.image_url(),
                          description=fake.text(),
                          prix=round(random.uniform(500, 5000), 0),  # Prix arrondi à deux décimales
                          qteStock=random.randint(1, 100),  # Quantité de 1 à 100
                          categorie=categories[categorie_index])
        produits.append(produit)
    return produits

