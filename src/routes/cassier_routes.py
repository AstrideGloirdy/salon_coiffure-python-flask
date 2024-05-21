from flask import render_template,request,redirect,url_for,jsonify,session
from ..models import app,Facture,Client,Abonnement,Coiffure,Produit,db,DetailsFacture,Caisse 
from .auth_routes import login_required,current_user
from ..forms.FactureForms import AddFactureForm,AddPaiementForm
from sqlalchemy.orm import object_mapper
from datetime import datetime


@app.route('/Cassierhome')
@login_required
def ListFacture():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    factures = Facture.query.paginate(page=page, per_page=10) 
    return render_template('caissier/facture/ListFacture.html',factures=factures)


#  with functions utilitaires 
@app.route('/Facture/Add', methods=['GET', 'POST'])
@login_required
def AddFacture():
    form = AddFactureForm()
    form.produit.choices = [(produit.id, produit.nom) for produit in Produit.query.all()]
    form.coiffure.choices = [(coiffure.id, coiffure.nom) for coiffure in Coiffure.query.all()]
    form.client.choices = [(client.id, f"{client.nom} {client.prenom}") for client in Client.query.all()]
   
    if form.validate_on_submit():
        help_form(form)
        return redirect(url_for('AddFacture'))

    montant_total = help_total()

    if request.method == 'POST':
        help_payment()
        return redirect(url_for('ListFacture'))
   
    return render_template('caissier/facture/AddFacture.html', form=form, produits=session.get('produits', []), coiffures=session.get('coiffures', []), montant_total=montant_total)


def help_form(form):
    coiffure_id = form.coiffure.data
    quantiteCoif = form.quantiteCoif.data if coiffure_id else None
    produit_id = form.produit.data
    quantiteProd = form.quantiteProd.data if produit_id else None
        
    if 'client_id' not in session:
        session['client_id'] = form.client.data

    if produit_id and quantiteProd:
        produit = Produit.query.get(produit_id)
        prix_produit = produit.prix
        montant_produit = prix_produit * quantiteProd
        produits = session.get('produits', [])
         # Vérifier si le produit est déjà dans la session
        for p in produits:
            if p['id'] == produit.id:
                # Mettre à jour la quantité et le montant
                p['quantite'] += quantiteProd
                p['montant'] += montant_produit
                break
        else:
            # Ajouter le produit à la session
            produits.append({'id': produit.id, 'nom': produit.nom, 'prix': prix_produit, 'quantite': quantiteProd, 'montant': montant_produit})
        session['produits'] = produits
        produit.qteStock -= quantiteProd
        db.session.commit()

    if coiffure_id and quantiteCoif:
        coiffure = Coiffure.query.get(coiffure_id)
        prix_coiffure = coiffure.prix
        montant_coiffure = prix_coiffure * quantiteCoif
        coiffures = session.get('coiffures', [])
        coiffures.append({'id': coiffure.id, 'nom': coiffure.nom, 'prix': prix_coiffure, 'quantite': quantiteCoif, 'montant': montant_coiffure})
        session['coiffures'] = coiffures


def help_total():
    return sum(produit['montant'] for produit in session.get('produits', [])) + sum(coiffure['montant'] for coiffure in session.get('coiffures', []))


def help_payment():
    montant_paye = int(request.form['montant_paye'])
    montant_total = help_total()

    if montant_paye >= montant_total:
        facture = Facture(
            user_id=current_user.id,
            client_id=session.get('client_id'),
            montant_total=montant_total,
            montant_paye=montant_paye,
            montant_rendu=montant_paye - montant_total,
            date=datetime.now())
        db.session.add(facture)
        db.session.commit()

        caisse = Caisse(montant_total=montant_total)
        db.session.add(caisse)
        db.session.commit()

        for produit in session.get('produits', []):
            details = DetailsFacture(facture_id=facture.id, produit_id=produit['id'], quantite_produit=produit['quantite'])
            db.session.add(details)

        for coiffure in session.get('coiffures', []):
            details = DetailsFacture(facture_id=facture.id, coiffure_id=coiffure['id'], quantite_coiffure=coiffure['quantite'])
            db.session.add(details)
        db.session.commit()

        session.pop('client_id', None)
        session.pop('produits', None)
        session.pop('coiffures', None)



@app.route('/Facture/details/<int:facture_id>', methods=['GET'])
@login_required
def DetailFacture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    details = DetailsFacture.query.filter_by(facture_id=facture_id).all()
    return render_template('caissier/facture/Facture.html', facture=facture,details=details)


@app.route('/Caisse/')
@login_required
def VoirCaisse():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    caisses = Caisse.query.paginate(page=page, per_page=10)
    total_caisse = sum(caisse.montant_total for caisse in caisses.items) 
    return render_template('caissier/caisse/VoirCaisse.html',caisses=caisses,total_caisse=total_caisse)





@app.route('/Ventes')
@login_required
def list_ventes_produits():

    page = request.args.get('page', 1, type=int)
    per_page = 2  # Nombre d'éléments par page

    # Requête pour obtenir les détails des factures concernant les produits
    produits_query = db.session.query(DetailsFacture).filter(DetailsFacture.produit_id.isnot(None)).join(Facture).order_by(Facture.date.desc())

    # Paginer les résultats
    produits_paginated = produits_query.paginate(page=page, per_page=per_page)

    # Liste des éléments à afficher
    produits = produits_paginated.items

    return render_template('caissier/ventes/VoirVentes.html', produits=produits, produits_paginated=produits_paginated)
 

@app.route('/Prestations')
@login_required
def list_coiffures():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Nombre d'éléments par page

    # Requête pour obtenir les détails des factures concernant les coiffures
    coiffures_query = db.session.query(DetailsFacture).filter(DetailsFacture.coiffure_id.isnot(None)).join(Facture).order_by(Facture.date.desc())

    # Paginer les résultats
    coiffures_paginated = coiffures_query.paginate(page=page, per_page=per_page)

    # Liste des éléments à afficher
    coiffures = coiffures_paginated.items

    return render_template('caissier/ventes/VoirPrestations.html', coiffures=coiffures, coiffures_paginated=coiffures_paginated)
    