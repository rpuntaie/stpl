==============================
stpl(1) Version 1.13.2 \| stpl
==============================

..   To test man page:
..
..     pandoc README.rst -s -t man | /usr/bin/man -l -
..
..   The generate:
..
..     pandoc README.rst -s -t man -o man/stpl.1

NAME
====

**stpl** — simple template - Bottle SimpleTemplate in a separate command line tool.

SYNOPSIS
========

**stpl** <file>\|<string>\|- [<directory>\|-] [<python variable>]* [-I <include folder>]*

DESCRIPTION
===========

**stpl** is a little command line tool, that

- takes a `bottle <https://bottlepy.org/docs/dev/stpl.html>`__
  SimpleTemplate file with extension **.stpl** and
- expands the template

  - to **stdout** or
  - to a directory, thereby dropping the **.stpl**

Parameters:

1) file or string or -
2) optional: directory or -
3) optionally several: python code defining variables. Enclose with ''.
4) optionally several: -I <include folder>

To install for user only, do::

   pip install --user stpl

Usage from Python:

.. code:: python

   >>> from stpl import SimpleTemplate
   >>> tpl = SimpleTemplate('Hello {{name}}!')
   >>> tpl.render(name='World')
   u'Hello World!'

or

.. code:: python

   >>> from bottle import template
   >>> template('Hello {{name}}!', name='World')
   u'Hello World!'

or

.. code:: python

   >>> from bottle import template
   >>> my_dict={'number': '123', 'street': 'Fake St.', 'city': 'Fakeville'}
   >>> template('I live at {{number}} {{street}}, {{city}}', **my_dict)
   u'I live at 123 Fake St., Fakeville'


SIMPLETEMPLATE
==============

Inline Expressions
------------------

``{{...}}``: any python expression is allowed within the curly brackets as long as it evaluates to a string or something that has a string representation:

.. code:: python

  >>> template('Hello {{name}}!', name='World')
  u'Hello World!'
  >>> template('Hello {{name.title() if name else "stranger"}}!', name=None)
  u'Hello stranger!'
  >>> template('Hello {{name.title() if name else "stranger"}}!', name='mArC')
  u'Hello Marc!'

You can start the expression with an exclamation mark to disable escaping::

.. code:: python

  >>> template('Hello {{name}}!', name='<b>World</b>')
  u'Hello &lt;b&gt;World&lt;/b&gt;!'
  >>> template('Hello {{!name}}!', name='<b>World</b>')
  u'Hello <b>World</b>!'

Embedded python code
--------------------

Code lines start with ``%`` and code blocks are surrounded by ``<%`` and ``%>`` tokens::

  % name = "Bob"  # a line of python code
  <p>Some plain text in between</p>
  <%
    # A block of python code
    name = name.title().strip()
  %>
  <p>More plain text</p>

Embedded python code follows regular python syntax, but with two additional syntax rules:

* **Indentation is ignored.**
  You can put as much whitespace in front of statements as you want.
  This allows you to align your code with the surrounding markup and can greatly improve readability.

* Blocks that are normally indented have to be closed explicitly with an ``end`` keyword.

::

  <ul>
    % for item in basket:
      <li>{{item}}</li>
    % end
  </ul>

Both the ``%`` and the ``<%`` tokens are only recognized if they are the first non-whitespace characters in a line.
You don't have to escape them if they appear mid-text in your template markup.
Only if a line of text starts with one of these tokens, you have to escape it with a backslash.
In the rare case where the backslash + token combination appears in your markup at the beginning of a line,
you can always help yourself with a string literal in an inline expression::

  This line contains % and <% but no python code.
  \% This text-line starts with the '%' token.
  \<% Another line that starts with a token but is rendered as text.
  {{'\\%'}} this line starts with an escaped token.

Whitespace Control
------------------

Code blocks and code lines always span the whole line.
Whitespace in front of after a code segment is stripped away.
You won't see empty lines or dangling whitespace in your template because of embedded code::

  <div>
   % if True:
    <span>content</span>
   % end
  </div>

This snippet renders to clean and compact html::

  <div>
    <span>content</span>
  </div>

But embedding code still requires you to start a new line, which may not what you want to see in your rendered template.
To skip the newline in front of a code segment, end the text line with a double-backslash::

  <div>\\
   %if True:
  <span>content</span>\\
   %end
  </div>

This time the rendered template looks like this::

  <div><span>content</span></div>

This only works directly in front of code segments.
In all other places you can control the whitespace yourself and don't need any special syntax.

Template Functions
==================

Each template is preloaded with a bunch of functions that help with the most common use cases.
These functions are always available.
You don't have to import or provide them yourself.
For everything not covered here there are probably good python libraries available.
Remember that you can ``import`` anything you want within your templates.
They are python programs after all.


*include(sub_template, \*\*variables)*


    Render a sub-template with the specified variables and insert the resulting text into the current template.
    The function returns a dictionary containing the local variables passed to or defined within the sub-template::

        % include('header.tpl', title='Page Title')
        Page Content
        % include('footer.tpl')


*rebase(name, \*\*variables)*

    Mark the current template to be later included into a different template.
    After the current template is rendered, its resulting text is stored in a variable named ``base`` and passed to the base-template, which is then rendered.
    This can be used to ``wrap`` a template with surrounding text, or simulate the inheritance feature found in other template engines::

        % rebase('base.tpl', title='Page Title')
        <p>Page Content ...</p>

    This can be combined with the following ``base.tpl``::

        <html>
        <head>
          <title>{{title or 'No title'}}</title>
        </head>
        <body>
          {{!base}}
        </body>
        </html>


Accessing undefined variables in a template raises ``NameError`` and stops rendering immediately.
This is standard python behavior and nothing new,
but vanilla python lacks an easy way to check the availability of a variable.
This quickly gets annoying if you want to support flexible inputs or use the
same template in different situations. These functions may help:


*defined(name)*

    Return True if the variable is defined in the current template namespace, False otherwise.


*get(name, default=None)*

    Return the variable, or a default value.


*setdefault(name, default)*

    If the variable is not defined, create it with the given default value.
    Return the variable.

    Here is an example that uses all three functions to implement optional template variables in different ways::

        % setdefault('text', 'No Text')
        <h1>{{get('title', 'No Title')}}</h1>
        <p> {{ text }} </p>
        % if defined('author'):
          <p>By {{ author }}</p>
        % end


EXAMPLES
========

Example file:

    NAME="{{!full_name}}"
    EMAIL="{{!default_email}}"
    REPO="{{!repo}}"

To stdout::

    stpl file.txt.stpl - 'full_name="Roland Puntaier"' 'default_email="roland.puntaier@gmail.com"' 'repo="https://github.com/rpuntaie/stpl"'

To file.txt::

    stpl file.txt.stpl . 'full_name="Roland Puntaier"' 'default_email="roland.puntaier\@gmail.com"' 'repo="https://github.com/rpuntaie/stpl"'

