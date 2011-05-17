Introduction
============

This package contains several handy python methods to cleanup HTML markup
or perform other common changes. The cleanup is strict enough to be able
to clean HTML pasted from MS Word or Apple Pages. This package also contains
integration code for `z3c.form`_ to provide fields that automatically
sanitize HTML on save.

The implementation is based on the ``Cleaner`` class from `lxml`_.


Cleanup routines
================

All cleanup routines can be invoked through the single ``sanitize`` function.
This functions takes an input string as input and will return a cleaned up
version of that string. Here is a simple example::

  >>> from htmllaundry import sanitize
  >>> sanitize('Hello, <em>world</em>')
  '<p>Hello, <em>world</em></p>'

The sanitize method takes an extra optional parameter with a lxml Cleaner
instance, which can be used to use different filtering rules. htmllaundry
includes three cleaners:

* ``htmllaundry.cleaners.DocumentCleaner``, which is the default cleaner. This
  cleaner will allow most safe tags, while stripping out inline styles and
  insecure markup.

* ``htmllaundry.cleaners.LineCleaner`` is a more strict cleaner which only
  allows a few inline elements. This is useful in places where you only
  want to accept single-line input, for example in document titles.

* ``htmllaundry.cleaners.CommentCleaner`` only allows a very limited set of
  HTML elements, and is designed to be useful for user provided comments. It
  will also force all external links to open in a new browser window.


If you want to go all the way you can also use ``strip_markup`` to strip
all markup from your input::

  >>> from htmllaundry import strip_markup
  >>> strip_markup('Hello, <em>world</em>')
  'Hello, world'


z3c.form integration
====================

If you want to use the ``z3c.form`` integration you should use the ``z3cform``
extra for this package::

  install_requires=[
       ....
       htmllaundry [z3cform]
       ...
       ],

In addition you will need to load the ZCML. In your ``configure.zcml`` add
a line like this::

  <include package="htmllaundry" />
 
You can then use the `HtmlText` field type in your schemas. For example::

  from zope.interface import Interface
  from zope import schema
  from htmllaundry.z3cform import HtmlText

  class IDocument(Interface):
      title = schema.TextLine(
              title = _(u"Title"),
              required = True)

      description = HtmlText(
              title = _(u"Description"),
            required = True)

Please note that using ``HtmlText`` will not automatically give you a WYSYWIG
widget.


.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _lxml: http://lxml.de/
