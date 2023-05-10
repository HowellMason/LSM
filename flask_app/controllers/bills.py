from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.bill import Bill
from flask_app.controllers import dashboard

# BILLS

@app.route('/bill/edit/<int:bill_id>')
def edit_bill(bill_id):
    data = {
        'id': bill_id
    }
    userinfo = {
        'id': session['user_id']
    }
    bill = Bill.get_by_id(data)
    user = User.get_with_id(userinfo)
    return render_template('edit-bill.html', user = user, bill = bill)

@app.route('/bill-process', methods = ['POST'])
def add_bill_process():
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

@app.route('/bill/edit-process', methods = ['POST'])
def edit_bill_process():
    if not Bill.validate_bill(request.form):
        return redirect('/bill/edit/' + str(request.form['id']))
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'amount': request.form['amount'],
        'due_day': request.form['due_day']
    }
    Bill.edit_bill(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/bill/delete-process/<int:bill_id>')
def delete_bill(bill_id):
    data = {
        'id': bill_id
    }
    Bill.delete_bill(data)
    return redirect('/dashboard/' + str(session['user_id']))

