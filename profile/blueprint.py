from flask import Blueprint
from flask import render_template

from data import db_session
from data.profile import Profile

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/')
def index():
    db_sess = db_session.create_session()
    profiles = db_sess.query(Profile).all()
    return render_template('profile/index.html', obj=profiles)
