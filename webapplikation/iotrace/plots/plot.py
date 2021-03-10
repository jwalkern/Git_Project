import io
import base64
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from iotrace import maps
from iotrace.models import Device, Dummydata 

plots = Blueprint('plots', __name__)

def device_temp(datadumps):
	time = []
	temp = []
	for item in datadumps:
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

def device_humid(datadumps):
	time = []
	humid = []
	# Fetching data
	for item in datadumps:
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

def device_hpa(datadumps):
	time = []
	hpa = []
	# Fetching data
	for item in datadumps:
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

def device_volt(datadumps):
	time = []
	volt = []
	# Fetching data
	for item in datadumps:
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


def device_lte_rssi(datadumps):
	time = []
	lte_rssi = []
	# Fetching data
	for item in datadumps:
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






@plots.route('/plots/plot/<int:device_id>', methods=['GET'])
@login_required
def plot1(device_id):
	device = Device.query.get_or_404(device_id)
	if device.owner != current_user:
		abort(403)
	
	temp = device_temp(device.datadumps)
	humid = device_humid(device.datadumps)
	hpa = device_hpa(device.datadumps)
	volt = device_volt(device.datadumps)
	lte_rssi = device_lte_rssi(device.datadumps)


	return render_template('plots/plot1.html', temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi)


