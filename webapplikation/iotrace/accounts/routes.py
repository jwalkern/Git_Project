from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from iotrace import db, bcrypt
from iotrace.models import User, Device
from iotrace.accounts.forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from iotrace.accounts.utils import save_picture, send_reset_email




accounts = Blueprint('accounts', __name__)


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('devices.curl_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('devices.curl_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('accounts/login.html', title='Login', form=form)

@accounts.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('devices.curl_dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('accounts.login'))
    return render_template('accounts/register.html', title='Register', form=form)

@accounts.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('accounts.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email        
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    devices = Device.query.filter_by(user_id=current_user.id)
    return render_template('accounts/account.html', title='Account', image_file=image_file, devices=devices, form=form)

@accounts.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('devices.curl_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email have been sent with instruction to reset your password', 'info')
        return redirect(url_for('accounts.login'))
    return render_template('accounts/reset_request.html', title='Reset Password', form=form)

@accounts.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('devices.curl_dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('accounts.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       user.password = hashed_password
       db.session.commit()
       flash('Your password has now been updated! You can now log in.', 'success')
       return redirect(url_for('accounts.login'))
    return render_template('accounts/reset_token.html', title='Reset Password', form=form)