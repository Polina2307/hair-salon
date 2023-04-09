from flask import Blueprint
from flask import render_template

employee = Blueprint('employee', __name__, template_folder='templates')  # Экземпляр класса


@employee.route('/')
def index():
    return render_template()
