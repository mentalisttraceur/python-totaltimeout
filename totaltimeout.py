# Copyright 2018 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


"""Spread one timeout over many operations

Correctly and efficiently spreads one timeout over many steps by
recalculating the time remaining after some amount of waiting has
already happened, to pass an adjusted timeout to the next step.
"""


from time import time as _time


__version__ = '3.0.0'
__all__ = ('Timeout',)


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
    """Counts down for the total timeout duration given"""

    def __init__(self, timeout, start=None, clock=None):
        self._timeout = timeout
        if clock is None:
            clock = _time
        self._clock = clock
        if start is None:
            start = clock()
        self._start = start

    def __repr__(self):
        if self._clock is _time:
            return _repr(self, self._timeout, start=self._start)
        return _repr(self, self._timeout, start=self._start, clock=self._clock)

    def __iter__(self):
        return TimeoutIterator(self)

    def time_left(self):
        """Returns time remaining in the timeout"""
        now = self._clock()
        elapsed = now - self._start
        remaining = self._timeout - elapsed
        return max(remaining, 0)


class TimeoutIterator(object):
    # pylint: disable=too-few-public-methods
    # pylint: disable=bad-option-value,useless-object-inheritance
    """Loops on a Timeout object, yielding the time remaining"""

    def __init__(self, timeout):
        self._timeout = timeout

    def __repr__(self):
        return _repr(self, self._timeout)

    def __iter__(self):
        return self

    def __next__(self):
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
