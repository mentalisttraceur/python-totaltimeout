totaltimeout
============

Spread one timeout over many operations.

Correctly and efficiently spreads one timeout over many steps by
recalculating the time remaining after some amount of waiting has
already happened, to pass an adjusted timeout to the next step.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.

The current version number is available in the variable ``__version__``,
as is normal for Python modules.


Installation
------------

::

    pip install totaltimeout


Usage
-----

Import the ``Timeout`` class.

.. code:: python

    from totaltimeout import Timeout

Waiting in a "timed loop" for an API with retries:

.. code:: python

    for time_left in Timeout(SOME_NUMBER_OF_SECONDS):
         reply = requests.get(some_flaky_api_url, timeout=time_left)
         if reply.status == 200:
             break
         time.sleep(some_retry_delay)

Waiting for multiple tasks to finish:

.. code:: python

    timeout = Timeout(10.0)
    my_thread_foo.join(timeout.time_left())
    my_thread_bar.join(timeout.time_left())
    my_thread_qux.join(timeout.time_left())
    # Waits at most ten seconds total for all three threads, but
    # waits the full ten seconds if *any* thread takes that long.

Waiting for multiple tasks within each iteration of a "timed loop"
(combining the above two examples):

.. code:: python

    timeout = Timeout(SOME_NUMBER_OF_SECONDS)
    for time_left in timeout:
         foo.some_work(timeout=time_left)
         # The first timeout can be *either* be the for loop value or
         # the ``time_left()`` method. The rest *have to be* the latter.
         foo.more_work(timeout=timeout.time_left())
         some_other_work(timeout=timeout.time_left())


Advanced Usage Notes
~~~~~~~~~~~~~~~~~~~~

``Timeout`` uses ``time.monotonic`` as the default time function,
falling back to ``time.time`` if ``time.monotonic`` is unavailable.

You can override this by passing in a callable as the second argument.

For example, if you've installed the
`monotonic backport <https://pypi.org/project/monotonic>`_:

.. code:: python

    from monotonic import monotonic

    timeout = Timeout(10.0, now=monotonic)

Any callables that return time in seconds as floating point values
are supported as part of the interface subject to SemVer backwards
compability guarantees.

However, **any** callables that return time values that can be
subtracted from each other to produce duration values which in turn can
be subtracted from each other and compared to zero should work, and
seconds are expected only because Python's idiomatic unit for timeouts
is seconds. If the ``timeout``, ``now``, and usage are consistent, any
choice that fits these criteria is likely to work.
