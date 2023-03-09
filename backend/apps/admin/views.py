from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterLike, FilterEqual
from flask_login import current_user
from wtforms.validators import DataRequired

from apps.main_helpers import get_hash_password


class DashboardView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class UserModelView(ModelView):

    # Don't show user password in Admin panel
    column_exclude_list = ['hashed_password', ]
    # Allow or forbid to create user
    can_create = False
    # Max rows on page
    page_size = 50

    # Change getting password to hash
    def on_model_change(self, form, model, is_created):
        model.hashed_password = get_hash_password(model.hashed_password)
        model.email = model.email.lower()

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class PostModelView(ModelView):

    # Change name of columns
    column_labels = {
        'title': 'Заголовок', 'content': 'Содержание', 'user': 'Владелец',
        'user.name': 'Имя владельца', 'user.email': 'Почта владельца',
        'like_count': 'Likes', 'dislike_count': 'Dislikes',
    }
    # Show current columns
    column_list = (
        'id', 'title', 'content', 'user.name', 'user.email', 'like_count',
        'dislike_count',
    )
    # Can sort columns
    column_sortable_list = (
        'id', 'title', 'content', 'user.name', 'user.email', 'like_count',
        'dislike_count',
    )
    # Search on title
    column_searchable_list = ('title',)
    # Add filters on columns
    column_filters = ('title', 'content', 'user.name', 'user.email')
    # form create
    form_args = {
        'title': dict(validators=[DataRequired()]),
        'content': dict(validators=[DataRequired()]),
        'user': dict(validators=[DataRequired()]),
    }
    # Allow or forbid to create post
    can_create = False
    # Max rows on page
    page_size = 50

    # Override for current filters
    def scaffold_filters(self, name):
        """
            Generate filter object for the given name

            :param name:
                Name of the field
        """
        filter_list = [
            FilterLike(name, name=self.column_labels.get(name, 'undefined')),
            FilterEqual(name, name=self.column_labels.get(name, 'undefined')),
        ]
        return filter_list

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
