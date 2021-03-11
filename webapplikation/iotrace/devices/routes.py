from flask import Blueprint, render_template, redirect, request, abort, flash, url_for
from flask_login import login_required, current_user
from iotrace import db
from iotrace.models import Device, Dummydata
from iotrace.devices.forms import CreateDeviceForm
from iotrace.plots.plot import device_temp, device_humid, device_hpa, device_volt, device_lte_rssi

devices = Blueprint('devices', __name__)

@devices.route('/dashboard')
@login_required
def dashboard():
    devices = Device.query.filter_by(user_id=current_user.id)    
    data = Dummydata.query.filter_by()
    test = current_user.devices
    return render_template('dashboard.html', title='Dashboard', devices=devices, data=data, test=test)


@devices.route('/dashboard/device/data/<device_id>')
@login_required
def device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    temp = device_temp(device.datadumps)
    humid = device_humid(device.datadumps)
    hpa = device_hpa(device.datadumps)
    volt = device_volt(device.datadumps)
    lte_rssi = device_lte_rssi(device.datadumps)   
    return render_template('device.html', title=device.devicename, device=device, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi)

@devices.route('/dashboard/device/update/<device_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('devices.device', device_id=device.id))
    elif request.method == 'GET':
        form.devicename.data = device.devicename
        form.devicetype.data = device.devicetype
    return render_template('edit_device.html', title='Update Device', form=form, legend='Update device')
 
@devices.route('/dashboard/device/delete/<device_id>', methods=['POST'])
@login_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    db.session.delete(device)
    db.session.commit()
    flash('Your device has been deleted!', 'success')
    return redirect(url_for('devices.dashboard'))

@devices.route('/dashboard/device/new', methods=['GET', 'POST'])
@login_required
def add_device():
    form = CreateDeviceForm()
    if form.validate_on_submit():
        device = Device(devicename=form.devicename.data, devicetype=form.devicetype.data, owner=current_user)
        db.session.add(device)
        db.session.commit()
        flash('The device have been added!', 'success')
        return redirect(url_for('devices.dashboard'))
    return render_template('edit_device.html', title='Add Device', form=form, legend='Add device')

