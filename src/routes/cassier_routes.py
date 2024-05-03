from flask import render_template,request,redirect,url_for,jsonify,session
from ..models import app,Facture,Client,Abonnement,Coiffure,Produit,db 
from .auth_routes import login_required,current_user
from ..forms.FactureForms import AddFactureForm
from sqlalchemy.orm import object_mapper
from datetime import datetime


@app.route('/Cassierhome')
@login_required
def ListFacture():
    page = request.args.get('page', 1, type=int)  # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    factures = Facture.query.paginate(page=page, per_page=10) 
    return render_template('caissier/facture/ListFacture.html',factures=factures)




@app.route('/Facture/Add', methods=['GET', 'POST'])
@login_required
def AddFacture():
    form = AddFactureForm()
    form.produit.choices = [(produit.id, produit.nom) for produit in Produit.query.all()]
    form.coiffure.choices =[(coiffure.id, coiffure.nom ) for coiffure in Coiffure.query.all()]
    # 
    if form.validate_on_submit():
        coiffure_id = form.coiffure.data
        if coiffure_id!=None:
            quantiteCoif = form.quantiteCoif.data
            coiffure = Coiffure.query.get(coiffure_id)
            prix_coif = coiffure.prix

        produit_id = form.produit.data
        if produit_id!=None:
            quantiteProd = form.quantiteProd.data
            produit = Produit.query.get(produit_id)
            prix_prod = produit.prix
            
        # qte stock je dois ajouter un message pour le esle
        
        if quantiteProd!=None and quantiteCoif!=None and produit.qteStock >= quantiteProd:
            # montant total 
            montant_total = float(prix_prod * quantiteProd)+float(prix_coif * quantiteCoif)
        elif quantiteProd!=None and produit.qteStock >= quantiteProd:
            montant_total=float(prix_prod * quantiteProd)
        elif quantiteCoif!=None:
            montant_total=float(prix_coif * quantiteCoif)
        
        facture = Facture(user_id=current_user.id,montant_total=montant_total,date=datetime.now())
        # facture = Facture(user_id=current_user.id,produit_id=None,coiffure_id=None,quantite_coiffure=None,quantite_produit=None,montant_total=montant_total,date=datetime.now())
        if quantiteProd!=None:
            facture.produit_id=produit_id
            facture.quantite_produit = quantiteProd
            
        if quantiteCoif!=None:
            facture.coiffure_id=coiffure_id
            facture.quantite_coiffure=quantiteCoif
        
        db.session.add(facture)
        # enlever la qte en stock 
        if quantiteProd!=None:
            produit.qteStock -= quantiteProd

        db.session.commit()

        return redirect(url_for('ListFacture'))
    return render_template('caissier/facture/AddFacture.html', form=form)


   
@app.route('/Facture/details/<int:id>', methods=['GET'])
@login_required
def DetailFacture(id):
    facture = Facture.query.get_or_404(id)
    return render_template('caissier/facture/Facture.html', facture=facture)









