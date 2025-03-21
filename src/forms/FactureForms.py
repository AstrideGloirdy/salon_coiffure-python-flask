from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField,FloatField, SubmitField,validators
from wtforms.validators import DataRequired,InputRequired


class AddFactureForm(FlaskForm):
    produit = SelectField('Produit',validators=[validators.Optional()])
    coiffure = SelectField('Coiffure',validators=[validators.Optional()])
    client= SelectField('Coiffure',validators=[validators.Optional()])
    quantiteProd = IntegerField('Quantité de Produit',validators=[validators.Optional()])
    quantiteCoif = IntegerField('Nombre de coifure',validators=[validators.Optional()])
    submit = SubmitField('Ajouter')


class AddPaiementForm(FlaskForm):
    montant_paye= FloatField(
        'Montant payé',
        validators=[
            DataRequired(),
            InputRequired("Ce champ est obligatoire !!!!")
        ])
    submit = SubmitField('Enregistrer')



class AddPaiementAbo(FlaskForm):
    client= SelectField('Coiffure',validators=[validators.Optional()])
    submit = SubmitField('Ajouter')



















# class ClientForm(FlaskForm):
#     client = SelectField('Client', coerce=int, validators=[DataRequired()])
#     submit = SubmitField('Add')

# class RechercheForm(FlaskForm):
#     recherche = StringField('Recherche', validators=[DataRequired()])
#     submit = SubmitField('Search')

# class FactureForm(FlaskForm):
#     quantite = IntegerField('Quantité', validators=[DataRequired()])
#     submit = SubmitField('Ajouter')

# class PaiementForm(FlaskForm):
#     montant_paye = IntegerField('Montant Payé', validators=[DataRequired()])
#     submit = SubmitField('Enregistrer Paiement')