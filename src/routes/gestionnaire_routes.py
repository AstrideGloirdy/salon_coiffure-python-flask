from datetime import datetime
from operator import or_
from flask import render_template, request, redirect, url_for,flash
from ..models import  Produit,Categorie,Client,Abonnement,TypeAbonnement,Coiffure,db
from  ..forms.ArticleForms import AddArticleForm,AddCategorieForm, EditArticleForm,SearchForm
from ..forms.ClientForms import AddClientForm,SearchForm
from ..forms.CoiffureForms import AddCoiffureForm, EditCoiffureForm,SearchForm
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

#======== Produit ============

@app.route('/ListerArticle',methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def ListerArticle():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    if form.validate_on_submit():
        search_query = form.search_query.data
        produits = Produit.query.filter(Produit.nom.ilike(f'%{search_query}%')).paginate(page=page, per_page=5)
    else:
        produits = Produit.query.paginate(page=page, per_page=5)

    return render_template('gestionnaire/article/ListerArticle.html', produits=produits,form=form)

@app.route('/Galerie',methods=['GET','POST'])
@login_required
def Galerie():
    produits = Produit.query.all()
    return render_template('gestionnaire/article/Galerie.html', produits=produits)

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
        return redirect(url_for('ListerArticle'))
    return render_template('gestionnaire/article/AjouterArticle.html',form=form)


@app.route('/Article/Edit/<int:produit_id>', methods=['GET', 'POST'])
@login_required
def EditArticle(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    form = EditArticleForm(obj=produit) # charger l'objet  correspondant
     # Charger les catégories disponibles dans le formulaire
    form.categorie.choices = [(categorie.id, categorie.nom) for categorie in Categorie.query.all()]
    if form.validate_on_submit():
        if form.nom.data != produit.nom or form.prix.data != produit.prix or form.categorie.data != produit.categorie_id:
            produit.nom = form.nom.data
            produit.prix = form.prix.data
            produit.qteStock = form.qte_stock.data
            produit.photo = form.photo.data
            produit.categorie_id = form.categorie.data
            db.session.commit()
            return redirect(url_for('ListerArticle'))
        else:
            
            flash('Aucune modification détectée.', 'info')
            return redirect(url_for('ListerArticle'))
        # Pré-sélectionner la catégorie actuelle de l'article dans le formulaire
    form.categorie.data = produit.categorie_id
    # Pré-remplir la quantité en stock actuelle du produit dans le formulaire
    form.qte_stock.data = produit.qteStock

    return render_template('gestionnaire/article/EditArticle.html', form=form, produit=produit)

@app.route('/Article/Delete/<int:produit_id>', methods=['GET','POST'])
@login_required
def DeleteArticle(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash('L\'article a été supprimé avec succès.', 'success')
    return redirect(url_for('ListerArticle'))

#======== Categorie ============
@app.route('/Article/Categorie/List',methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def ListerCategorie():
    form = AddCategorieForm()
    page = request.args.get('page', 1, type=int)
    categories = Categorie.query.paginate(page=page, per_page=5)
    if form.validate_on_submit():
        categorie = Categorie(nom=form.nom.data)
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for('ListerCategorie'))
    return render_template('gestionnaire/article/ListerCategorie.html', form=form, categories=categories)




#======== Client ============ 

@app.route('/Client/List',methods=['GET', 'POST'])
@login_required
# @gestionnaire_required
def ListClient():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    if form.validate_on_submit():
        search_query = form.search_query.data
        #clients = Client.query.filter(Client.nom.ilike(f'%{search_query}%')).paginate(page=page, per_page=5)
        clients = Client.query.filter(or_(Client.nom.ilike(f'%{search_query}%'), Client.prenom.ilike(f'%{search_query}%'))).paginate(page=page, per_page=5)
    else:
        clients = Client.query.paginate(page=page, per_page=5)
    return render_template('gestionnaire/client/ListClient.html', clients=clients,form=form)


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

@app.route('/Client/Edit/<int:client_id>', methods=['GET', 'POST'])
@login_required
def EditClient(client_id):
    client = Client.query.get_or_404(client_id)
    form = AddClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client) # pour faire la modification 
        db.session.commit()
        return redirect(url_for('ListClient'))

    return render_template('gestionnaire/client/EditClient.html', form=form, client=client)

@app.route('/Client/Delete/<int:client_id>', methods=['GET','POST'])
@login_required
def DeleteClient(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('ListClient'))

#======== coiffure ============

@app.route('/CoiffureList',methods=['GET','POST'])
@login_required
# @gestionnaire_required
def ListCoiffure():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    if form.validate_on_submit():
        search_query = form.search_query.data
        print("Mot recherché :", search_query)
        coiffures = Coiffure.query.filter(Coiffure.nom.ilike(f'%{search_query}%')).paginate(page=page, per_page=5)
    else:
        coiffures = Coiffure.query.paginate(page=page, per_page=5)

    return render_template('gestionnaire/coiffure/ListCoiffure.html', coiffures=coiffures, form=form)


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


@app.route('/Coiffure/Edit/<int:coiffure_id>', methods=['GET', 'POST'])
@login_required
def EditCoiffure(coiffure_id):
    coiffure = Coiffure.query.get_or_404(coiffure_id)
    form = EditCoiffureForm(obj=coiffure) # charger l'objet coiffure correspondant
    if form.validate_on_submit():
        form.populate_obj(coiffure)
        db.session.commit()
        return redirect(url_for('ListCoiffure'))    
    return render_template('gestionnaire/coiffure/EditCoiffure.html', form=form, coiffure=coiffure)

@app.route('/Coiffure/Delete/<int:coiffure_id>', methods=['GET','POST'])
@login_required
def DeleteCoiffure(coiffure_id):
    coiffure = Coiffure.query.get_or_404(coiffure_id)
    db.session.delete(coiffure)
    db.session.commit()
    flash('La coiffure a été supprimée avec succès.', 'success')
    return redirect(url_for('ListCoiffure'))

#=== Abonnement =======

@app.route('/Abonnement/Type/List')
@login_required
# @gestionnaire_required
def ListTypeAbonnement():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    abonnements = TypeAbonnement.query.paginate(page=page, per_page=5)  # Paginer les résultats, 10 éléments par page
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
    abonnements = Abonnement.query.paginate(page=page, per_page=5)  # Paginer les résultats, 10 éléments par page
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

@app.route('/Abonnement/Delete/<int:abonnement_id>', methods=['GET','POST'])
@login_required
def DeleteAbonnement(abonnement_id):
    abonnement = Abonnement.query.get_or_404(abonnement_id)
    db.session.delete(abonnement)
    db.session.commit()
    return redirect(url_for('ListAbonnement'))

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
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Construire le nom de fichier avec le nom et prénom du client et la date
    filename = f"facture_{abonnement.client.nom}_{date_str}.pdf"
    filename = filename.replace(" ", "_")  # Remplacer les espaces par des underscores

    # Chemin relatif pour enregistrer le PDF
    pdf_path = os.path.join(os.getcwd(), filename)
    
    # Enregistrer le PDF 
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    # Envoyer le fichier PDF en réponse à la requête 
    # avec as_attachment a true ,il telecharge directement le fichier si a false 
    # le fichier est d'abord visionner par le navigateur et on peut l'imprimer ou l'enregistrer en pdf 
    return send_file(pdf_path, as_attachment=True) 






