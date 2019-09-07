#! /usr/bin/env python3

#pip install --user -e .
#py.test --cov stpl --cov-report term-missing

#sudo python setup.py bdist_wheel
#twine upload ./dist/stpl*.whl

from setuptools import setup
import os

#https://github.com/pypa/packaging-problems/issues/72
from glob import glob
import os

def find_dirs(dir_name):
    for dir, dirs, files in os.walk('.'):
        if dir_name in dirs:
            yield os.path.relpath(os.path.join(dir, dir_name))

# Find all of the man/info pages
data_files = []
man_sections = {}
for dir in find_dirs('man'):
    for file in os.listdir(dir):
        section = file.split('.')[-1]
        man_sections[section] = man_sections.get(section, []) + [os.path.join(dir, file)]
for section in man_sections:
    data_files.append(('share/man/man'+section, man_sections[section]))
info_pages = {}
for dir in find_dirs('info'):
    for file in glob(os.path.join(dir, '*.info')):
        info_pages[dir] = info_pages.get(dir, []) + [file] 
for dir in info_pages:
    data_files.append(('share/info', info_pages[dir]))    

#also in readme.rst
__version__ = '1.13.2'
#bottle_major+1.bottle_miner.local_fix

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
        'Programming Language :: Python',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Topic :: Utilities',
        ],

    install_requires = [],
    extras_require = {'develop': ['mock','pytest','pytest-coverage']},
    long_description = read('readme.rst'),
    ##to check with ``restview --pypi-strict long_description.rst``
    #with open('long_description.rst','w',encoding='utf-8') as f:
    #    f.write(long_description)
    packages=['stpl'],
    include_package_data=True,
    exclude_package_data={'': ['*.pyc']},
    data_files=data_files,
    zip_safe=False,
    tests_require=[],
    entry_points={'console_scripts': ['stpl=stpl:main']}
    )

