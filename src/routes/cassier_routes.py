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



##### hope last one 
@app.route('/Facture/Add', methods=['GET', 'POST'])
@login_required
def AddFacture():
    form = AddFactureForm()
    form.produit.choices = [(produit.id, produit.nom) for produit in Produit.query.all()]
    form.coiffure.choices = [(coiffure.id, coiffure.nom) for coiffure in Coiffure.query.all()]

    if form.validate_on_submit():
        coiffure_id = form.coiffure.data
        quantiteCoif = form.quantiteCoif.data if coiffure_id else None
        produit_id = form.produit.data
        quantiteProd = form.quantiteProd.data if produit_id else None

        
        # Ajout des produits
        if produit_id and quantiteProd:
            produit = Produit.query.get(produit_id)
            prix_produit = produit.prix
            montant_produit = prix_produit * quantiteProd
            produits = session.get('produits', [])
            # Stocker l'identifiant du produit dans la session
            produits.append({'id': produit.id, 'nom': produit.nom, 'prix': prix_produit, 'quantite': quantiteProd, 'montant': montant_produit})
            session['produits'] = produits
#           # Réduire la quantité en stock du produit
            produit.qteStock -= quantiteProd
            db.session.commit()
        if coiffure_id and quantiteCoif:
            coiffure = Coiffure.query.get(coiffure_id)
            prix_coiffure = coiffure.prix
            montant_coiffure = prix_coiffure * quantiteCoif
            coiffures = session.get('coiffures', [])
            coiffures.append({'id': coiffure.id, 'nom': coiffure.nom, 'prix': prix_coiffure, 'quantite': quantiteCoif, 'montant': montant_coiffure})
            session['coiffures'] = coiffures
        
        return redirect(url_for('AddFacture'))

    # Calcul du montant total
    montant_total = sum(produit['montant'] for produit in session.get('produits', [])) + sum(coiffure['montant'] for coiffure in session.get('coiffures', []))
    if request.method == 'POST' and 'Enregistrer' in request.form:
        # Enregistrement de la facture dans la base de données
        facture = Facture(user_id=current_user.id, montant_total=montant_total, date=datetime.now())
        db.session.add(facture)
        db.session.commit()

        # Mise à jour du montant total dans la caisse
        caisse = Caisse(montant_total=montant_total)
        db.session.add(caisse)
        db.session.commit()

        # Enregistrement des détails de la facture dans la base de données
        for produit in session.get('produits', []):
            details = DetailsFacture(facture_id=facture.id, produit_id=produit['id'], quantite_produit=produit['quantite'])
            db.session.add(details)

        for coiffure in session.get('coiffures', []):
            details = DetailsFacture(facture_id=facture.id, coiffure_id=coiffure['id'], quantite_coiffure=coiffure['quantite'])
            db.session.add(details)
        db.session.commit()
         # Réinitialisation des données de session
        session.pop('produits', None)
        session.pop('coiffures', None)
        return redirect(url_for('ListFacture'))
       

    return render_template('caissier/facture/AddFacture.html', form=form, produits=session.get('produits', []), coiffures=session.get('coiffures', []), montant_total=montant_total)

   
@app.route('/Facture/details/<int:id>', methods=['GET'])
@login_required
def DetailFacture(id):
    facture = Facture.query.get_or_404(id)
    return render_template('caissier/facture/Facture.html', facture=facture)


@app.route('/Caisse/')
@login_required
def VoirCaisse():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    caisses = Caisse.query.paginate(page=page, per_page=10)
    total_caisse = sum(caisse.montant_total for caisse in caisses.items) 
    return render_template('caissier/caisse/VoirCaisse.html',caisses=caisses,total_caisse=total_caisse)






