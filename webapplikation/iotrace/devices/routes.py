import os
from flask import Blueprint, render_template, redirect, request, abort, flash, url_for
from flask_login import login_required, current_user
from iotrace import db
from iotrace.models import Device, TrackingDeviceData
from iotrace.devices.forms import CreateDeviceForm
from iotrace.plots.plot import device_temp, device_humid, device_hpa, device_volt, device_lte_rssi, device_pos, all_device_pos, device_alarm1, device_alarm2

devices = Blueprint('devices', __name__)


@devices.route('/dashboard')
@login_required
def dashboard():
    devices = Device.query.filter_by(user_id=current_user.id)
    all_device, GOOGLEMAPS_KEY = all_device_pos(devices)
    return render_template('devices/dashboard.html',  title='Dashboard', devices=devices, GOOGLEMAPS_KEY=GOOGLEMAPS_KEY, all_device=all_device)


@devices.route('/dashboard/device/data/<device_id>')
@login_required
def device(device_id):
    device = Device.query.get_or_404(device_id)
    if current_user != device.owner:
        abort(403)
    if device.devicetype != 'fire':
        temp = device_temp(device.data_trackingdevice)
        humid = device_humid(device.data_trackingdevice)
        hpa = device_hpa(device.data_trackingdevice)
        volt = device_volt(device.data_trackingdevice)
        lte_rssi = device_lte_rssi(device.data_trackingdevice)
        pos, GOOGLEMAPS_KEY= device_pos(device.data_trackingdevice)
        return render_template('devices/device.html', title=device.devicename, device=device, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi, pos=pos, GOOGLEMAPS_KEY=GOOGLEMAPS_KEY)
    elif device.devicetype == 'fire':
        alarm_1 = device_alarm1(device.data_firedevice)
        alarm_2 = device_alarm2(device.data_firedevice)
        volt = device_volt(device.data_firedevice)
        lte_rssi = device_lte_rssi(device.data_firedevice)       
        return render_template('devices/device.html', title=device.devicename, device=device, alarm_1=alarm_1, alarm_2=alarm_2, volt=volt, lte_rssi=lte_rssi)

@devices.route('/dashboard/device/edit/<device_id>', methods=['GET', 'POST'])
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
    return render_template('devices/edit_device.html', title='Update Device', form=form, legend='Update device')
 
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
        device = Device(device_mac=form.device_mac.data ,devicename=form.devicename.data, devicetype=form.devicetype.data, owner=current_user)
        db.session.add(device)
        db.session.commit()
        flash('The device have been added!', 'success')
        return redirect(url_for('devices.dashboard'))
    return render_template('devices/add_device.html', title='Add Device', form=form)

