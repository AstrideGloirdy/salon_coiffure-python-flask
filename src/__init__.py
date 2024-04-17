from flask import Flask

from config import UPLOAD_FOLDER
from .routes.gestionnaire_routes import gestionnaire
from .routes.admin_routes import admin
from .routes.cassier_routes import cassier
from .Fixtures import generate_fake_categories, generate_fake_produits
from .models import db  # Assurez-vous que db est importé depuis models.py uniquement

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialiser la base de données
    db.init_app(app)

    # Créer toutes les tables dans la base de données
    with app.app_context():
        db.create_all()

        # Générer des données fictives
        generate_fake_data(app)

    # Enregistrer les Blueprints
    app.register_blueprint(gestionnaire, url_prefix='/gestionnaire')
    app.register_blueprint(cassier, url_prefix='/cassier')
    app.register_blueprint(admin, url_prefix='/admin')

    return app



def generate_fake_data(app):
    with app.app_context():
        categories = generate_fake_categories()
        db.session.add_all(categories)
        produits = generate_fake_produits()
        db.session.add_all(produits)
        db.session.commit()