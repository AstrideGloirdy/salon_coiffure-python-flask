from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length


class AddClientForm(FlaskForm):
    nom = StringField(
        'Nom du client',
        validators=[
            DataRequired(message="Le nom est requis."),
            Length(min=1, max=100, message="Le nom doit avoir entre 1 et 100 caractères.")
        ]
    )
    prenom = StringField(
        'Prénom du client',
        validators=[
            DataRequired(message="Le prénom est requis."),
            Length(min=1, max=100, message="Le prénom doit avoir entre 1 et 100 caractères.")
        ]
    )
    telephone = StringField(
        'Numéro de téléphone',
        validators=[
            DataRequired(message="Le numéro de téléphone est requis."),
            Length(min=1, max=100, message="Le numéro de téléphone doit avoir entre 1 et 100 caractères.")
        ]
    )
    adresse = StringField(
        'Adresse du client',
        validators=[
            DataRequired(message="L'adresse est requise."),
            Length(min=1, max=250, message="L'adresse doit avoir entre 1 et 250 caractères.")
        ]
    )

   
 
class SearchForm(FlaskForm):
    search_query = StringField(
        'Recherche',
        render_kw={"class": "form-control",
                    "aria-label": "search", 
                    "aria-describedby": "search"})
    submit = SubmitField('Rechercher', render_kw={"class": "btn btn-primary"})