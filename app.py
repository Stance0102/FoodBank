from flask import Flask, render_template, request, redirect, url_for, session
from database import db_session, init_db
from models.person import Member
from models.material import Material
from sqlalchemy import desc
import datetime
from models.forms import RegistrationForm,LoginForm,MaterialForm
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.before_request
def make_session_permanet():
	session.permanet = True
	app.permanet_session_lifetime = datetime.timedelta(minutes=10)

@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# index
@app.route("/")
def index():
    return render_template("index.html")

#Member Management----------------------------------
@app.route('/signin',methods=['GET','POST'])
def signin():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		member = Member(
			name = form.name.data,
			email = form.email.data,
			password = form.password.data,
			address = form.address.data,
			role = form.role.data
		)
		db_session.add(member)
		db_session.commit()

		return redirect('/login')

	return render_template('signin.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	error = None
	if request.method == 'POST' and form.validate():
		member = Member.query.filter(Member.name == form.name.data).first()
		if member:
			if member.password == form.password.data:
				session['Id'] = member.Id
				session['name'] = member.name
				session['role'] = member.role
				return redirect('/')
			else:
				member = None
		if not member:
			error = "帳號、密碼或身分不正確"
	
	return render_template('login.html',form=form,error=error)

@app.route('/logout')
def logout():
	session.pop('name',None)
	session.pop('Id',None)
	return redirect('/')
#---------------------------------------------------

#Mechanism List-------------------------------------
@app.route('/mechanism_list')
def mechanism_list():
	mechanism_list = Member.query.filter(Member.role == 'mechanism').limit(100)
	return render_template('mechanism_list.html',mechanisms=mechanism_list)
#---------------------------------------------------

#Material Management--------------------------------
@app.route('/create_material',methods=['GET','POST'])
def create_material():
	form = MaterialForm(request.form)
	if request.method == 'POST' and 'role' in session and form.validate():
		curUser = Member.query.filter(Member.name == session['name']).first()
		material = Material(
			name = form.name.data,
			quantity = form.quantity.data,
			create_user_id = curUser.Id,
			create_user_name = curUser.name,
			role = curUser.role
		)
		db_session.add(material)
		db_session.commit()

		if session['role'] == 'user':
			return redirect(url_for('user_material_list'))
		else:
			return redirect(url_for('mechanism_material_list'))

	return render_template('create_material.html',form=form)

@app.route('/user_material_list')
def user_material_list():
	material_list = Material.query.filter(Material.role == 'user', Material.view == True).all()
	return render_template('user_material_list.html',materials=material_list)

@app.route('/mechanism_material_list')
def mechanism_material_list():
	material_list = Material.query.filter(Material.role == 'mechanism', Material.view == True).all()
	return render_template('mechanism_material_list.html',materials=material_list)

@app.route('/material_item_check')
def material_item_check():
	id = request.args.get('id')
	material = Material.query.filter(Material.Id == id ).first()

	if material:
		material.change_id = session['Id']
		material.change_name = session['name']
		material.status = True
		material.view = False
		material.final_datetime = datetime.datetime.now()
		db_session.commit()
		return redirect(url_for('my_already_list'))

	return redirect('/')

@app.route('/my_material_list')
def my_material_list():
	materials = Material.query.filter(Material.create_user_id == session['Id'])
	return render_template('my_material_list.html',materials=materials)

@app.route('/my_already_list')
def my_already_list():
	materials = Material.query.filter(Material.change_id == session['Id'], Material.status == True )
	return render_template('my_already_list.html',materials=materials)

def datetimeformat(value):
	return value.strftime('%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['datetime'] = datetimeformat

#Run App
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run(
    	#host = '163.18.42.226',
    	host = '127.0.0.1',
    	port = 5555,
    	debug = True
	)
