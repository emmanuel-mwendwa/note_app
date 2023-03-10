from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import SignUpForm, LogInForm, ChangePasswordForm
from .. import db
from ..models import User
from ..email import send_email

@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(firstName=form.firstname.data, lastName=form.lastname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('Account created successfully. A confirmation link has been sent to you.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/sign_up.html', form=form)

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password', category='error')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated\
    and not current_user.confirmed\
    and request.blueprint != 'auth'\
    and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm/<token>', methods=["GET", "POST"])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link has expired or is invalid')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to your email.')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', category='success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid Password', category='error')
    return render_template('auth/change_password.html', form=form)