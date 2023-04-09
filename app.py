from flask import Flask
from config import Configuration

from employee.blueprint import employee

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(employee, url_prefix='/employee')