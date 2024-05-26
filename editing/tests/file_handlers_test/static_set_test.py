#!/usr/bin/env python
"""Tests for static test."""

from typing import Iterator, Hashable
import unittest

from file_handlers.static_set import StaticSet


class TestStaticSetInitMethod(unittest.TestCase):
    """Tests for initialising an Instance."""

    def test_init_with_no_args_expect_staticset_object(self) -> None:
        """Test initiliasing without arguments returns instance."""
        ss = StaticSet()
        self.assertIsInstance(ss, StaticSet)

    def test_init_with_arg_as_hashable_expect_staticset_instance(self) -> None:
        """Test initialising with a Hashable object returns an instance."""
        hashables: list[Hashable] = [
            type, None, str(), bytes(), 1, 0.123, frozenset(), tuple()]
        for item in hashables:
            with self.subTest(item=item):
                ss = StaticSet(item)
                self.assertIsInstance(ss, StaticSet)

    def test_init_with_arg_as_unhashable_expect_raise_typeerror(self) -> None:
        """Test initialising with a Hashable object returns an instance."""
        unhashables: list = [list(), set(), dict()]
        for item in unhashables:
            with (self.subTest(item=item), self.assertRaises(TypeError)):
                StaticSet(item)  # type: ignore


class TestStaticSetItemsProperty(unittest.TestCase):
    """Tests for the items property."""

    def test_init_with_no_args_expect_items_property_as_iterator(self) -> None:
        """Test init without args, items returns Iterator."""
        ss_items = StaticSet().items
        self.assertIsInstance(ss_items, Iterator)

    def test_init_with_no_args_expect_raises_stopiteration_on_next(self) -> None:  # noqa: E501
        """Test init without args, next(items) raises StopIteration."""
        ss_items = StaticSet().items
        with self.assertRaises(StopIteration):
            next(ss_items)

    def test_init_with_arg_as_none_expect_items_property_as_iterator(self) -> None:  # noqa: E501
        """Test init without args, items returns Iterator."""
        ss_items = StaticSet(None).items
        self.assertIsInstance(ss_items, Iterator)

    def test_init_with_arg_as_none_expect_raises_stopiteration_on_next(self) -> None:  # noqa: E501,B950
        """Test init without args, next(items) raises StopIteration."""
        ss_items = StaticSet(None).items
        with self.assertRaises(StopIteration):
            next(ss_items)

    def test_init_with_arg_as_hashable_expect_items_property_as_iterator(self) -> None:  # noqa: E501,B950
        """Test init with Hashable objects, items returns Iterator."""
        hashables: list[Hashable] = [
            type, str(), bytes(), 1, 0.123, frozenset(), tuple()]
        for item in hashables:
            with self.subTest(item=item):
                ss_items = StaticSet(item).items
                self.assertIsInstance(ss_items, Iterator)

    def test_init_with_arg_as_hashable_expect_items_next_has_correct_type(self) -> None:  # noqa: E501,B950
        """Test init with a Hashable, next(items) has correct type."""
        hashables: list[Hashable] = [
            type, str(), bytes(), 1, 0.123, frozenset(), tuple()]
        for item in hashables:
            with self.subTest(item=item):
                ss_items = StaticSet(item).items
                self.assertIsInstance(next(ss_items), type(item))

    def test_init_with_arg_as_hashable_expect_second_items_next_raises_stopiteration(self) -> None:  # noqa: E501,B950
        """Test init with a Hashable, next(items)*2 raises StopIteration."""
        hashables: list[Hashable] = [
            type, str(), bytes(), 1, 0.123, frozenset(), tuple()]
        for item in hashables:
            with self.subTest(item=item):
                ss_items = StaticSet(item).items
                next(ss_items)
                with self.assertRaises(StopIteration):
                    next(ss_items)


class TestStaticSetAndMethod(unittest.TestCase):
    """Tests for the StaticSet & operator."""


class TestStaticSetContainsMethod(unittest.TestCase):
    """Tests for StaticSet.__contains__."""


class TestStaticSetEqualMethod(unittest.TestCase):
    """Tests for the StaticSet == operator."""


class TestStaticSetIAndMethod(unittest.TestCase):
    """Tests for the StaticSet &= operator."""


class TestStaticSetIOrMethod(unittest.TestCase):
    """Tests for the StaticSet |= operator."""


class TestStaticSetISubMethod(unittest.TestCase):
    """Tests for the StaticSet -= operator."""


class TestStaticSetIterMethod(unittest.TestCase):
    """Tests for iter(StaticSet)."""


class TestStaticSetIXorMethod(unittest.TestCase):
    """Tests for the StaticSet ^= operator."""


class TestStaticSetLessEqualMethod(unittest.TestCase):
    """Tests for the StaticSet <= operator."""


class TestStaticSetLessMethod(unittest.TestCase):
    """Tests for the StaticSet < operator."""


class TestStaticSetOrMethod(unittest.TestCase):
    """Tests for the StaticSet | operator."""


class TestStaticSetReprMethod(unittest.TestCase):
    """Tests for repr(StaticSet)."""


class TestStaticSetSubMethod(unittest.TestCase):
    """Tests for the StaticSet - operator."""


class TestStaticSetXorMethod(unittest.TestCase):
    """Tests for the StaticSet ^ operator."""


class TestStaticSetAddMethod(unittest.TestCase):
    """Tests for StaticSet.add."""


class TestStaticSetClearMethod(unittest.TestCase):
    """Tests for StaticSet.clear."""


class TestStaticSetCopyMethod(unittest.TestCase):
    """Tests for StaticSet.copy."""


class TestStaticSetDifferenceMethod(unittest.TestCase):
    """Tests for StaticSet.difference."""


class TestStaticSetDifferennceUpdateMethod(unittest.TestCase):
    """Tests for StaticSet.difference_update."""


class TestStaticSetDiscardMethod(unittest.TestCase):
    """Tests for StaticSet.discard."""


class TestStaticSetIntersectionMethod(unittest.TestCase):
    """Tests for StaticSet.intersction."""


class TestStaticSetIntersectionUpdateMethod(unittest.TestCase):
    """Tests for StaticSet.intersection_update."""


class TestStaticSetRemoveMethod(unittest.TestCase):
    """Tests for StaticSet.remove."""


class TestStaticSetUnionMethod(unittest.TestCase):
    """Tests for StaticSet.union."""


class TestStaticSetUpdateMethod(unittest.TestCase):
    """Tests for StaticSet.update."""


if __name__ == "__main__":
    unittest.main()
