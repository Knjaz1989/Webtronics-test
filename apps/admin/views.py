from flask_admin.contrib.sqla import ModelView

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
