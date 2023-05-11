from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.daily import Daily

@app.route('/daily-process', methods = ['POST'])
def add_daily(): 
    if not Daily.validate_daily(request.form):
        return redirect('/dashboard/' + str(session['user_id']))
    data = {
        'name': request.form['name'],
        'category': request.form['category'],
        'priority': request.form['priority'],
        'user_id': request.form['user_id']
    }
    Daily.add_daily(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/complete-daily-process/<int:daily_id>')
def complete_daily(daily_id):
    data = {
        'id': daily_id,
        'category': 'Complete'
    }
    Daily.complete_daily(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/revert-daily-process/<int:daily_id>')
def revert_daily(daily_id):
    data = {
        'id': daily_id,
        'category': 'Not Complete'
    }
    Daily.revert_daily(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/delete-daily-process/<int:daily_id>')
def delete_daily(daily_id):
    data = {
        'id': daily_id
    }
    Daily.delete_daily(data)
    return redirect('/dashboard/' + str(session['user_id']))