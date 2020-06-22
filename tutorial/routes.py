from flask import Flask, render_template, url_for, flash, redirect, request
from tutorial.forms import RegisterForm, LoginForm, EstudianteForm, CarreraForm
from tutorial import db, app

from flask_login import login_required, current_user, login_user, logout_user

@app.route('/')
def home():
    return render_template('index.html', titulo ='Home')

@app.route('/about')
def about():
    return render_template('about.html', titulo='About')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', titulo='Registro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login successful for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', titulo='Login', form=form)

@app.route('/estudiantes', methods=['GET', 'POST'])
def estudiante():
    form = EstudianteForm()
    return render_template('estudiante.html', titulo = 'Estudiantes', form=form)

@app.route('/carreras')
def carrera():
    cursor = db.connection.cursor()
    cursor.callproc('verCarreras')
    data = cursor.fetchall()
    return render_template('carrera.html', titulo = 'Carreras', career=data)

@app.route('/carreras/crear', methods=['GET', 'POST'])
def crearCarrera():
    form = CarreraForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            identificacion = form.identificacion.data
            nombre = form.nombre.data
            extension = form.extension.data

            args = (identificacion, nombre, extension)
            cursor = db.connection.cursor()
            cursor.callproc('crearCarrera', args)
            db.connection.commit()
            cursor.close()

            flash(f'Ha creado de manera correcta la carrera de {form.nombre.data}!', 'success')
            return redirect(url_for('carrera'))
        except:
            flash(f'Revise que los datos no estén repetidos', 'danger')
            return redirect(url_for('carrera'))

    return render_template('crearCarrera.html', titulo = 'Crear Carrera', form = form)

@app.route('/carreras/<int:id_carrera>')
def verCarrera(id_carrera):
    cursor = db.connection.cursor()
    cursor.callproc('verCarrera', [id_carrera])
    datos = cursor.fetchone()
    return render_template('verCarrera.html', titulo = 'Ver Carrera', carrera = datos)

@app.route('/carreras/<int:id_carrera>/modificar', methods=['GET', 'POST'])
def editarCarrera(id_carrera):
    form = CarreraForm()
    if form.validate_on_submit():
        ident = form.identificacion.data
        nombre = form.nombre.data
        extension = form.extension.data

        args = (ident, nombre, extension, id_carrera)

        cursor = db.connection.cursor()
        cursor.callproc('modificarCarrera', args)
        db.connection.commit()
        flash(f'Ha modificado de manera correcta la carrera de {form.nombre.data}!', 'success')
        return redirect(url_for('carrera'))
    elif request.method == "GET":
        cursor = db.connection.cursor()
        cursor.callproc('verCarrera', [id_carrera])
        for career in cursor.fetchall():
            form.identificacion.data = career[0]
            form.nombre.data = career[1]
            form.extension.data = career[2]
    return render_template('modificarCarrera.html', nombrecito = 'Modificar Carrera' ,titulo = 'Modificar Carrera', form = form)

@app.route('/carreras/<int:id_carrera>/eliminar', methods=['GET', 'POST'])
def eliminarCarrera(id_carrera):
    cursor = db.connection.cursor()
    cursor.callproc('eliminarCarrera', [id_carrera])
    db.connection.commit()
    return redirect(url_for('carrera'))