Changelog
=========

2.1 - May 10, 2016
------------------

* Do not remove empty ``<a>`` tags that could be used as anchors.
* When removing empty tags, allow to define additional tags that are considered OK to be empty


2.0 - December 7, 2012
----------------------

* When wrapping unwrapped text do not create separate wrappers for inline
  elements.

* Use PEP8 naming for all functions. The old names for public methods
  will continue to work for backwards compatibility.

* Add support for Python 3.


1.10 - May 17, 2011
-------------------

* Add option to `sanitize` to specify a different wrap element or
  skip wrapping completely.


1.9 - April 27, 2011
--------------------

* Add MANIFEST.in to faciliate releases not made from subversion.

* Fix all cleaners to strip javascript. This fixes `issue 1
  <https://github.com/wichert/htmllaundry/issues/1>`_.


1.8 - November 30, 2010
-----------------------

* Remove link target enforcement from hardcoded code path from ``sanitize``.
  This makes it possible to use the new ``link_target`` cleaner option.


1.7 - November 30, 2010
-----------------------

* Make forcing of target attributes on externals linke configurable via a
  new ``link_target`` option in the cleaners. Only enable this option for
  the ``CommentCleaner``.


1.6 - November 18, 2010
-----------------------

* Correct whitespace test for wrapping bare text as well.


1.5 - November 18, 2010
-----------------------

* Correct whitespace checks to handle all unicode whitespace. This fixes problems
  with \xA0 (or &nbsp; in HTML-speak) being treated as text.


1.4 - August 3, 2010
--------------------

* Small code cleanup.

* Strip leading breaks.


1.3 - July 30, 2010
-------------------

* Strip all top level br elements. Breaks are fine in blocklevel elements,
  but should not be used to add vertical spacing between block elements.


1.2 - February 15, 2010
-----------------------

* Fix a typo in the documentation.

* Strip trailing breaks.


1.1 - February 5, 2010
----------------------

* Add a simple StripMarkup method.

* Add ZCML necessary for z3c.form integration.


1.0 - February 5, 2010
----------------------

* First release

