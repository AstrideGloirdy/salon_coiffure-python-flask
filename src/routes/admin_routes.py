from flask import Blueprint,render_template
from ..models import  Categorie

admin = Blueprint('admin', __name__)

@admin.route('/home')
def home():
   categories = Categorie.query.all()
    #return "<h1>Test de l'application pour l'admin</h1>"
   #return render_template('layouts/base.html')
   return render_template('layouts/base.html',categories=categories)

@admin.route('/')
def error():
   return render_template('errors/error-404.html')

@admin.route('/Ast')
def error1():
   return render_template('errors/error-500.html')