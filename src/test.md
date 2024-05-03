from decimal import Decimal

@app.route('/Facture/Add', methods=['GET', 'POST'])
@login_required
def AddFacture():
    form = AddFactureForm()
    # Charger les produits disponibles dans la liste déroulante
    form.produit.choices = [(produit.id, produit.nom) for produit in Produit.query.all()]

    if form.validate_on_submit():
        produit_id = form.produit.data
        quantite = form.quantite.data

        # Récupération du prix du produit à partir de son ID
        produit = Produit.query.get(produit_id)
        prix_produit = Decimal(produit.prix)  # Convertir le prix du produit en Decimal

        # Convertir la quantité en Decimal
        quantite = Decimal(quantite)

        # Calcul du montant total de la facture
        montant_total = prix_produit * quantite

        # Création de la facture
        facture = Facture(user_id=current_user.id, produit_id=produit_id, quantite=quantite, montant_total=montant_total, date=datetime.now())
        db.session.add(facture)
        db.session.commit()

        return redirect(url_for('ListFacture'))

    return render_template('caissier/facture/AddFacture.html', form=form)