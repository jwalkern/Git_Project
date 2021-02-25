# -*- coding: utf-8 -*-

from flask import render_template
from app import app


#Dette er vores startside og viser index.html 
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/create')
def create():
    
    return render_template('create.html')

@app.route('/read')
def read():
    
    return render_template('read.html')

@app.route('/update')
def update():
    
    return render_template('update.html')

@app.route('/delete')
def delete():
    
    return render_template('delete.html')