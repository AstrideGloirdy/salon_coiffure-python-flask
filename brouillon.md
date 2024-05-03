
class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    montant_total = db.Column(db.Float, nullable=False)
    montant_paye = db.Column(db.Float, nullable=False)
    montant_restant = db.Column(db.Float, nullable=False)
    produits = db.relationship("Produit", secondary=facture_produits, backref="factures")