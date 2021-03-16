import os
import io
import base64
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from iotrace import googlemaps
from flask_googlemaps import Map
from iotrace.models import Device, TrackingDeviceData 

plots = Blueprint('plots', __name__)

def device_temp(data_trackingdevice):
	time = []
	temp = []
	for item in data_trackingdevice:
		time.append(item.timestamp.strftime('%d-%m-%Y'))
		temp.append(item.temp)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Temperatur")
	axis.set_ylabel("Temperatur")
	axis.plot(time, temp)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_humid(data_trackingdevice):
	time = []
	humid = []
	# Fetching data
	for item in data_trackingdevice:
		time.append(item.timestamp.strftime('%d-%m-%Y'))
		humid.append(item.humid)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Humidity")
	axis.set_ylabel("Humidity")
	axis.plot(time, humid)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_hpa(data_trackingdevice):
	time = []
	hpa = []
	# Fetching data
	for item in data_trackingdevice:
		time.append(item.timestamp.strftime('%d-%m-%Y'))
		hpa.append(item.hpa)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Air pressure")
	axis.set_ylabel("hPa")
	axis.plot(time, hpa)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_volt(data_trackingdevice):
	time = []
	volt = []
	# Fetching data
	for item in data_trackingdevice:
		time.append(item.timestamp.strftime('%d-%m-%Y'))
		volt.append(item.volt)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Voltage")
	axis.set_ylabel("Voltage")
	axis.plot(time, volt)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG


def device_lte_rssi(data_trackingdevice):
	time = []
	lte_rssi = []
	# Fetching data
	for item in data_trackingdevice:
		time.append(item.timestamp.strftime('%d-%m-%Y'))
		lte_rssi.append(item.lte_rssi)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Signal Strength")
	axis.set_ylabel("LTE RSSI")
	axis.plot(time, lte_rssi)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_pos(data_trackingdevice):
	
	GOOGLEMAPS_KEY =  os.environ.get('GOOGLEMAPS_KEY')	
	return GOOGLEMAPS_KEY


def all_device_pos(devices):
	device_pos = []
	for device in devices:
		try:
			lng, lat = device.data_trackingdevice[-1].pos.split(',')
			label = device.devicename
			device_pos.append([lng, lat, label])
		except:
			pass

	GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')
	return device_pos, GOOGLEMAPS_KEY




@plots.route('/plots/plot/<int:device_id>', methods=['GET'])
@login_required
def plot1(device_id):
	device = Device.query.get_or_404(device_id)
	if device.owner != current_user:
		abort(403)
	
	temp = device_temp(device.data_trackingdevice)
	humid = device_humid(device.data_trackingdevice)
	hpa = device_hpa(device.data_trackingdevice)
	volt = device_volt(device.data_trackingdevice)
	lte_rssi = device_lte_rssi(device.data_trackingdevice)
	pos = device_pos(device.data_trackingdevice)


	return render_template('plots/plot1.html', temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi, pos=pos)


@plots.route('/map')
@login_required
def mapTest():
	devices = Device.query.filter_by(user_id=current_user.id)
	test, GOOGLEMAPS_KEY = all_device_pos(devices)	
	return render_template('plots/maptest.html', GOOGLEMAPS_KEY=GOOGLEMAPS_KEY, test=test)

@plots.route('/plots/map/<int:device_id>')
@login_required
def mapview(device_id):
	device = Device.query.get_or_404(device_id)
	if device.owner != current_user:
		abort(403)
	pos , GOOGLEMAPS_KEY = device_pos(device.data_trackingdevice)


	return render_template('plots/map.html', GOOGLEMAPS_KEY=GOOGLEMAPS_KEY, pos=pos)