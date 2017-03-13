.. :changelog:

History
-------

2.0.2 (2017-03-13)
++++++++++++++++++

* Fixed requirements for Python > 3.4.

2.0.1 (2017-02-27)
++++++++++++++++++

* Remove enum34 for Python > 3.4.
* Added support for Python 2.6.


2.0 (2016-09-26)
++++++++++++++++

* Added force_set method.
* Added field machine.
* Added support for Python 3.5.

Backward compatibility breaks:

* Empty state is now disallowed.
* Only full names are allowed, when using scalars, no shortcuts.
* Removed support for unhashable types.

1.0 (2014-09-04)
----------------

* Added all basic features.

0.1.0 (2014-08-08)
---------------------

* First release on PyPI.
* Added utilities to create simple state machine.
