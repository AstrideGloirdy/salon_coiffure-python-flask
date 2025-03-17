from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField,PasswordField,EmailField
from wtforms.validators import DataRequired,Length,InputRequired,Email,ValidationError
from ..models import User

class LoginForm(FlaskForm):
    login = EmailField('Login', 
                        validators=[
                            DataRequired(message="le login n'est pas valide"), 
                            Length(min=4, max=20),
                            Email(message="Votre adresse Email n'est pas correcte ou complete"),
                            InputRequired()]
                        )
    password = PasswordField('Password', 
                             validators=[
                                DataRequired(message="Le mot de passe incorrecte"),
                                Length(min=6),
                                InputRequired(message="Le password est obligatoire")])
    
    submit = SubmitField('Login')



class AddUserForm(FlaskForm):
    login = EmailField('Login', 
                       validators=[
                            DataRequired(), 
                            Length(min=4, max=100),
                            InputRequired(message="Le login est obligatoire"),
                            Email()
                             ])
    password = PasswordField('Password', 
                             validators=[
                                DataRequired(),
                                Length(min=6, max=128),
                                InputRequired(message="Le mot de passe est obligatoire")])
    nom = StringField('Nom', 
                      validators=[
                          DataRequired(), 
                          Length(max=100),
                          InputRequired(message="Le nom est obligatoire")
                          ])
    prenom = StringField('Prénom',
                          validators=[
                            DataRequired(),
                            Length(max=100),
                            InputRequired(message="Le prenom est obligatoire")
                                ])
    telephone = StringField('Téléphone', 
                            validators=[
                                DataRequired(),
                                Length(max=100),
                                InputRequired(message="Le numero de telephone est obligatoire")],
                                 )
    
    adresse = StringField('Adresse', 
                          validators=[
                              DataRequired(),
                                Length(max=250),
                                InputRequired(message="L'adresse est obligatoire")])
    role = SelectField('Role',
                       choices=[], 
                       coerce=int, 
                       validators=[DataRequired(message="Veuillez selectionner un role pour l'utilisateur")]
                       )
    submit = SubmitField('Enregistrer')
    
    def validate_login(self,login):
        existing_login=User.query.filter_by(
            login=login.data).first()
        if existing_login:
            raise ValidationError(
                "Ce login existe deja. Veuillez en choisir un autre"
            )

#  <span class="password-toggle-icon"><i class="fas fa-eye"></i></span>




