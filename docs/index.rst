django-lite-cms-page
====================

.. toctree::
    :maxdepth: 4

.. warning::
    The docs is work in progress, so it is not completed by now and will
    be subject to change.

**django-lite-page** adds hierarchical pagees to **django-lite-cms**..


Installation
------------

``django-lite-cms-page`` can be found on pypi. Run::

    pip install django-lite-cms-page

to install the package on your machine or in your virtual environment.


Dependencies
------------

If you install ``django-lite-cms-page`` the following modules will be
installed, because ``django-lite-cms-page`` depends on them:

- django-lite-cms-core
    The base classes for **django-lite-cms**.

- django-mptt
    Provides the tree functionality for the hierarchical pages.

- django-mptt-admin
    django-tinymce provides the HTML field for the ``ContentFieldMixin``.


Settings
--------

tbd


Getting Started
---------------

To integrate ``django-lite-cms-page`` with your site, follow the steps as listed:

1.  Add this application in the ``INSTALLED_APPS`` portion of your settings
    file. Your settings file will look something like::

        INSTALLED_APPS = (
            # ...
            'lite_cms_core,
            'lite_cms_page',
        )

2.  Add the lite_cms_page urls to the end of your root urlconf. Your urlconf
    will look something like::

        urlpatterns = [
            # ...
            path('lite_cms_page/', include('lite_cms_page.urls')),
        ]

Model Classes
-------------

.. automodule:: lite_cms_page.models
    :members:

Views
-----

.. automodule:: lite_cms_page.views
    :members:

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`