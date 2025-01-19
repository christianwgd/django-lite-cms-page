from modeltranslation.translator import register

from lite_cms_core.translation import TranslatedContentFieldMixin
from lite_cms_page.models import Page


@register(Page)
class TranslatedPage(TranslatedContentFieldMixin):
    fields = ('name', )
