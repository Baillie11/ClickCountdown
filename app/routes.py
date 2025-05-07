from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import mongo
from datetime import datetime
from bson.objectid import ObjectId

main = Blueprint('main', __name__)  # ✅ This defines 'main'

@main.route('/')
def home():
    return redirect(url_for('auth.login'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        if name and date:
            mongo.db.events.insert_one({
                'user_id': current_user.id,
                'name': name,
                'date': date
            })
        return redirect(url_for('main.dashboard'))

    events = mongo.db.events.find({'user_id': current_user.id})
    return render_template('dashboard.html', events=events)

@main.route('/delete_event/<event_id>')
@login_required
def delete_event(event_id):
    mongo.db.events.delete_one({'_id': ObjectId(event_id), 'user_id': current_user.id})
    return redirect(url_for('main.dashboard'))
