from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_mptt_admin.admin import DjangoMpttAdmin

from lite_cms_page.models import Menu, Page


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ['name']
    search_fields = ['name']


@admin.register(Page)
class PageAdmin(DjangoMpttAdmin):

    list_display = ['title', 'url', 'site_link']
    list_display_links = ['title', 'site_link']
    ordering = ['title']
    use_context_menu = True
    autocomplete_fields = ['menus']

    fieldsets = (
        (_('Page'), {
            'fields': ('title', 'content', 'template'),
        }),
        (_('Link'), {
            'fields': ('url', 'ext'),
        }),
        (_('Menu'), {
            'fields': (
                'name', 'slug', 'menus',
                'parent', 'icon', 'nav_img',
                'breadcrumb_exclude',
                'login_required', 'static',
            ),
        }),
        (_('Status'), {
            'fields': ('status',),
        }),
    )

    @staticmethod
    @admin.display(description='')
    def site_link(obj):
        return mark_safe(
            f'<a href="{obj.get_absolute_url()}" target="blank">{_("View on site")}</a>'
        )
