import pytest
from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.template import Context
from django.test import TestCase, RequestFactory
from django.urls import reverse
from faker import Faker

from lite_cms_page.models import Menu, Page
from lite_cms_page.templatetags import menu_tags
from lite_cms_page.validators import url_or_relative_url_validator

User = auth.get_user_model()


class PageModelTest(TestCase):

    def setUp(self):
        fake = Faker('de_DE')
        Faker.seed(0)
        self.page = Page.objects.create(
            title=' '.join(fake.words()),
            content=' '.join(fake.paragraphs(nb=5)),
        )
        self.page_url = Page.objects.create(
            title=' '.join(fake.words()),
            url=fake.uri(),
            ext=True
        )
        self.menu = Menu.objects.create(
            name=' '.join(fake.words()),
        )

    def test_page_str(self):
        self.assertEqual(str(self.page), self.page.title)

    def test_menu_str(self):
        self.assertEqual(str(self.menu), self.menu.name)

    def test_page_name_is_title(self):
        """ If no page name is provided it should be assigned to title """
        self.assertEqual(self.page.name, self.page.title)

    def test_page_get_absolute_url(self):
        self.assertEqual(
            self.page.get_absolute_url(),
            reverse('lite_cms_page:page-view', kwargs={'slug': self.page.slug})
        )

    def test_page_get_absolute_url_ext(self):
        self.assertEqual(
            self.page.get_absolute_url(),
            reverse('lite_cms_page:page-view', kwargs={'slug': self.page.slug})
        )

    def test_page_get_absolute_url_page_has_url(self):
        self.assertEqual(
            self.page_url.get_absolute_url(),
            self.page_url.url
        )

    def test_page_get_absolute_url_page_static(self):
        self.page.static = True
        self.page.url = None
        self.page.save()
        self.page.refresh_from_db()
        self.assertEqual(
            self.page.get_absolute_url(),
            reverse('home')
        )


class PageViewTest(TestCase):

    def setUp(self):
        fake = Faker('de_DE')
        Faker.seed(0)
        self.page = Page.objects.create(
            title=' '.join(fake.words()),
            content=' '.join(fake.paragraphs(nb=5)),
        )

    def test_page_detail(self):
        url = reverse('lite_cms_page:page-view', kwargs={'slug': self.page.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['page'], Page)


class PageTagTest(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        Faker.seed(0)
        self.user = User.objects.create(
            username='myadmin',
            is_superuser=True
        )

        self.factory = RequestFactory()
        self.context = Context()
        request = self.factory.get('/any/path/really/')
        request.user = self.user
        self.context['request'] = request

        self.menu = Menu.objects.create(
            name='Testmenu',
        )
        for _ in range(5):
            page = Page.objects.create(
                title=' '.join(self.fake.words()),
                content=' '.join(self.fake.paragraphs(nb=5)),
            )
            page.menus.add(self.menu)

    def test_menu(self):
        response = menu_tags.menu(
            self.context,
            'testmenu',
            'lite_cms_page/includes/bottom_menu.html'
        )
        for page in self.menu.page_set.all():
            self.assertInHTML(
                f'<a href="/lite_cms_page/{page.slug}/" class="" title="{page.title}">{page.title}</a>',
                response
            )

    def test_submenu(self):
        page_w_submenu = Page.objects.first()
        for _ in range(3):
            page = Page.objects.create(
                title=' '.join(self.fake.words()),
                content=' '.join(self.fake.paragraphs(nb=5)),
                parent=page_w_submenu
            )
            page.menus.add(self.menu)
        response = menu_tags.submenu(
            self.context,
            page_w_submenu,
            'lite_cms_page/includes/submenuright.html'
        )
        sub_pages = page_w_submenu.get_descendants(
            include_self=False
        )
        for page in sub_pages:
            self.assertInHTML(
                f'<a href="/lite_cms_page/{page.slug}/" aria-label="{page.name}">{page.title}</a>',
                response
            )


class FormWithUrlOrRelativeUrlField(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'url')


class UrlOrRelativeUrlFieldTest(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        Faker.seed(0)

    def test_field_validator_local_url_valid(self):
        valid_local_url = f'/{self.fake.uri_path()}'
        self.assertIsNone(url_or_relative_url_validator(valid_local_url))

    def test_field_validator_local_url_invalid(self):
        invalid_url = self.fake.word()
        with pytest.raises(ValidationError):
            url_or_relative_url_validator(invalid_url)

    def test_field_validator_http_url_valid(self):
        self.valid_url = f'/{self.fake.url(schemes=["http"])}'
        self.assertIsNone(url_or_relative_url_validator(self.valid_url))

    def test_field_validator_https_url_valid(self):
        valid_url = f'/{self.fake.url(schemes=["https"])}'
        self.assertIsNone(url_or_relative_url_validator(valid_url))

    def test_field_validator_url_invalid(self):
        invalid_url = self.fake.word()
        with pytest.raises(ValidationError):
            url_or_relative_url_validator(invalid_url)

    def test_form_url_valid(self):
        form_data = {
            'title': self.fake.word(),
            'url': f'/{self.fake.url(schemes=["https"])}',
        }
        form = FormWithUrlOrRelativeUrlField(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_url_invalid(self):
        form_data = {
            'title': self.fake.word(),
            'url': self.fake.word(),
        }
        form = FormWithUrlOrRelativeUrlField(data=form_data)
        self.assertFalse(form.is_valid())
