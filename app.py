# from src import create_app,gestionnaire
# from src.models import db
# from flask_migrate import Migrate

# # Initialiser l'application Flask
# app = create_app()

# # Initialiser la base de données SQLAlchemy
# migrate = Migrate(app, db)
 

# if __name__ == "__main__":
   
#     with app.app_context():
#         db.create_all()
       

#     app.run(debug=True)

from src import app
from src.routes.admin_routes import *
from src.routes.auth_routes import *
from src.routes.cassier_routes import *
from src.routes.gestionnaire_routes import *
from src.routes.Security import *
from src.forms import *
from src.fileManager import *


# Initialiser l'application Flask



 

if __name__ == "__main__":
   
  

    app.run(debug=True)

