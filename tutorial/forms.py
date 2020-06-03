from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
from tutorial import db, app

def Carreras():
    with app.app_context():
        cursor = db.connection.cursor()
        cursor.callproc('verCarreras')
        for carrera in cursor.fetchall():
            nombreCarrera = carrera[1]
            return nombreCarrera

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EstudianteForm(FlaskForm):
    identificacion = IntegerField('ID Estudiante', validators=[DataRequired()])
    nombre = StringField('Nombre del Estudiante', validators=[DataRequired()])
    apellido = StringField('Apellido del Estudiante', validators=[DataRequired()])
    carrera = SelectField('Carrera', validators=[DataRequired()], choices=[Carreras()])
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Crear Estudiante')

class CarreraForm(FlaskForm):
    identificacion = IntegerField('ID Carrera', [validators.DataRequired(), validators.NumberRange(min=0, max=99999999999)])
    nombre = StringField('Nombre de la Carrera', validators=[DataRequired()])
    extension = StringField('Extensión', validators=[DataRequired()])
    submit = SubmitField('Crear Carrera')