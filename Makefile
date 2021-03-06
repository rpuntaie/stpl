.PHONY: test check dist up man tag devinstall

test:
	py.test

man:
	pandoc README.rst -s -t man -o man/stpl.1
	#pandoc README.rst -s -t man | /usr/bin/man -l -

check:
	restview --long-description --strict

dist: test man
	sudo python setup.py bdist_wheel

up: dist
	twine upload dist/`ls dist -rt | tail -1`

devinstall:
	sudo pip install -e .

tag: devinstall
	$(eval TAGMSG="v$(shell stpl --version | cut -d ' ' -f 2)")
	echo $(TAGMSG)
	git tag -s $(TAGMSG) -m"$(TAGMSG)"
	git verify-tag $(TAGMSG)
	git push origin $(TAGMSG) --follow-tags
