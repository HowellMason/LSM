from flask_app import app
from flask import redirect, request, session
from flask_app.models.weekly import Weekly

@app.route('/weekly-process', methods = ['POST'])
def add_weekly(): 
    if not Weekly.validate_weekly(request.form):
        return redirect('/dashboard/' + str(session['user_id']))
    data = {
        'name': request.form['name'],
        'category': request.form['category'],
        'priority': request.form['priority'],
        'user_id': request.form['user_id']
    }
    Weekly.add_weekly(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/complete-weekly-process/<int:weekly_id>')
def complete_weekly(weekly_id):
    data = {
        'id': weekly_id,
        'category': 'Complete'
    }
    Weekly.complete_weekly(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/revert-weekly-process/<int:weekly_id>')
def revert_weekly(weekly_id):
    data = {
        'id': weekly_id,
        'category': 'Not Complete'
    }
    Weekly.revert_weekly(data)
    return redirect('/dashboard/' + str(session['user_id']))

@app.route('/delete-weekly-process/<int:weekly_id>')
def delete_weekly(weekly_id):
    data = {
        'id': weekly_id
    }
    Weekly.delete_weekly(data)
    return redirect('/dashboard/' + str(session['user_id']))