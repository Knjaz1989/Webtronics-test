from flask import Flask
from flask_admin import Admin

from database.db_sync import db
from database.models import User
from .views import UserModelView

flask_app = Flask(__name__)

# set optional bootswatch theme
flask_app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(
    flask_app, name='Social', template_mode='bootstrap4', url='/'
)

admin.add_view(UserModelView(User, db))
