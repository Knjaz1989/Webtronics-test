from flask import Flask
from flask_admin import Admin

from database.db_sync import db as db_sync, Session
from database.models import User, Post
from settings import config
from .views import UserModelView, PostModelView

flask_app = Flask(__name__)

# set optional bootswatch theme
flask_app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# set secret key
flask_app.config['SECRET_KEY'] = config.SECRET

admin = Admin(
    flask_app, name='Social', template_mode='bootstrap4', url='/'
)

admin.add_view(UserModelView(User, db_sync, name='Пользователи'))
admin.add_view(PostModelView(Post, db_sync, name='Посты'))
