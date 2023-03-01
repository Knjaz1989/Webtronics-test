from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


def get_main_page(request):
    return templates.TemplateResponse('main.html', {'request': request})