from datetime import timedelta

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from database.db_sync import db as db_sync
from database.models import User, Post
from settings import config
from .handlers import Login
from .views import UserModelView, PostModelView, DashboardView

flask_app = Flask(__name__)

# set optional bootswatch theme
flask_app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# set secret key
flask_app.config['SECRET_KEY'] = config.SECRET
flask_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

flask_app.add_url_rule('/login',
                       view_func=Login.as_view('login'),
                       methods=["GET", "POST"])

#Implement admin
admin = Admin(
    flask_app, name='Social', template_mode='bootstrap4', url='/',
    index_view=DashboardView(
        name='Home',
        url='/'
    ),
)

admin.add_view(UserModelView(User, db_sync, name='Пользователи'))
admin.add_view(PostModelView(Post, db_sync, name='Посты'))

# Implement login
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        from database.models import User
        return db_sync.query(User).filter(User.id == user_id).first()
    except:
        return None
