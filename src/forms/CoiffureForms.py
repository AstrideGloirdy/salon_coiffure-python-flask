from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,FileField,TextAreaField,FloatField
from wtforms.validators import DataRequired, NumberRange,Length,InputRequired


class AddCoiffureForm(FlaskForm):
    nom = StringField(
        'Nom de la coiffure',
        validators=[
            DataRequired(message="Le nom de la coiffure est requis."),
            Length(min=1, max=100, message="Le nom de la coiffure doit avoir entre 1 et 100 caractères.")
        ]
    )
    prix = FloatField(
        'Prix de la coiffure (en FCFA)',
        validators=[
            DataRequired(message="Le prix de la coiffure est requis."),
            NumberRange(min=0, message="Le prix de la coiffure doit être supérieur ou égal à zéro.")
        ]
    )