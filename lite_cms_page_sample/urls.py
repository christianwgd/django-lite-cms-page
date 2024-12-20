"""wgdnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from filebrowser.sites import site

from lite_cms_page_sample import views


urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),

    path('', views.index, name='home'),

    path('lite_cms_core/', include('lite_cms_core.urls')),
    path('lite_cms_page/', include('lite_cms_page.urls')),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
