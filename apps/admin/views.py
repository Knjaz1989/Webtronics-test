from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_exclude_list = ['hashed_password', ]
    can_create = False
    page_size = 50
