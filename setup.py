"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from maya_signatures import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


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
        'test': ['coverage', 'nose', 'tox', 'virtualenv', 'travis'],
        'dev': ['twine', 'virtualenv', 'Sphinx', 'docutils', 'docopt']
    },
    entry_points={
        'console_scripts': [
            'mayasig=maya_signatures.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
