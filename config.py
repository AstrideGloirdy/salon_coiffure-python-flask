""" Installation - configuration-requtes de base"""

import os
DEBUG = True
APP_NAME= "GestionSalon"
SECRET_KEY="MaCleSecrete"

#------ Config pour SQLAlchemy -------

SQLALCHEMY_TRACK_MODIFICATIONS = False
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/gastr/Desktop/projet python/GestionSalon/gestion.sqlite"

#----- Fichier de telecharement des photos 

UPLOAD_FOLDER = 'C:/Users/gastr/Desktop/projet python/GestionSalon/src/Upload'
