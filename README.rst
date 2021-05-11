totaltimeout
============

*Get timeouts right, without the hassle.*

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
a timeout:

.. code:: python

    while ...:
        foo(timeout)

The right way is to set a timeout for the whole loop, subtract the
time each iteration took, pass the remaining time to the function,
and break out once we're out of time.

``totaltimeout`` lets you code timeouts the right way, without
writing all that boilerplate to calculate the remaining time.

Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


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
         reply = requests.get(api_url, timeout=time_left)
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

You can also set the starting time of the timeout. This lets timeouts
count down from a well-known point in time, which can be useful for
testing, for synchronizing timeouts across networks, and so on:

.. code:: python

    start_of_this_minute = (time.now() // 60) * 60
    timeout = Timeout(10.0, start=start_of_this_minute)

.. code:: python

    moment_in_time = time.now()
    timeout = Timeout(10.0, start=moment_in_time)
    time.sleep(1)
    identical_timeout = Timeout(10.0, start=moment_in_time)
    # both timeouts have exactly the same amount of time left

Finally, ``totaltimeout`` can be an ergonomic way to put a time
limit on a loop even if the code in the loop does not support
timeouts, so long as each iteration does not block for too long:

.. code:: python

    counter = 0
    for _ in Timeout(30):
        counter += 1
