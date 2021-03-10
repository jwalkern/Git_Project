import random
from flask import Blueprint, render_template, flash
from iotrace import db
from iotrace.models import Device, Dummydata
from iotrace.main.forms import GenerateDummyData

main = Blueprint('main', __name__)

#Dette er vores startside og viser index.html 
@main.route('/')
@main.route(('/home'))
def home():    
    return render_template('home.html')

def random_generate():
    pos = str(round(random.uniform(-180,180),6))+','+ str(round(random.uniform(-90,90),6))
    temp = round(random.uniform(1500,3000))
    humid = round(random.uniform(35000,65000))
    hpa = round(random.uniform(10000000,20000000))
    volt = round(random.uniform(15000,65000))
    lte_rssi = round(random.uniform(-100,0))
    return pos, temp, humid, hpa, volt, lte_rssi

@main.route('/generate/data', methods=['GET', 'POST'])
def dummy():
    device = Device.query.all()
    form = GenerateDummyData()
    if form.validate_on_submit():
        for item in range(len(device)):
            pos, temp, humid, hpa, volt, lte_rssi = random_generate()
            data = Dummydata(pos=pos, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi, device_id=(item+1))
            db.session.add(data)
        db.session.commit()
        flash('Data generated!', 'success')  
    return render_template('dummy_data.html', title='GDD', form=form) 

