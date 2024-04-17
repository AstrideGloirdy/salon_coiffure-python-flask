
Entités :

Client : Représente un client du salon de coiffure.
Attributs : ID du client, nom, prénom, numéro de téléphone, adresse, etc.
Abonnement : Représente un abonnement mensuel souscrit par un client.
Attributs : ID de l'abonnement, type d'abonnement, montant mensuel, date de début, date de fin, etc.
Type de Coiffure : Représente les différents types de coiffures proposés par le salon.
Attributs : ID du type de coiffure, nom, description, prix, etc.
Carte d'Abonnement : Représente la carte d'abonnement remise au client lors de la souscription.
Attributs : ID de la carte, ID du client, ID de l'abonnement, date de délivrance, date d'expiration, etc.
Relations :

Un client peut avoir plusieurs abonnements, mais un abonnement est associé à un seul client. Relation un à plusieurs entre Client et Abonnement.
Un abonnement est lié à un type de coiffure spécifique. Relation un à un entre Abonnement et Type de Coiffure.
Une carte d'abonnement est associée à un client et à un abonnement spécifiques. Relation un à un entre Carte d'Abonnement, Client et Abonnement.
Exemple de Schéma de Base de Données :

Table Client : ID (PK), Nom, Prénom, Numéro de Téléphone, Adresse, etc.
Table Abonnement : ID (PK), ID_Client (FK), Type_Abonnement, Montant_Mensuel, Date_Début, Date_Fin, etc.
Table Type_Coiffure : ID (PK), Nom, Description, Prix, etc.
Table Carte_Abonnement : ID (PK), ID_Client (FK), ID_Abonnement (FK), Date_Délivrance, Date_Expiration, etc.
Cette modélisation permet de gérer les abonnements mensuels des clients du salon de coiffure de manière efficace, en prenant en compte les différentes relations entre les clients, les abonnements, les types de coiffures et les cartes d'abonnement.


_______________________________


Entités :

Client : Représente un client du salon de coiffure.
Abonnement : Représente un abonnement mensuel souscrit par un client.
Attributs : ID de l'abonnement, type d'abonnement, montant mensuel, date de début, date de fin, nombre de coiffures inclus, taux de réduction, etc.
Type de Coiffure : Représente les différents types de coiffures proposés par le salon.
Carte d'Abonnement : Représente la carte d'abonnement remise au client lors de la souscription.
Paiement Abonnement : Représente le paiement effectué lors de la souscription à un abonnement.
Attributs : ID du paiement, ID de l'abonnement, montant payé, date de paiement, etc.
Relations :

Un abonnement est associé à un seul type de coiffure. Relation un à un entre Abonnement et Type de Coiffure.
Une carte d'abonnement est associée à un client et à un abonnement spécifiques. Relation un à un entre Carte d'Abonnement, Client et Abonnement.
Un paiement est associé à un abonnement spécifique. Relation un à un entre Paiement Abonnement et Abonnement.
Exemple de Schéma de Base de Données :

Table Client : ID (PK), Nom, Prénom, Numéro de Téléphone, Adresse, etc.
Table Abonnement : ID (PK), ID_Type_Coiffure (FK), Montant_Mensuel, Date_Début, Date_Fin, Nombre_Coiffures_Inclus, Taux_Réduction, etc.
Table Type_Coiffure : ID (PK), Nom, Description, Prix, etc.
Table Carte_Abonnement : ID (PK), ID_Client (FK), ID_Abonnement (FK), Date_Délivrance, Date_Expiration, etc.
Table Paiement_Abonnement : ID (PK), ID_Abonnement (FK), Montant_Payé, Date_Paiement, etc.
Cette extension permet de prendre en compte le paiement lors de la souscription à un abonnement, ainsi que la définition du nombre de coiffures inclus et du taux de réduction pour chaque type d'abonnement.



<div class="row">
  {% for abonnement in abonnements %}
  <div class="col-lg-3 col-md-6 col-sm-8 col-xs-12 ">
      <div class="card  " style="width: 200px; border-width: 10px; border-style: solid;
       border-radius: 10px; border-color: aqua;
       font-size: small;
       ">
          <div class="card-header orange-bg text-white">
              <h5 class="card-title">{{ abonnement.nomTypeAbonnement }}</h5>
          </div>
          <div class="card-body">
              <h6 class="card-subtitle mb-2">Abonnement Mensuel</h6>
              <ul class="list-group list-group-flush">
                  <li class="list-group-item rounded"> Taux de réduction : {{ abonnement.taux_reduction }}%</li>
                  <li class="list-group-item rounded"><i class="fa fa-cut text-orange"></i> Nombre de coiffures incluses : {{ abonnement.nombre_coiffures_incluses }}</li>
                  <li class="list-group-item rounded"><i class="fa fa-scissors text-orange"></i> Nombre de coiffures restantes : {{ abonnement.nombre_coiffures_restantes }}</li>
              </ul>
          </div>
          
      </div>
  </div>
  {% endfor %}
</div>