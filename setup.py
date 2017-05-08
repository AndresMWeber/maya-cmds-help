"""Packaging settings."""
import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from distutils.util import convert_path

__package__ = 'maya_signatures'

# from:
# http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
main_ns = {}
with open(convert_path('%s/version.py' % __package__)) as ver_file:
    exec(ver_file.read(), main_ns)

with codecs.open(join(abspath(dirname(__file__)), 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='Maya Signature Scraper',
    version=main_ns['__version__'],
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
        'dev': ['distutils2', 'twine', 'virtualenv', 'Sphinx', 'docutils', 'docopt']
    },
    entry_points={
        'console_scripts': [
            'mayasig=maya_signatures.cli:main',
        ],
    },
    cmdclass={'test': 'tox'},
)
