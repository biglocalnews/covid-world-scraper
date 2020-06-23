#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'bs4',
    'click',
    'pandas',
    'requests',
    'retrying',
    'selenium',
    'xlrd',
]

test_requirements = [
    'flake8',
    'pytest',
#    'vcrpy',
#    'pytest-vcr'
]

setup(
    name='covid-world-scrapers',
    version='0.1.0',
    description="Command-line tool for scraping COVID-19 data from countries around the world.",
    long_description=__doc__,
    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',
    url='https://github.com/biglocalnews/covid-world-scrapers',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        covid-world-scraper=covid_world_scraper.cli:cli
    ''',
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
