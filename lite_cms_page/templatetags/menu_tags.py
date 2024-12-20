from django import template
from lite_cms_page.models import Page

register = template.Library()


@register.simple_tag(takes_context=True)
def menu(context, slug, template_name):
    request = context['request']
    pages = Page.objects.published(request.user).filter(menus__slug=slug)
    tpl = template.loader.get_template(template_name)
    return tpl.render({
        'request': context['request'],
        'pages': pages,
        'path': request.path
    })


@register.simple_tag(takes_context=True)
def submenu(context, page, template_name):
    request = context['request']
    pages = Page.get_children(page)
    tpl = template.loader.get_template(template_name)
    return tpl.render({
        'request': context['request'],
        'pages': pages,
        'path': request.path
    })
