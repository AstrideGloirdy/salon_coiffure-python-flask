from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,FileField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, NumberRange,Length,InputRequired
from flask_wtf.file import FileAllowed, FileSize

class AddArticleForm(FlaskForm):
    nom = StringField(
    'Nom de l\'article',
    validators=[
        DataRequired(),
        InputRequired("Le nom saisie est invalide"),
        Length(min=1, max=200)]
    )

    prix = IntegerField(
        'Prix unitaire de l\'article',
        validators=[
            DataRequired(),
            InputRequired("Le prix unitaire est obligatoire !!!"),
            NumberRange(min=0,max=100000)
            ]
    )

    qte_stock = IntegerField(
        'Quantité en stock',
        validators=[
            DataRequired(), 
            InputRequired("Le quantite n'est pas valide obligatoire !!!"),
            NumberRange(min=0, max=200)]
    )

    categorie = SelectField(
        'Catégorie de l\'article',
        choices=[],
        validators=[
            DataRequired(message="Veuillez sélectionner une catégorie")]
            
    )

    photo = FileField(
        'Photo de l\'article',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], message="Seuls les fichiers JPG, JPEG et PNG sont autorisés"),
            FileSize(max_size=5 * 1024 * 1024, message="La taille de l'image ne doit pas dépasser 5 Mo")
        ]
    )

    description = TextAreaField(
        'Description de l\'article',
        validators=[Length(max=500, message="La description ne doit pas dépasser 500 caractères")]
    )
    
class EditArticleForm(FlaskForm):
    nom = StringField('Nom de l\'article',validators=[DataRequired(),InputRequired("Le nom saisie est invalide"),Length(min=1, max=200)])
    prix = IntegerField( 'Prix unitaire de l\'article', validators=[ DataRequired(), InputRequired("Le prix unitaire est obligatoire !!!"),NumberRange(min=0,max=100000) ])
    qte_stock = IntegerField( 'Quantité en stock',validators=[DataRequired(), InputRequired("Le quantite n'est pas valide obligatoire !!!"),NumberRange(min=0, max=200)])
    categorie = SelectField( 'Catégorie de l\'article', choices=[], validators=[DataRequired(message="Veuillez sélectionner une catégorie")] )
    photo = FileField( 'Photo de l\'article', validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="Seuls les fichiers JPG, JPEG et PNG sont autorisés"),FileSize(max_size=5 * 1024 * 1024, message="La taille de l'image ne doit pas dépasser 5 Mo")])
    description = TextAreaField( 'Description de l\'article',validators=[Length(max=500, message="La description ne doit pas dépasser 500 caractères")])


class AddCategorieForm(FlaskForm):
    nom = StringField('Nom de la catégorie', validators=[DataRequired()])

class SearchForm(FlaskForm):
    search_query = StringField(
        'Recherche',
        render_kw={"placeholder": " nom de l'article...",
                    "class": "form-control",
                    "aria-label": "search", 
                    "aria-describedby": "search"})
    submit = SubmitField('Rechercher', render_kw={"class": "btn btn-primary"})

class ApprovisionnementForm(FlaskForm):
    qte_appro = IntegerField('Quantité à approvisionner', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Approvisionner')