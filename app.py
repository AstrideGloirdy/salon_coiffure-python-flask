from src import create_app, generate_fake_data
from src.models import db
from flask_migrate import Migrate

# Initialiser l'application Flask
app = create_app()

# Initialiser la base de données SQLAlchemy
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Créer toutes les tables dans la base de données et générer des données fictives
    with app.app_context():
        db.create_all()
       

    app.run(debug=True)

