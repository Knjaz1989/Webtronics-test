from flask import render_template, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_required, login_user

from database.models import User


class Login(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        user: User = User.check_user(
            email=request.form.get('email'),
            password=request.form.get('password')
        )
        if not user or user.is_admin is not True:
            flash(message="Wrong login or password",
                  category='login_message')
            return redirect(url_for('login'))
        login_user(user)
        return redirect('/admin')
