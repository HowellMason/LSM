from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.bill import Bill
from flask_app.models.income import Income
from flask_app.controllers import bill
from flask_app.controllers import income
from flask import flash
from flask import jsonify
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# HOME PAGE / DASHBOARD

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    data = {
        'id': user_id
    }
    user = User.get_with_id(data)
    bills = Bill.bills_for_one(data)
    incomes = Income.incomes_for_one(data)
    return render_template('dashboard.html', user = user, bills = bills, incomes = incomes)

@app.route('/terms')
def terms_page():
    return render_template('terms.html')

@app.route('/privacy')
def privary_page():
    return render_template('privacy.html')


# PROCESSES

@app.route('/test-route')
def test():
    if 'user_id' in session:
        return redirect('/dashboard/' + str(session['user_id']))
    else:
        flash("You must be logged in to visit your dashboard")
        return redirect('/login')
