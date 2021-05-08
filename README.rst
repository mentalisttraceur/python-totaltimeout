totaltimeout
============

*Code timeouts correctly, without the hassle.*

So you're writing a function that takes a timeout

.. code:: python

    def foo(timeout):
        ...

and inside it you do something like

.. code:: python

    bar(timeout)
    qux(timeout)

*Wrong!* The right way is to subtract the time spent in the first
function, and pass just the remaining time as the timeout to the
second function.

Or maybe you want to put a retry loop around a function that takes
a timeout?

.. code:: python

    while ...:
        foo(timeout)

The right way is to set a timeout for the whole loop, subtract the
time each iteration took, pass the remaining time to the function,
and break out once we're out of time.

``totaltimeout`` lets you code timeouts the right way like that,
without all that boilerplate for calculating the remaining time.

Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install totaltimeout


Usage
-----

Import the ``Timeout`` class.

.. code:: python

    from totaltimeout import Timeout

Waiting in a "timed loop" for an API with retries (useful
for unreliable APIs that may either hang or need retries):

.. code:: python

    for time_left in Timeout(SOME_NUMBER_OF_SECONDS):
         reply = requests.get(api_url, timeout=time_left)
         if reply.status == 200:
             break

Same as above, but with a wait between retries:

.. code:: python

    timeout = Timeout(SOME_NUMBER_OF_SECONDS)
    for time_left in timeout:
         reply = requests.get(some_flaky_api_url, timeout=time_left)
         if reply.status == 200:
             break
         # If you need to get the remaining time again in the same
         # loop iteration, you have to use the .time_left() method:
         if timeout.time_left() <= RETRY_DELAY:
             break
         time.sleep(RETRY_DELAY)

Waiting for multiple tasks to finish:

.. code:: python

    timeout = Timeout(10.0)
    thread_foo.join(timeout.time_left())
    thread_bar.join(timeout.time_left())
    thread_qux.join(timeout.time_left())
    # Works out almost as if we waited 10
    # seconds for each thread in parallel.

Waiting for multiple tasks within each iteration of a "timed loop":

.. code:: python

    timeout = Timeout(SOME_NUMBER_OF_SECONDS)
    for time_left in timeout:
         some_work(timeout=time_left)
         some_more_work(timeout=timeout.time_left())
         some_other_work(timeout=timeout.time_left())

Using a monotonic clock instead of the wall clock:

.. code:: python

    import time

    timeout = Timeout(10.0, clock=time.monotonic)

You can also set the starting time of the timeout. This is
useful if you need a repeating timeout on an interval, and
you want that interval to stay synchronized with the clock:

.. code:: python

    INTERVAL = 60
    beginning_of_interval = (time.now() // INTERVAL) * INTERVAL
    while True:
        timeout = Timeout(INTERVAL, start=beginning_of_interval)
        metric_values = []
        for time_left in timeout:
            metric_values.append(get_metric())
        average_and_report(metric_values)
        beginning_of_interval += INTERVAL
