#! /usr/bin/env python3
# -*- coding: utf-8 -*

import pytest
from stpl import main
import os
import subprocess
import sys

from mock import patch

os.environ['PATH']+=":"+os.path.dirname(__file__)

@pytest.yield_fixture
def tmpworkdir(tmpdir):
    cwd = os.getcwd()
    os.chdir(tmpdir.strpath)
    yield tmpdir
    os.chdir(cwd)

def test_string(request,capfd):
    main(file_or_string="{{i+j}}",directory=None,code="i=2;j=3")
    out, err = capfd.readouterr()
    assert out == '5'

@pytest.yield_fixture
def stplfile(tmpworkdir):
    with open('tst.c.stpl','w',encoding='utf-8') as f:
        f.write('''\
{{i+j}}'''
        )
    yield 'tst.c.stpl'

def test_file(stplfile,capfd):
    main(file_or_string=stplfile,directory=None,code="i=2;j=3")
    out, err = capfd.readouterr()
    assert out == '5'

def test_dir(stplfile):
    main(file_or_string=stplfile,directory='tst.c',code="i=2;j=3")
    assert os.path.isfile('tst.c')
    assert open('tst.c').read()=='5'

@pytest.yield_fixture
def nostplfile(tmpworkdir):
    with open('tst.c','w',encoding='utf-8') as f:
        f.write('''\
{{i+j}}'''
        )
    yield 'tst.c'

#like inplace
def test_nostpl(nostplfile):
    main(file_or_string=nostplfile,directory='.',code="i=2;j=3")
    assert os.path.isfile('tst.c')
    assert open('tst.c').read()=='5'

def test_parse_args(stplfile):
    testargs = ['stpl.py',stplfile,'.','i=2;j=3']
    with patch.object(sys, 'argv', testargs):
        main()
        assert os.path.isfile('tst.c')
        assert open('tst.c').read()=='5'

def test_raise(request):
    with pytest.raises(ValueError):
        main(file_or_string="{{i+j}}",directory='.',code="i=2;j=3")
