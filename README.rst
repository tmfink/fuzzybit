Fuzzybit
========

Fuzzybit is a library for determining possible values of bits in integers based
on observed concrete values.


Install
-------

To install fuzzybit (after downloading)::

    python setup.py install


To install fuzzybit with pip::

    pip install fuzzybit


Using fuzzybit
--------------

Here is an example of tracking a single bit using the FuzzyBit class::

    >>> import fuzzybit
    >>> b = fuzzybit.FuzzyBit()
    >>> b.get_value()
    '?'

    >>> b.observe_value('0')
    >>> b.get_value()
    '0'
    >>> b.get_entropy()
    0

    >>> b.observe_value('0')
    >>> b.get_value()
    '0'
    >>> b.get_entropy()
    0

    >>> b.observe_value('1')
    >>> b.get_value()
    '*'
    >>> b.get_entropy()
    1


Here is an example of tracking an integer using the FuzzyInt class::

    >>> import fuzzybit
    >>> x = fuzzybit.FuzzyInt(16)  # Create 16 bit integer
    >>> x.get_value()
    '????????????????'

    >>> x.observe_value(0x0ff0)
    >>> x.get_value()
    '0000111111110000'
    >>> x.get_entropy()
    0

    >>> x.observe_value(0x0000)
    >>> x.get_value()
    '0000********0000'
    >>> x.get_entropy()
    8

    >>> x.observe_value(0x0dd1)
    >>> x.get_value()
    '0000********000*'
    >>> x.get_entropy()
    9
