from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.bill import Bill
from flask_app.models.income import Income
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


# PROCESSES

@app.route('/test-route')
def test():
    if 'user_id' in session:
        return redirect('/dashboard/' + str(session['user_id']))
    else:
        flash("You must be logged in to visit your dashboard")
        return redirect('/login')

@app.route('/bill-process', methods = ['POST'])
def add_bill():
    if not Bill.validate_bill(request.form):
        return redirect('/dashboard/' + str(session['user_id']))
    data = {
        'name': request.form['name'],
        'amount': request.form['amount'],
        'due_day': request.form['due_day'],
        'user_id': request.form['user_id']
    }
    print(data)
    Bill.add_bill(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/income-process', methods = ['POST'])
def add_income():
    if not Income.validate_income(request.form):
        return redirect('/dashboard/' + str(session['user_id']))
    data = {
        'name': request.form['name'],
        'amount': request.form['amount'],
        'user_id': request.form['user_id']
    }
    print(data)
    Income.add_income(data)
    return redirect('/dashboard/' + str(session['user_id']))