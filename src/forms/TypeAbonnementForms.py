from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField
from wtforms.validators import DataRequired, NumberRange,Length,InputRequired

class AddTypeAbonnementForm(FlaskForm):
    nom = StringField(
        'Nom de l\'abonnement',
        validators=[
            DataRequired(),
            InputRequired("Le nom saisi est invalide"),
            Length(min=1, max=200)]
    )

    taux_reduction = IntegerField(
        'Taux de réduction (%)',
        validators=[NumberRange(min=0, max=100),
                    InputRequired()]
    )

    nombre_coiffures_incluses = IntegerField(
        'Nombre de coiffures incluses',
        validators=[DataRequired(),
                    InputRequired(),
                    NumberRange(min=0)]
    )

    coiffure_id = SelectField(
        'Coiffure',
        coerce=int,
        choices=[],
        validators=[DataRequired(message="Veuillez sélectionner une coiffure"),
                    InputRequired()]
    )
