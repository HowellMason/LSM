from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.income import Income

# INCOMES

@app.route('/income/edit/<int:income_id>')
def edit_income(income_id):
    data = {
        'id': income_id
    }
    userinfo = {
        'id': session['user_id']
    }
    income = Income.get_by_id(data)
    user = User.get_with_id(userinfo)
    return render_template('edit-income.html', user = user, income = income)

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

@app.route('/income/edit-process', methods = ['POST'])
def edit_income_process():
    if not Income.validate_income(request.form):
        return redirect('/income/edit/' + str(request.form['id']))
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'amount': request.form['amount']
    }
    Income.edit_income(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/income/delete-process/<int:income_id>')
def delete_income(income_id):
    data = {
        'id': income_id
    }
    Income.delete_income(data)
    return redirect('/dashboard/' + str(session['user_id']))