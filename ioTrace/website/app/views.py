# -*- coding: utf-8 -*-

from flask import render_template
from app import app


#Dette er vores startside og viser index.html 
@app.route('/')
def index():
    
    return render_template('index.html')

