from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterLike, FilterEqual
from wtforms.validators import DataRequired

from apps.main_helpers import get_hash_password


class UserModelView(ModelView):

    # Change getting password to hash
    def on_model_change(self, form, model, is_created):
        model.hashed_password = get_hash_password(model.hashed_password)
        model.email = model.email.lower()

    # Don't show user password in Admin panel
    column_exclude_list = ['hashed_password', ]
    # Allow or forbid to create user
    # can_create = False
    # Max rows on page
    page_size = 50


class PostModelView(ModelView):

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
        'title', 'content', 'user.name', 'user.email', 'like_count',
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
    # can_create = False
    # Max rows on page
    page_size = 50
