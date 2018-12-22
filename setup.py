#! /usr/bin/env python3

#py.test --cov stpl --cov-report term-missing

#sudo python setup.py bdist_wheel
#twine upload ./dist/stpl*.whl

from setuptools import setup
import os

__version__ = '1.1.5'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname),encoding='utf-8').read()

setup(name = 'stpl',
    version = __version__,
    description = 'stpl - expand bottle SimpleTemplate',
    license = 'MIT',
    author = 'Roland Puntaier',
    keywords=['Duplicate, File'],
    author_email = 'roland.puntaier@gmail.com',
    url = 'https://github.com/rpuntaie/stpl',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Topic :: Utilities',
        ],

    install_requires = [],
    extras_require = {'develop': ['mock','pytest','pytest-coverage']},
    long_description = read('readme.rst'),
    packages=['stpl'],
    include_package_data=False,
    zip_safe=False,
    tests_require=[],
    entry_points={'console_scripts': ['stpl=stpl:main']}
    )

