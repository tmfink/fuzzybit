"""Contains tests for fuzzybit module"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from unittest import TestCase
from fuzzybit import (
        FuzzyBit, FuzzyInt,
        InsufficientHistoryException, InvalidArgumentException
        )


class TestFuzzyBit(TestCase):
    """Tests FuzzyBit class"""

    def assert_history(self, history, value):
        self.assertTrue(FuzzyBit(history), value)

    def test_blank(self):
        self.assert_history('', '?')

    def test_hist1(self):
        self.assert_history('0', '0')
        self.assert_history('1', '1')

    def test_hist2(self):
        self.assert_history('00', '0')
        self.assert_history('01', '*')
        self.assert_history('10', '*')
        self.assert_history('11', '1')

    def test_entropy_fail(self):
        self.assertRaises(InsufficientHistoryException,
                          lambda: FuzzyBit('').get_entropy())

    def test_entropy_none(self):
        self.assertEqual(FuzzyBit('0').get_entropy(), 0)

    def test_entropy_one(self):
        self.assertEqual(FuzzyBit('01').get_entropy(), 1)
        self.assertEqual(FuzzyBit('10').get_entropy(), 1)
        self.assertEqual(FuzzyBit('100').get_entropy(), 1)
        self.assertEqual(FuzzyBit('101').get_entropy(), 1)

    def test_mixed_types(self):
        self.assertEqual(FuzzyBit([0, '1', '0', 1]).get_entropy(), 1)

    def test_wrong_values(self):
        self.assertRaises(InvalidArgumentException, lambda: FuzzyBit('2'))
        self.assertRaises(TypeError, lambda: FuzzyBit(-1))
        self.assertRaises(InvalidArgumentException, lambda: FuzzyBit([-1]))


class TestFuzzyInt(TestCase):
    """Tests FuzzyInt class"""

    def assert_history(self, bit_size, history, value):
        self.assertTrue(FuzzyInt(bit_size, history).get_value(), value)

    def test_blank(self):
        self.assert_history(4, [], '????')

    def test_hist1(self):
        self.assert_history(4, [0b0000], '0000')
        self.assert_history(4, [0b0010], '0010')

    def test_hist2(self):
        self.assert_history(4, [0b0000, 0b1100], '**00')
        self.assert_history(4, ['0000', '1100'], '**00')
        self.assert_history(4, [0b0010, 0b0110], '0*10')

    def test_entropy_error(self):
        self.assertRaises(InsufficientHistoryException,
                          lambda: FuzzyInt(4, []).get_entropy())

    def test_entropy_none(self):
        self.assertEqual(FuzzyInt(4, [0b0000]).get_entropy(), 0)
        self.assertEqual(FuzzyInt(4, [0b1100]).get_entropy(), 0)
        self.assertEqual(FuzzyInt(4, [0b1111]).get_entropy(), 0)
        self.assertEqual(FuzzyInt(4, ['1111']).get_entropy(), 0)

    def test_entropy1(self):
        self.assertEqual(FuzzyInt(4, [0b0000, 0b1100]).get_entropy(), 2)
        self.assertEqual(FuzzyInt(4, [0b0110, 0b1100]).get_entropy(), 2)
        self.assertEqual(FuzzyInt(4, [0b0000, 0b0000, 0b0100]).get_entropy(), 1)
        self.assertEqual(FuzzyInt(4, [0b0000, '0000', 0b0100]).get_entropy(), 1)

    def test_wrong_values(self):
        self.assertRaises(TypeError, lambda: FuzzyInt(4, -1))
        self.assertRaises(InvalidArgumentException,
                          lambda: FuzzyInt(4, [0b0000, '7000', 0b0100]))
