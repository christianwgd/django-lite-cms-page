import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-lite-cms-page',
    version='0.0.1',
    packages=setuptools.find_packages(
        exclude=["lite_cms_page_sample", "*manage.py"]
    ),
    include_package_data=True,
    package_data={
        "lite_cms_page": [
            "templates/lite_cms_page/*.html",
            "templates/lite_cms_page/includes/*.html",
            "locale/*/LC_MESSAGES/*",
        ],
    },
    description='CMS page classes for django-lite-cms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Christian Wiegand',
    license='MIT',
    url='https://github.com/christianwgd/django-lite-cms-page',
    keywords=['django', 'bootstrap', 'cms'],
    install_requires=[
        'django',
        'django-mptt',
        'django-mptt-admin',
        'django-bootstrap5',
        'django-filebrowser-no-grappelli',
        'django-tinymce',
        'django-lite-cms-core',
        'Pillow',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
