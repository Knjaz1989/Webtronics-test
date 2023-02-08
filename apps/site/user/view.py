from apps.site.utils.jinja2_render import render_template


def get_main_page(request):
    return render_template("main.html", request, {})


def get_login_page(request):
    return render_template("login.html", request, {})
