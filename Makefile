.PHONY: test check dist up man

test:
	py.test

man:
	pandoc README.rst -s -t man -o man/stpl.1
	#pandoc README.rst -s -t man | /usr/bin/man -l -

check:
	restview --long-description --strict

dist:
	sudo python setup.py bdist_wheel

up:
	twine upload dist/`ls dist -rt | tail -1`

