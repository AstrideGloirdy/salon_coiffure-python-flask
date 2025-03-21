from flask import render_template,request,redirect,url_for
from ..models import User,db,Role,app
from ..forms.SecurityForms import AddUserForm
from .auth_routes import login_required

from flask_bcrypt import Bcrypt



bcrypt = Bcrypt(app)


@app.route('/User/List')
@login_required
def ListUser():
   page = request.args.get('page', 1, type=int)  
   users = User.query.paginate(page=page, per_page=5) 
   return render_template('admin/user/ListUser.html', users=users)




@app.route('/User/Add', methods=['GET', 'POST'])
@login_required
def AddUser():
   form = AddUserForm()
   form.role.choices = [(roles.id, roles.name) for roles in Role.query.all()]
   if form.validate_on_submit():
      hashed_password= bcrypt.generate_password_hash(form.password.data)
      role_id = form.role.data  
      role = Role.query.get(role_id)   
      user = User(
            login=form.login.data,
            password=hashed_password,
            nom=form.nom.data,
            prenom=form.prenom.data,
            telephone=form.telephone.data,
            adresse=form.adresse.data,
            role=role
      )
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('ListUser'))
   return render_template('admin/user/AddUser.html', form=form)


