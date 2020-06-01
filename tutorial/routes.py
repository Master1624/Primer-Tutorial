from flask import Flask, render_template, url_for, flash, redirect
from tutorial.forms import RegisterForm, LoginForm
from tutorial import db, app

posts=[
    {
        'autor': 'Juan',
        'fecha': '30 de Mayo',
        'clima': 'Lluvioso'
    },
    {
        'autor': 'Maria',
        'fecha': 'Abril',
        'clima': 'Templado'
    },
    {
        'autor': 'Santiago'
    }
]

@app.route('/')
def home():
    return render_template('index.html', info = posts, titulo ='Home')

@app.route('/about')
def about():
    return render_template('about.html', info = posts, titulo='About')

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
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', titulo='Login', form=form)