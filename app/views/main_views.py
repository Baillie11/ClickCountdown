# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask import Blueprint, redirect, render_template, request, url_for, current_app, flash
from flask_user import current_user, login_required, roles_required
import stripe
from datetime import datetime

from app import db
from app.models.user_models import UserProfileForm
from app.forms.countdown_forms import CountdownForm
from app.models.countdown_models import Countdown

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users
@main_blueprint.route('/member')
@login_required
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    form = UserProfileForm(request.form, obj=current_user)

    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('main.home_page'))

    return render_template('main/user_profile_page.html', form=form)


@main_blueprint.route('/subscribe')
@login_required
def subscribe():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Premium Membership'},
                'unit_amount': 1000,
                'recurring': {'interval': 'month'},
            },
            'quantity': 1,
        }],
        success_url=url_for('main.subscription_success', _external=True),
        cancel_url=url_for('main.subscription_cancelled', _external=True),
    )

    return redirect(session.url, code=303)


@main_blueprint.route('/subscription-success')
@login_required
def subscription_success():
    return render_template('main/subscription_success.html')


@main_blueprint.route('/subscription-cancelled')
@login_required
def subscription_cancelled():
    return render_template('main/subscription_cancelled.html')


# Create a new countdown
@main_blueprint.route('/countdown/new', methods=['GET', 'POST'])
@login_required
def create_countdown():
    form = CountdownForm()

    if form.validate_on_submit():
        countdown = Countdown(
            title=form.title.data,
            target_datetime=form.target_datetime.data,
            is_public=form.is_public.data,
            user_id=current_user.id
        )
        db.session.add(countdown)
        db.session.commit()

        flash('Countdown created successfully!', 'success')
        return redirect(url_for('main.view_countdowns'))

    return render_template('countdown/create_countdown.html', form=form)


# View all user's countdowns
@main_blueprint.route('/countdowns')
@login_required
def view_countdowns():
    countdowns = Countdown.query.filter_by(user_id=current_user.id).all()
    return render_template('countdown/view_countdowns.html', countdowns=countdowns, current_time=datetime.utcnow())
