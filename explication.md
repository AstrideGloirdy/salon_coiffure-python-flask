FlaskForm

from wtforms import StringField : comme un input text permet de saisir les champs de saisit ,voir documentation 

avoir une cle secret :

app.config["SECRET_KEY"]="voiciMaCleSecret"

if form.validate_on_submit pour savoir si on a submit le formulaire et on donne les actions dans la route 

pour recuperer les donnees on a form.username.data etc si on a form=LoginForm()


Valider les formulaires ,creer le formulaire d'abord 


pour mettre le mot de passe en clair et masque 

dans le form : 

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    show_password = BooleanField('Afficher le mot de passe')
    submit = SubmitField('Se connecter')

dans le html :  

<form method="POST" action="{{ url_for('login') }}">
    {{ form.hidden_tag() }}
    <div>
        {{ form.email.label }}
        {{ form.email() }}
    </div>
    <div>
        {{ form.password.label }}
        {% if form.show_password.data %}
            {{ form.password(type="text") }}
        {% else %}
            {{ form.password(type="password") }}
        {% endif %}
    </div>
    <div>
        {{ form.show_password.label }}
        {{ form.show_password() }}
    </div>
    <div>
        {{ form.submit() }}
    </div>
</form>


// on utilise dans la base 
{% block content %}
{% endblock  %}

 et dans la page fille 

 {% extends "layouts/base.html" %}

 {% block content %}
 {% endblock %}


 on peut avoir aussi des {% block title %} {% endblock %}

 on peut ajouter avec 
 {% block title %}
    {{super() }} | client  
  {% endblock %}



- nom salon de coiffure : AfroChic Coiffure


- Mode de fonctionnement des abonnements dans le salon de coiffure 

Les clients payent une inscription pour souscrire à un abonnement 
Un abonnement a un type de coiffure definies (tresses mi-longues) ,un nombre de coiffure par mois 
selon le prix de l'abonnement ,une reduction est accorde sur le nombre de coiffure 
une carte est donne et ceux qui ont cette carte et se font tresser la presente lors de la prestation a la caisse 
ensuite a la fin du mois une facture est donnee a payer du total des prestations avec une reduction 
