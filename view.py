from app import app
from flask import render_template


@app.route('/')
def index():
    name = {'polina': 'Polina', 'vasilisa': 'Василиса'}
    return render_template('index.html', n=name)
