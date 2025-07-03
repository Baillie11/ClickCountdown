from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import mongo
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    events = mongo.db.events.find({'user_id': current_user.id})
    return render_template('dashboard.html', events=events)

@main.route('/add-event', methods=['GET', 'POST'])
@login_required
def add_event():
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

    return render_template('add_event.html')

@main.route('/edit-event/<event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = mongo.db.events.find_one({'_id': ObjectId(event_id), 'user_id': current_user.id})
    
    if not event:
        flash('Event not found.')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        if name and date:
            mongo.db.events.update_one(
                {'_id': ObjectId(event_id), 'user_id': current_user.id},
                {'$set': {'name': name, 'date': date}}
            )
            flash('Event updated successfully!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Please fill in all fields.')
    
    return render_template('edit_event.html', event=event)

@main.route('/delete_event/<event_id>')
@login_required
def delete_event(event_id):
    mongo.db.events.delete_one({'_id': ObjectId(event_id), 'user_id': current_user.id})
    return redirect(url_for('main.dashboard')) 