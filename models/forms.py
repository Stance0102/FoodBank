from flask_wtf import FlaskForm
from wtforms import Form, StringField ,PasswordField ,SelectField ,validators,IntegerField
from wtforms.fields.html5 import EmailField
from models.person import Member

class RegistrationForm(FlaskForm):
	name = StringField('帳號',[validators.DataRequired(),validators.Length(min=2,max=30)])
	email = EmailField('Email',[validators.DataRequired(),validators.Email()])
	password = PasswordField('密碼',[
		validators.DataRequired(),
		validators.EqualTo('confirm',message = '密碼必須一致')
	])
	confirm = PasswordField('再次輸入密碼')
	address = StringField('聯絡地址',[validators.DataRequired(),validators.Length(min=4,max=30)])
	role = SelectField('身分', choices=[('user','一般使用者'),('mechanism','機構')])
	#def validate_name(FlaskForm,field):
	#	if Member.query.filter(name = field.data).first():
	#		raise ValidationError('帳號已被註冊過了')

class LoginForm(FlaskForm):
	name = StringField('輸入帳號',[validators.DataRequired()])
	password = PasswordField('輸入密碼',[validators.DataRequired()])
	role = SelectField('身分', choices=[('user','一般使用者'),('mechanism','機構')])

class MaterialForm(FlaskForm):
	name = StringField('名稱',[validators.DataRequired(),validators.Length(min=1,max=10)])
	quantity = IntegerField('數量',[validators.DataRequired()]) 