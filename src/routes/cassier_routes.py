from flask import Blueprint,render_template

cassier = Blueprint('cassier', __name__)

@cassier.route('/home')
def home():
    return render_template('layouts/base.connexion.html')

@cassier.route('/facture')
def Facture():
    return render_template('cassier/ListFacture.html')

@cassier.route('/facture')
def AddFacture():
    return render_template('cassier/facture/AddFacture.html')
   