import os
import sys

from setuptools import setup, find_packages


version = '0.1'

requires = (
    'nextgisweb',
    'celery>=4.0',
    'redis',
)

entry_points = {
    'nextgisweb.packages': [
        'nextgisweb_celery = nextgisweb_celery:pkginfo',
    ],
}

setup(
    name='nextgisweb_celery',
    version=version,
    description="",
    long_description="",
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points=entry_points,
)
