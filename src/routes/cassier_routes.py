from flask import Blueprint,render_template

cassier = Blueprint('cassier', __name__)

@cassier.route('/home')
def home():
    return render_template('layouts/base.connexion.html')
    #return "<h1>Test de l'application pour le cassier</h1>"