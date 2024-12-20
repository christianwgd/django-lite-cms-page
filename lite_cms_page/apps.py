from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PageConfig(AppConfig):
    name = 'lite_cms_page'
    verbose_name = _('Pages')
