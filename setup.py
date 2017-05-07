"""Packaging settings."""
import codecs
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

__version__ = '0.5.5'

with codecs.open(join(abspath(dirname(__file__)), 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='Maya Signature Scraper',
    version=__version__,
    description='A command line program to systematically scrape command signatures for maya in Python.',
    long_description=long_description,
    url='https://github.com/andresmweber/mayasig-cli.git',
    author='Andres Weber',
    author_email='andresmweber@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['redis', 'bs4', 'requests', 'six'],
    extras_require={
        'test': ['coverage', 'nose', 'tox', 'virtualenv', 'travis', 'python-coveralls'],
        'dev': ['twine', 'virtualenv', 'Sphinx', 'docutils', 'docopt']
    },
    entry_points={
        'console_scripts': [
            'mayasig=maya_signatures.cli:main',
        ],
    },
    cmdclass={'test': 'tox'},
)
