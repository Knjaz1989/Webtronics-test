from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="apps/site/templates/")


def render_template(
    template_name: str,
    request,
    context: dict,
    locale: str = 'en'
):
    context.update({"request": request, "locale": locale})
    return templates.TemplateResponse(template_name, context)
