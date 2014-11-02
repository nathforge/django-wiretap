Django Wiretap
==============

Captures HTTP requests & responses for debugging.

This is an early release, and is **not** suitable for production use.


Screenshots
-----------

List
^^^^

    .. image:: screenshot-list.png

View
^^^^

    .. image:: screenshot-view.png


Usage:
------

- ``pip install django-wiretap``
- Edit Django settings:

   - Add ``'wiretap'`` to ``INSTALLED_APPS``
   - Add ``'wiretap.middleware.WiretapMiddleware'`` to your ``MIDDLEWARE_CLASSES``.

- Create models with ``./manage.py syncdb``
- Go to Django admin, add a new ``Tap``.

  - This contains a path regex, which is matched against the full path, including the query string
  - If you just want to test Wiretap, set it to ``'/'``.

HTTP request/responses will now be saved to the `Message` admin page.

Note that Wiretap will be disabled if Django is not in debug mode.
