
# from flask import Flask
# from flask_login import LoginManager
# from config import UPLOAD_FOLDER
# from .routes.gestionnaire_routes import gestionnaire
# from .routes.admin_routes import admin
# from .routes.cassier_routes import cassier

# from .models import db  



# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config')
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    

#     # Initialiser la base de données
#     db.init_app(app)

   
   

  

#     # Enregistrer les Blueprints
#     app.register_blueprint(gestionnaire, url_prefix='/gestionnaire')
#     app.register_blueprint(cassier, url_prefix='/cassier')
#     app.register_blueprint(admin, url_prefix='/admin')
#     # app.register_blueprint(authentication)

#     return app


from .models import app
