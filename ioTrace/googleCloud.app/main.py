import os
from flask import Flask, render_template, request, jsonify
from db import get_device, add_device
from forms import CreateDeviceForm



db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd70f607b41a89d8c815357cb3dcfc614'

#Dette er vores startside og viser index.html 
@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/create')
def create():
    form = CreateDeviceForm()       
    return render_template('create.html', title='Add Deivce', form=form)

@app.route('/read')
def read():    
    return render_template('read.html', title='read')

@app.route('/update')
def update():    
    return render_template('update.html', title='update')

@app.route('/delete')
def delete():    
    return render_template('delete.html', title='delete')


#Below this comment is all the API commands


@app.route('/api/read', methods=['GET'])
def api_read():
    return get_device()


@app.route('/api/create', methods=['POST'])
def api_create():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        add_device(request.get_json())
        return 'Device Added'

    return get_device()



if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)