from django.template.response import TemplateResponse

def index(request, template='testapp/index.html'):
    return TemplateResponse(request, template)
