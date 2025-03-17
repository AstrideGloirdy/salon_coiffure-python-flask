from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from ..models import Client, TypeAbonnement

class AddAbonnementForm(FlaskForm):
    client_id = SelectField(
        'Client',
        coerce=int,
        choices=[],
        validators=[
            DataRequired(message="Veuillez sélectionner un client"),
        ]
    )

    type_abonnement_id = SelectField(
        'Type Abonnement',
        coerce=int,
        choices=[],
        validators=[
            DataRequired(message="Veuillez sélectionner un type d'abonnement"),
        ]
    )

    

    def __init__(self, *args, **kwargs):
        super(AddAbonnementForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(client.id, f"{client.nom} {client.prenom}") for client in Client.query.all()]
        self.type_abonnement_id.choices = [(abonnement.id, abonnement.nomTypeAbonnement) for abonnement in TypeAbonnement.query.all()]
