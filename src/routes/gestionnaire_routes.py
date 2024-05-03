from flask import render_template, request, redirect, url_for,flash
from ..models import  Produit,Categorie,Client,Abonnement,TypeAbonnement,Coiffure,db
from  ..forms.ArticleForms import AddArticleForm,AddCategorieForm
from ..forms.ClientForms import AddClientForm
from ..forms.CoiffureForms import AddCoiffureForm
from ..forms.TypeAbonnementForms import AddTypeAbonnementForm
from ..forms.AbonnementForms import AddAbonnementForm
from ..fileManager import save_uploaded_file
from flask_weasyprint import HTML,CSS  
from flask import send_file
from ..models import app
from .Security import gestionnaire_required
from .auth_routes import login_required
import os


# gestionnaire = Blueprint('gestionnaire', __name__)


@app.route('/ListerArticle')
@login_required
# @gestionnaire_required
def ListerArticle():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    produits = Produit.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/article/ListerArticle.html', produits=produits)

#======== Categorie ============
@app.route('/Article/Categorie/List',methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def ListerCategorie():
    form = AddCategorieForm()
    page = request.args.get('page', 1, type=int)
    categories = Categorie.query.paginate(page=page, per_page=7)
    if form.validate_on_submit():
        categorie = Categorie(nom=form.nom.data)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for('ListerCategorie'))
    return render_template('gestionnaire/article/ListerCategorie.html', form=form, categories=categories)

#======== Produit ============

@app.route('/Article/Add', methods=['GET','POST'])
@login_required
# @gestionnaire_required
def AddArticle():
    form = AddArticleForm()
    form.categorie.choices = [(cat.id, cat.nom) for cat in Categorie.query.all()]
    if form.validate_on_submit():
        filename = save_uploaded_file(form.photo.data)
        produit = Produit(
            nom=form.nom.data,
            prix=form.prix.data,
            qteStock=form.qte_stock.data,
            categorie_id=form.categorie.data,  
            photo=filename,
            description=form.description.data
        )
        db.session.add(produit)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('gestionnaire/article/AjouterArticle.html',form=form)


#======== coiffure ============ 

@app.route('/Client/List')
@login_required
# @gestionnaire_required
def ListClient():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    clients = Client.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/client/ListClient.html', clients=clients)


@app.route('/Client/Add',methods=['GET','POST'])
@login_required
# @gestionnaire_required
def AddClient():
    form = AddClientForm()
    if form.validate_on_submit():
        client = Client(
                nom=form.nom.data,
                prenom=form.prenom.data,
                telephone=form.telephone.data,
                adresse=form.adresse.data,
            )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('ListClient'))
    return render_template('gestionnaire/client/AddClient.html',form=form)


#======== coiffure ============

@app.route('/Coiffure/List')
@login_required
# @gestionnaire_required
def ListCoiffure():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    coiffures = Coiffure.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/coiffure/ListCoiffure.html', coiffures=coiffures)


@app.route('/Coiffure/Add',methods=['GET','POST'])
@login_required
# @gestionnaire_required
def AddCoiffure():
    form = AddCoiffureForm()
    if form.validate_on_submit():
        coiffure = Coiffure(
                nom=form.nom.data,
                prix=form.prix.data,
            )
        db.session.add(coiffure)
        db.session.commit()
        return redirect(url_for('ListCoiffure'))
    return render_template('gestionnaire/coiffure/AddCoiffure.html',form=form)


#=== Abonnement =======

@app.route('/Abonnement/Type/List')
@login_required
# @gestionnaire_required
def ListTypeAbonnement():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    abonnements = TypeAbonnement.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/typeAbonnement/ListTypeAbonnement.html', abonnements=abonnements)


@app.route('/Abonnement/Type/Add', methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def AddTypeAbonnement():
    form = AddTypeAbonnementForm()
    form.coiffure_id.choices = [(coiffure.id, coiffure.nom) for coiffure in Coiffure.query.all()]
    if form.validate_on_submit():
        abonnement = TypeAbonnement(
            nomTypeAbonnement=form.nom.data,
            taux_reduction=form.taux_reduction.data,
            nombre_coiffures_incluses=form.nombre_coiffures_incluses.data,
            nombre_coiffures_restantes=form.nombre_coiffures_incluses.data,
            coiffure_id=form.coiffure_id.data
        )
        db.session.add(abonnement)
        db.session.commit()
        return redirect(url_for('ListTypeAbonnement'))
    return render_template('gestionnaire/typeAbonnement/AddTypeAbonnement.html', form=form)



#======== Abonnement ============

@app.route('/Abonnement/List')
@login_required
# @gestionnaire_required
def ListAbonnement():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    abonnements = Abonnement.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/abonnement/ListAbonnement.html', abonnements=abonnements)


@app.route('/Abonnement/Add', methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def AddAbonnement():
    form = AddAbonnementForm()
    if form.validate_on_submit():
        abonnement = Abonnement(
            client_id=form.client_id.data,
            type_abonnement_id=form.type_abonnement_id.data
        )
        db.session.add(abonnement)
        db.session.commit()
        return redirect(url_for('ListAbonnement'))
    return render_template('gestionnaire/abonnement/AddAbonnement.html', form=form)

# Details Abonnements 

@app.route('/Abonnement/details/<int:id>', methods=['GET'])
@login_required
# @gestionnaire_required
def DetailAbonnement(id):
    abonnement = Abonnement.query.get_or_404(id)
    return render_template('gestionnaire/abonnement/DetailAbonnement.html', abonnement=abonnement)



#__________________________



@app.route('/Abonnement/details/<int:id>/print', methods=['GET'])
@login_required
# @gestionnaire_required
def print_abonnement(id):
    abonnement = Abonnement.query.get_or_404(id)
    rendered_template = render_template('gestionnaire/abonnement/carte.html', abonnement=abonnement)
    # Générer le PDF à partir du modèle HTML en spécifiant la taille et l'orientation de la page 
    pdf_bytes = HTML(string=rendered_template).write_pdf(
        stylesheets=[CSS(string='@page { size: A3 ; }')]
    )
    # Chemin relatif pour enregistrer le PDF 
    pdf_path = os.path.join(os.getcwd(), "output.pdf")

    # Enregistrer le PDF 
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    # Envoyer le fichier PDF en réponse à la requête 
    # avec as_attachment a true ,il telecharge directement le fichier si a false 
    # le fichier est d'abord visionner par le navigateur et on peut l'imprimer ou l'enregistrer en pdf 
    return send_file(pdf_path, as_attachment=False) 







