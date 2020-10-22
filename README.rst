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
         reply = requests.get(some_flaky_api_url, timeout=time_left)
         if reply.status == 200:
             break

Same as above, but with a wait between retries:

.. code:: python

    timeout = Timeout(SOME_NUMBER_OF_SECONDS)
    for time_left in timeout:
         reply = requests.get(some_flaky_api_url, timeout=time_left)
         if reply.status == 200:
             break
         if timeout.time_left() <= RETRY_DELAY:
             break
         time.sleep(RETRY_DELAY)

Waiting for multiple tasks to finish:

.. code:: python

    timeout = Timeout(10.0)
    my_thread_foo.join(timeout.time_left())
    my_thread_bar.join(timeout.time_left())
    my_thread_qux.join(timeout.time_left())
    # Wait only as long as the slowest
    # thread to finish, as if they all
    # got a 10 second wait in parallel.

Waiting for multiple tasks within each iteration of a "timed loop":

.. code:: python

    timeout = Timeout(SOME_NUMBER_OF_SECONDS)
    for time_left in timeout:
         foo.some_work(timeout=time_left)
         # The first timeout can be *either* be the for loop value or
         # the ``time_left()`` method. The rest *have to be* the latter.
         foo.some_more_work(timeout=timeout.time_left())
         some_other_work(timeout=timeout.time_left())

Using a monotonic clock instead of the wall clock:

.. code:: python

    import time

    timeout = Timeout(10.0, now=time.monotonic)

You can also set the starting point in time of the timeout,
which is useful when you need a repeating timeout on an
interval, and you don't want that interval to drift or you
you want that interval to stay faithful to the wall clock
time:

.. code:: python

    beginning_of_minute = (time.now() // 60) * 60
    while True:
        timeout = Timeout(60, start=beginning_of_minute)
        metric_values = []
        for time_left in timeout:
            metric_values.append(get_metric())
        average_and_report(metric_values)
        beginning_of_minute += 60


Explanation
~~~~~~~~~~~

If you're confused about what's going on, run this example program:

.. code:: python

    from time import sleep

    from totaltimeout import Timeout

    def demo(timeout_in_seconds):
        timeout = Timeout(timeout_in_seconds)
        for time_left in timeout:
            print(time_left)
            sleep(1)
            print(timeout.time_left())
            sleep(1)

    if __name__ == '__main__':
        demo(10)

You should get output kinda like this::

    9.99990844912827
    8.996184696443379
    7.992705063894391
    6.990415567532182
    5.983945298939943
    4.981594786979258
    3.979213748127222
    2.9768632212653756
    1.9745127055794
    0.9699955033138394
