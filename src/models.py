from flask import Flask

from datetime import timedelta
import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from config import UPLOAD_FOLDER



app = Flask(__name__,template_folder="./templates",static_folder='./static')
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
# Initialiser la base de données SQLAlchemy
migrate = Migrate(app, db)

# Créer une instance de SQLAlchemy
# db = SQLAlchemy()

# CREATIONS DES MODELES

#Categorie Model 
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)

#Produit model
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    qteStock = db.Column(db.Integer, nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    categorie = db.relationship('Categorie', backref=db.backref('produits', lazy=True))
    # produit = db.relationship("Facture", backref="produit")
    factures = db.relationship("DetailsFacture", backref="produit")

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(250), nullable=False)
    

class TypeAbonnement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomTypeAbonnement = db.Column(db.String(250), nullable=False)
    taux_reduction = db.Column(db.Float, nullable=True)
    nombre_coiffures_incluses = db.Column(db.Integer, nullable=False)
    nombre_coiffures_restantes = db.Column(db.Integer, nullable=False)
    coiffure_id = db.Column(db.Integer, db.ForeignKey('coiffure.id'))
    coiffure = db.relationship('Coiffure', back_populates='abonnements')


class Coiffure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    abonnements = db.relationship('TypeAbonnement', back_populates='coiffure')
    factures = db.relationship("DetailsFacture", backref="coiffure")


class Abonnement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    type_abonnement_id = db.Column(db.Integer, db.ForeignKey('type_abonnement.id'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    is_paye = db.Column(db.Boolean, default=False)
    is_valide = db.Column(db.Boolean, default=True)
    montant = db.Column(db.Float, nullable=False) 
    client = db.relationship('Client', backref='abonnements')
    type_abonnement = db.relationship('TypeAbonnement', backref='abonnements')

    def __init__(self, client_id, type_abonnement_id):
        self.client_id = client_id
        self.type_abonnement_id = type_abonnement_id
        self.date_debut = datetime.datetime.now()
        self.date_fin = self.calculer_date_fin()  
        self.montant = self.calculer_montant() 
        
    def calculer_montant(self):
        # Cette methode sert le montant en fonction du prix unitaire, du nombre de coiffures incluses
        # et du taux de réduction
        type_abonnement = TypeAbonnement.query.get(self.type_abonnement_id)
        if type_abonnement:
            prix_unitaire = type_abonnement.coiffure.prix
            nombre_coiffures_incluses = type_abonnement.nombre_coiffures_incluses
            taux_reduction = type_abonnement.taux_reduction / 100  # Convertir le pourcentage en décimal
            montant_total = (prix_unitaire * nombre_coiffures_incluses) * (1 - taux_reduction)
            return montant_total

    def calculer_date_fin(self): # calculer la date de fin qui est dans 30 jours de la date de creation 
        return self.date_debut + timedelta(days=30)

    
# # Pour le cassier 

# Model détails de facture
class DetailsFacture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=True)
    coiffure_id = db.Column(db.Integer, db.ForeignKey('coiffure.id'), nullable=True)
    quantite_produit = db.Column(db.Integer, nullable=True)
    quantite_coiffure = db.Column(db.Integer, nullable=True)

# Model facture
class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    montant_total = db.Column(db.Float, nullable=False)
    montant_paye = db.Column(db.Float, nullable=False)
    montant_rendu = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", backref="factures")
    client = db.relationship("Client", backref="factures")
    details = db.relationship("DetailsFacture", backref="facture")



class Caisse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    montant_total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class PaiementAbo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnement.id'), nullable=False)
    montant_paye = db.Column(db.Float, nullable=False)
    montant_rendu = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    user = db.relationship("User", backref="paiement")
    abonnement = db.relationship('Abonnement', backref='paiements')

#Admin
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(250), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))


class Approvisionnement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    produit = db.relationship('Produit', backref=db.backref('approvisionnements', lazy=True))
    qte_actuelle = db.Column(db.Integer, nullable=False)
    qte_ajoutee = db.Column(db.Integer, nullable=False)
    date_heure = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('approvisionnements', lazy=True))

    
    
# ============= LES FONCTIONS POUR LA TABLE PRODUIT ============= 

    def getAll():
        return Produit.query.order_by(Produit.nom).all()

    
    def save(produit):
        db.session.add(produit)
        db.session.commit()

    def update(produit):
        db.session.commit()

    
    def delete(produit):
        db.session.delete(produit)
        db.session.commit()

 
    def findById(id):
        return Produit.query.get(id)
    

# ============= LES FONCTIONS POUR LA TABLE Categorie  =============  
    
    @staticmethod
    def save_all(categories):
        db.session.add_all(categories)
        db.session.commit()
    


# ============= LES FONCTIONS POUR LA TABLE CLIENT =============  

    def getAll():
        return Client.query.order_by(Client.nom).all()

    
    def saveClient(client):
        db.session.add(client)
        db.session.commit()

    def updateClient(client):
        db.session.commit()

    
    def delete(client):
        db.session.delete(client)
        db.session.commit()

 
    def findById(id):
        return Client.query.get(id)

# ============= LES FONCTIONS POUR LA TABLE ABONNEMENT  =============    
    def getAll():
        return Abonnement.query.order_by(Abonnement.id).all()

    def save(abo):
        db.session.add(abo)
        db.session.commit()

    def update(abo):
        db.session.commit()

    
    def delete(abo):
        db.session.delete(abo)
        db.session.commit()

 
    def findById(id):
        return Abonnement.query.get(id)

# ============= LES FONCTIONS POUR LA TABLE TYPE ABONNEMENT ============= 
        
    def getAll():
        return TypeAbonnement.query.order_by(TypeAbonnement.nom).all()

    
    def save(typeAbo):
        db.session.add(typeAbo)
        db.session.commit()

    def update(typeAbo):
        db.session.commit()

    
    def delete(typeAbo):
        db.session.delete(typeAbo)
        db.session.commit()

 
    def findById(id):
        return TypeAbonnement.query.get(id)

# ============= LES FONCTIONS POUR LA TABLE COIFFURE  ============= 
    def getAll():
        return Coiffure.query.order_by(Coiffure.nom).all()

    
    def saveCoiffure(coiffure):
        db.session.add(coiffure)
        db.session.commit()

    def updateCoiffure(coiffure):
        db.session.commit()

    
    def delete(coiffure):
        db.session.delete(coiffure)
        db.session.commit()

 
    def findById(id):
        return Coiffure.query.get(id)

# ============= LES FONCTIONS POUR LA TABLE FACTURE  ============= 
    def getAll():
        return Facture.query.order_by(Facture.date).all()

    
    def save(facture):
        db.session.add(facture)
        db.session.commit()

    def update(facture):
        db.session.commit()

    
    def delete(facture):
        db.session.delete(facture)
        db.session.commit()

 
    def findById(id):
        return Facture.query.get(id)
    
# ============= LES FONCTIONS POUR LA TABLE USER  ============= 
    def getAll():
        return User.query.order_by(User.nom).all()
    
    def save(user):
        db.session.add(user)
        db.session.commit()

    def update(user):
        db.session.commit()

    
    def delete(user):
        db.session.delete(user)
        db.session.commit()

 
    def findById(id):
        return User.query.get(id)