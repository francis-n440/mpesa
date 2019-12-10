from pdf-extractor import app
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')
