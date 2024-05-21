from flask import Blueprint, render_template, redirect, session,url_for, request,flash
from flask_login import login_user, logout_user, login_required,current_user,LoginManager
from ..models import User,app
from .gestionnaire_routes import ListerArticle
from ..forms.SecurityForms import LoginForm
from flask_bcrypt import Bcrypt 




bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)





@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(login=form.login.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.role.name == 'admin':
                    return redirect(url_for('ListUser'))
                elif user.role.name == 'caissier':
                    return redirect(url_for('ListFacture'))
                elif user.role.name == 'gestionnaire':
                    return redirect(url_for('ListerArticle'))
                # Ajoutez d'autres conditions pour d'autres rôles si nécessaire
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
                return redirect(url_for('login'))
    return render_template('security/connexion.html', form=form)



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def test():
     return render_template('test.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

