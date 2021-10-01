# SPDX-License-Identifier: 0BSD
# Copyright 2018 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Get timeouts right, without the hassle.

``totaltimeout`` robustly, efficiently, and cleanly abstracts away
the boilerplate of calculating the time remaining on a timeout,
after some time has already passed. This helps correctly combine
multiple operations which take timeout arguments.
"""

__version__ = '3.0.1'
__all__ = ('Timeout', 'TimeoutIterator')


from time import time as _time


def _name(obj):
    return type(obj).__name__


def _repr(obj, *args, **kwargs):
    arguments = []
    for argument in args:
        arguments.append(repr(argument))
    for name in kwargs:
        arguments.append(name + '=' + repr(kwargs[name]))
    return _name(obj) + '(' + ', '.join(arguments) + ')'


class Timeout(object):
    # pylint: disable=too-few-public-methods
    # pylint: disable=bad-option-value,useless-object-inheritance
    """Timeout object that helps cover many operations with one timeout."""

    def __init__(self, timeout, start=None, clock=None):
        """Initialize the timeout object.

        Arguments:
            timeout: Time duration before the timeout expires.
            start (optional): Time from which the timeout starts.
                Defaults to the result of calling ``clock``.
            clock (optional): Function (or other callable) that
                is called with no arguments to get the current
                time. Defaults to ``time.time``.
        """
        self._timeout = timeout
        if clock is None:
            clock = _time
        self._clock = clock
        if start is None:
            start = clock()
        self._start = start

    def __repr__(self):
        """Represent this timeout object as an unambiguous string."""
        if self._clock is _time:
            return _repr(self, self._timeout, start=self._start)
        return _repr(self, self._timeout, start=self._start, clock=self._clock)

    def __iter__(self):
        """Get a TimeoutIterator for this timeout object."""
        return TimeoutIterator(self)

    def time_left(self):
        """Return the time remaining in this timeout object."""
        now = self._clock()
        elapsed = now - self._start
        remaining = self._timeout - elapsed
        return max(remaining, 0)


class TimeoutIterator(object):
    # pylint: disable=too-few-public-methods
    # pylint: disable=bad-option-value,useless-object-inheritance
    """Iterator that yields the time remaining until its timeout expires."""

    def __init__(self, timeout):
        """Initialize the timeout iterator.

        Arguments:
            timeout: Timeout object instance to iterate on.
        """
        self._timeout = timeout

    def __repr__(self):
        """Represent this timeout iterator as an unambiguous string."""
        return _repr(self, self._timeout)

    def __iter__(self):
        """Return this timeout iterator itself."""
        return self

    def __next__(self):
        """Return the time remaining in this iterator's timeout object.

        Raises:
            StopIteration: If no time is left in the timeout object.
        """
        time_left = self._timeout.time_left()
        if time_left <= 0:
            raise StopIteration
        return time_left

    next = __next__  # Python 2 used `next` instead of ``__next__``


# Portability to some minimal Python implementations:
try:
    Timeout.__name__
except AttributeError:
    Timeout.__name__ = 'Timeout'
    TimeoutIterator.__name__ = 'TimeoutIterator'
