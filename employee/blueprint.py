from flask import Blueprint
from flask import render_template

from data import db_session
# from data.profile import Profile

employee = Blueprint('employee', __name__, template_folder='templates')  # Экземпляр класса


@employee.route('/')
def index():
    db_sess = db_session.create_session()
    # profiles = db_sess.query(Profile).all()
    return render_template('employee/index.html')
