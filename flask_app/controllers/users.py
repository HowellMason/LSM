from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.controllers import dashboard, income, bill
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# LOGIN
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard/' + str(session['user_id']))
    return render_template('login.html')

@app.route('/login/process', methods= ['POST'])
def process_login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.validate_login(data):
        return redirect('/login')
    existing_user = User.get_with_email(data)
    session['user_id'] = existing_user.id
    return redirect('/dashboard/' + str(session['user_id']))


# REGISTER
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/process', methods = ['POST'])
def register_process():
    if not User.validate_registration(request.form):
        return redirect('/register')
    data = {
        'first_name': (request.form['first_name'].strip().title()),
        'last_name': (request.form['last_name'].strip().title()),
        'email': (request.form['email'].strip()),
        'password': bcrypt.generate_password_hash(request.form['password']),
        'phone_number': request.form['phone_number'].replace(' ', '')
    }
    new_user = User.add_user(data)
    session['user_id'] = new_user
    return redirect('/')


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
