from flask import Blueprint, render_template, request, redirect, url_for,flash
from ..models import  Produit,Categorie,Client,Abonnement,TypeAbonnement,Coiffure,db
from  ..forms.ArticleForms import AddArticleForm,AddCategorieForm
from ..forms.ClientForms import AddClientForm
from ..forms.CoiffureForms import AddCoiffureForm
from ..forms.TypeAbonnementForms import AddTypeAbonnementForm
from ..forms.AbonnementForms import AddAbonnementForm
from ..fileManager import save_uploaded_file

gestionnaire = Blueprint('gestionnaire', __name__)



@gestionnaire.route('/home')
def home():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    produits = Produit.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/home.html', produits=produits)

#======== Categorie ============

@gestionnaire.route('/Article/Categorie/List',methods=['GET', 'POST'])
def ListerCategorie():
    form = AddCategorieForm()
    page = request.args.get('page', 1, type=int)
    categories = Categorie.query.paginate(page=page, per_page=7)
    
    if form.validate_on_submit():
        categorie = Categorie(nom=form.nom.data)
        db.session.add(categorie)
        db.session.commit()
        # flash('Catégorie ajoutée avec succès!', 'success')
        return redirect(url_for('gestionnaire.ListerCategorie'))
    
    return render_template('gestionnaire/ListerCategorie.html', form=form, categories=categories)

#======== Produit ============

@gestionnaire.route('/Article/Add', methods=['GET','POST'])
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
        flash('Le produit a été ajouté avec succès!', 'success')  # Affiche un message de succès à l'utilisateur
        return redirect(url_for('gestionnaire.home'))
    return render_template('gestionnaire/AjouterArticle.html',form=form)


#======== coiffure ============ 

@gestionnaire.route('/Client/List')
def ListClient():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    clients = Client.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/ListClient.html', clients=clients)


@gestionnaire.route('/Client/Add',methods=['GET','POST'])
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
        return redirect(url_for('gestionnaire.ListClient'))
    return render_template('gestionnaire/AddClient.html',form=form)


#======== coiffure ============

@gestionnaire.route('/Coiffure/List')
def ListCoiffure():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    coiffures = Coiffure.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/ListCoiffure.html', coiffures=coiffures)


@gestionnaire.route('/Coiffure/Add',methods=['GET','POST'])
def AddCoiffure():
    form = AddCoiffureForm()
    if form.validate_on_submit():
        coiffure = Coiffure(
                nom=form.nom.data,
                prix=form.prix.data,
            )
        db.session.add(coiffure)
        db.session.commit()
        return redirect(url_for('gestionnaire.ListCoiffure'))
    return render_template('gestionnaire/AddCoiffure.html',form=form)


#=== Abonnement =======

@gestionnaire.route('/Abonnement/Type/List')
def ListTypeAbonnement():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    abonnements = TypeAbonnement.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/ListTypeAbonnement.html', abonnements=abonnements)


@gestionnaire.route('/Abonnement/Type/Add', methods=['GET', 'POST'])
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
        return redirect(url_for('gestionnaire.ListTypeAbonnement'))
    return render_template('gestionnaire/AddTypeAbonnement.html', form=form)



#======== Abonnement ============

@gestionnaire.route('/Abonnement/List')
def ListAbonnement():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    abonnements = Abonnement.query.paginate(page=page, per_page=10)  # Paginer les résultats, 10 éléments par page
    return render_template('gestionnaire/ListAbonnement.html', abonnements=abonnements)



@gestionnaire.route('Abonnement/Add', methods=['GET', 'POST'])
def AddAbonnement():
    form = AddAbonnementForm()
    success_message = None  # Définir success_message à None par défaut
    if form.validate_on_submit():
        abonnement = Abonnement(
            client_id=form.client_id.data,
            type_abonnement_id=form.type_abonnement_id.data
        )
        db.session.add(abonnement)
        db.session.commit()
        success_message = "L'abonnement a été ajouté avec succès."
        flash(success_message, 'success')  # Stocker le message de succès dans la session
        return redirect(url_for('gestionnaire.ListAbonnement'))
    return render_template('gestionnaire/AddAbonnement.html', form=form)

@gestionnaire.route('/Abonnement/details/<int:id>', methods=['GET'])
def DetailAbonnement(id):
    abonnement = Abonnement.query.get_or_404(id)
    return render_template('gestionnaire/DetailAbonnement.html', abonnement=abonnement)













# @gestionnaire.route('/Article/Delete/<int:produit_id>', methods=['POST'])
# def SupprimerProduit(produit_id):
#     produit = Produit.query.get_or_404(produit_id)
#     db.delete(produit)  # Utilisez la fonction delete définie dans votre modèle de données
#     flash('Le produit a été supprimé avec succès!', 'success')
#     return redirect(url_for('gestionnaire.home'))

# @gestionnaire.route('/modifier-produit/<int:produit_id>', methods=['GET', 'POST'])
# def ModifierProduit(produit_id):
#     produit = Produit.query.get_or_404(produit_id)
#     if form.validate_on_submit():
#         form.populate_obj(produit)
#         db.update(produit)  # Utilisez la fonction update définie dans votre modèle de données
#         flash('Le produit a été modifié avec succès!', 'success')
#         return redirect(url_for('gestionnaire.home'))
#     return render_template('modifier_produit.html', form=form)