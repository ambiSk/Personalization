from urllib import response
from app import app
from flask import render_template, request, redirect, url_for, flash
import requests, ntpath, io
from base64 import b64encode
from selfie import ImageAPI

imageApi = ImageAPI()
genders = ['male', 'female']
def allowed_file(filename):
    return filename.endswith(('.png', '.jpg', '.jpeg'))

@app.route('/')
def homepage():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload():
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        gender = str(request.form.get('gender'))
        image = file.read()
        bufferReader = io.BufferedReader(io.BytesIO(image))
        
        image3d = imageApi(file.filename, bufferReader, gender)
        
        image = b64encode(image).decode("utf-8")

        return render_template('upload.html', image = image, threeDimage = image3d)


