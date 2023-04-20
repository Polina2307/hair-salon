from flask import Blueprint
from flask import render_template

from data import db_session
from data.profile import Profile
from .forms import ProfileForm

profile = Blueprint('profile', __name__, template_folder='templates')  # Экземпляр класса


@profile.route('/create', methods=['post', 'get'])
def create_profile():
    form = ProfileForm()
    return render_template('profile/create_profile.html', form=form)


@profile.route('/')
def index():
    db_sess = db_session.create_session()
    # profiles = db_sess.query(Profile).all()
    return render_template('profile/index.html')
