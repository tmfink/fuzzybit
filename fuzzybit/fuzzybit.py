"""Tracks history of observed bit values"""


class InsufficientHistoryException(Exception):
    """
    Indicates that no history has been observed and hence entropy can not be
    determined.
    """
    pass


class FuzzyObject(object):
    """Abstract parent class for Fuzzy objects"""

    def get_entropy(self):
        """Return entropy in bits"""
        raise NotImplementedError()

    def get_value(self):
        """Return representation as string"""
        raise NotImplementedError()


class FuzzyBit(FuzzyObject):
    """
    Determine possible values of bit

    '?' - no history observed
    '0' - always observed to be 0
    '1' - always observed to be 1
    '*' - observed to be either 0 or 1
    """

    def __init__(self, history=None):
        """
        Create FuzzyBit, optionally with history. The history should be an
        iterable of strings of length 1.
        """
        self._value = '?'
        if history != None:
            for item in history:
                self.observe_value(item)

    def observe_value(self, just_seen):
        """Add bit to history"""
        if just_seen not in ['0', '1']:
            raise Exception('Must be 0 or 1')

        if self._value == '?':
            # First value seen
            self._value = just_seen
            return
        elif self._value == '*':
            # Will always be *
            return

        # Current value is 0 or 1
        if self._value == just_seen:
            return
        else:
            # See different value
            self._value = '*'

    def get_value(self):
        """Return representation as string of length one"""

        return self._value

    def get_entropy(self):
        if self._value == '?':
            raise InsufficientHistoryException('No history to calculate entropy')
        elif self._value == '*':
            return 1
        else:
            return 0


class FuzzyInt(FuzzyObject):
    """Represents integer of FuzzyBits"""

    def __init__(self, bit_size, history=None):
        if bit_size <= 0:
            raise Exception("Fuzzy integer must have positive length")

        self._bit_size = bit_size

        # Store bits such that the lowest order bits are stored first
        # (1 << i) & n is stored in _bits[i]
        self._bits = [FuzzyBit() for _ in xrange(bit_size)]

        if history != None:
            for item in history:
                self.observe_value(item)

    def observe_value(self, just_seen):
        """Observe integer value just_seen"""

        for i in range(self._bit_size):
            seen_bit = '1' if just_seen & (1 << i) else '0'
            self._bits[i].observe_value(seen_bit)

    def get_value(self):
        """Return string of FuzzyBits with most significant bits first"""
        return ''.join(reversed(list(b.get_value() for b in self._bits)))

    def get_entropy(self):
        if self._bits[0].get_value() == '?':
            raise InsufficientHistoryException('No history to calculate entropy')
        else:
            return self.get_value().count('*')
