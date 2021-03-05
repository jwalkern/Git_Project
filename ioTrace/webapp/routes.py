import os
import secrets
import random
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from webapp import app, db, bcrypt
from webapp.forms import LoginForm, RegistrationForm, UpdateAccountForm, CreateDeviceForm, GenerateDummyData
from webapp.models import User, Device, Dummydata
from flask_login import login_user, logout_user, current_user, login_required

#Dette er vores startside og viser index.html 
@app.route('/')
@app.route(('/home'))
def home():    
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    devices = Device.query.all()
    data = Dummydata.query.all()     
    return render_template('dashboard.html', title='Dashboard', devices=devices, data=data)

@app.route('/dashboard/device/<int:device_id>')
@login_required
def device(device_id):
    device = Device.query.get_or_404(device_id)
    return render_template('device.html', title=device.devicename, device=device)

@app.route('/dashboard/device/<int:device_id>/update', methods=['GET', 'POST'])
@login_required
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    form = CreateDeviceForm()
    if form.validate_on_submit():
        device.devicename = form.devicename.data
        device.devicetype = form.devicetype.data
        db.session.commit()
        flash('Your device has been updated', 'success')
        return redirect(url_for('device', device_id=device.id))
    elif request.method == 'GET':
        form.devicename.data = device.devicename
        form.devicetype.data = device.devicetype
    return render_template('edit_device.html', title='Update Device', form=form, legend='Update device')
 
@app.route('/dashboard/device/<int:device_id>/delete', methods=['POST'])
@login_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    db.session.delete(device)
    db.session.commit()
    flash('Your device has been deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard/device/new', methods=['GET', 'POST'])
@login_required
def add_device():
    form = CreateDeviceForm()
    if form.validate_on_submit():
        device = Device(devicename=form.devicename.data, devicetype=form.devicetype.data, owner=current_user)
        db.session.add(device)
        db.session.commit()
        flash('The device have been added!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_device.html', title='Add Device', form=form, legend='Add device')

def random_generate():
    pos = str(round(random.uniform(-180,180),6))+','+ str(round(random.uniform(-90,90),6))
    temp = round(random.uniform(1500,3000))
    humid = round(random.uniform(35000,65000))
    hpa = round(random.uniform(10000000,20000000))
    volt = round(random.uniform(15000,65000))
    lte_rssi = round(random.uniform(-100,0))
    return pos, temp, humid, hpa, volt, lte_rssi

@app.route('/generate/data', methods=['GET', 'POST'])
def dummy():
    form = GenerateDummyData()
    if form.validate_on_submit():
        device_id = Device.query.filter_by(id=form.device_uid.data).first()
        if device_id:
            pos, temp, humid, hpa, volt, lte_rssi = random_generate()
            generateddummydata = Dummydata(pos=pos, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi, device_id=form.device_uid.data )
            db.session.add(generateddummydata)
            db.session.commit()
            flash('Dummy Data Generated!', 'success')
            
    return render_template('dummy_data.html', title='GDD', form=form)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pics', picture_fn)    
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)    
    i.save(picture_path)
    
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email        
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
    