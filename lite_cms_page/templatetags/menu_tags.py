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


@register.simple_tag(takes_context=True)
def get_active(context, page):
    request = context['request']
    if page.slug in request.path:
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def get_active_parent(context, page):
    request = context['request']
    for pg in page.get_children():
        if pg.slug in request.path:
            return 'active'
    return ''


@register.inclusion_tag('lite_cms_page/includes/lang_flag.html')
def lang_flag(lang_code):
    img_url = f'/static/img/flags/{lang_code}.png'
    return { 'img_url': img_url, 'lang_code': lang_code }
