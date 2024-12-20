# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from filebrowser.fields import FileBrowseField
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from lite_cms_core.models import BaseEntity, ContentFieldMixin, SluggedMixin
from lite_cms_core.managers import BaseEntityManager
from lite_cms_page.fields import URLOrRelativeURLField


def wrapped_manager(klass):

    class Mgr(BaseEntityManager, klass):
        pass

    return Mgr()


class Menu(SluggedMixin, models.Model):
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')

    def __str__(self):
        return self.name

    def get_slug(self, attr=None):
        return super().get_slug(attr='name')

    name = models.CharField(max_length=50, verbose_name=_('Menu'))


class Page(MPTTModel, ContentFieldMixin, SluggedMixin, BaseEntity):
    """
    A html page.
    """

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return self.name

    """
    In addition to the title field, a page has a name 
    which designates the menu entry text. 
    """
    name = models.CharField(
        max_length=50, verbose_name=_('name'),
        help_text=_('Name of menu item.'), blank=True
    )
    #: The menu text can have an icon, None if not needed
    icon = models.CharField(
        max_length=50, verbose_name=_("icon"),
        null=True, blank=True
    )
    #: ManyToMany field to specify in which menus the page should be displayed
    menus = models.ManyToManyField(
        Menu, verbose_name=_("Menus"), blank=True
    )
    """
    The url attrbute can hold a URL to any page, either external as 
    a normal ``https://`` URL or as a local url pointing to any path 
    in the app. In this case the url must start with a ``/``.
    If this is a page from some app model, the URL is fetched from 
    ``get_absolute_url()`` and this field should be None. 
    """
    url = URLOrRelativeURLField(
        verbose_name=_('URL'),
        null=True, blank=True
    )
    """
    The ``ext`` attribute specifies if the page should be opened in 
    a new window (True). 
    Be aware that opening a new window is not recommended by the  
    Web Accessibility rules! (https://www.w3.org/TR/WCAG20-TECHS/G200.html)
    """
    ext = models.BooleanField(
        default=False, verbose_name=_('Open in new window')
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )
    static = models.BooleanField(
        default=False, verbose_name=_('Static Element'),
        help_text=_('Element ist for navigation only, no link if selected.')
    )
    nav_img = FileBrowseField(
        max_length=200, directory='navimg/', extensions=['.png', '.jpg'],
        verbose_name=_('menu image'), blank=True, null=True,
    )
    template = models.CharField(
        verbose_name=_("Template"), max_length=50,
        null=True, blank=True
    )
    login_required = models.BooleanField(
        verbose_name=_('Login required'), default=False,
        help_text=_('If checked, only logged in users can view this page')
    )
    breadcrumb_exclude = models.BooleanField(
        verbose_name=_('Exclude from Breadcrumbs'), default=False,
        help_text=_('Will be excluded from Breadcumbs, if checked')
    )

    search_fields = {"title", "content"}

    objects = wrapped_manager(TreeManager)

    def allowed(self, user):
        return user.is_authenticated if self.login_required else not self.login_required

    def save(self, *args, **kwargs):
        if self.title and not self.name:
            self.name = self.title
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.url:
            return self.url
        if self.static:
            return reverse('home')
        return reverse('lite_cms_page:page-view', args=[str(self.slug)])
