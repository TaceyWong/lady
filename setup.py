#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'html2text>=2020.1.16',
'Jinja2>=3.0.2']

test_requirements = ['pytest>=3', ]

setup(
    author="Tacey Wong",
    author_email='xinyong.w@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package that generates clean, responsive HTML e-mails for sending transactional mail",
    entry_points={
        'console_scripts': [
            'lady=lady.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lady',
    name='lady',
    packages=find_packages(include=['lady', 'lady.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/TaceyWong/lady',
    version='0.1.0',
    zip_safe=False,
)
