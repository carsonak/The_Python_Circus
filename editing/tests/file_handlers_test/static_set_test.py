#!/usr/bin/env python
"""Tests for static test."""

from typing import Callable, Generator, Iterator, Hashable
import unittest

from file_handlers.static_set import StaticSet

HASHABLES_IN_TUPLES: dict[type, tuple[Hashable, ...]] = {
    type: (type, int, dict),
    type(None): (None, None, None),
    str: tuple("(💖👅💖)"),
    bytes: (b"A", b"B", b"C"),
    int: (-6, 9, 0, 6, -9),
    bool: (True, False),
    float: (99.9, 99.99, 1/3, float("inf"), float("nan")),
    frozenset: (frozenset("I"), frozenset("C"), frozenset("E")),
    tuple: (("(", ")"), (1, 1), ("(", ")")),
    type(range(1)): (range(-5, 1), range(0, 6, -1), range(6, 11, -1)),
}
ITERABLE_GENERATORS: dict[type, Callable] = {
    list: lambda x: list(x),
    tuple: lambda x: tuple(x),
    set: lambda x: set(x),
    frozenset: lambda x: frozenset(x),
    bytes: lambda x: bytes(str(x), encoding="utf-8"),
    str: lambda x: str(x),
    Iterator: lambda x: iter(x),
    Generator: lambda x: (y for y in x),
    StaticSet: lambda x: StaticSet(x),
}

NOT_HASHABLES_IN_TUPLES: dict[type, tuple] = {
    set: (set(), {1}),
    list: (list(), [1]),
    dict: (dict(), {1: "One"}),
    bytearray: (bytearray(), bytearray(b"xyz")),
}
NOT_ITERABLES: dict[type, object] = {
    int: 1, float: 22/7, bool: True, type: type,
    type(lambda x: x): lambda x: x,
}


class TestInitStaticSet(unittest.TestCase):
    """Tests for initialising an Instance."""

    def setUp(self) -> None:
        """Setup."""

    def tearDown(self) -> None:
        """Teardown."""

    def test_init_with_no_args_expect_items_is_empty_set(self) -> None:
        """Check initiliasing without arguments returns instance."""
        ss: StaticSet[Hashable] = StaticSet()

        self.assertIsInstance(ss._items, set)
        self.assertFalse(bool(ss._items))

    def test_init_with_no_args_expect_oftype_is_set_to_none(self) -> None:
        """Check initiliasing without arguments returns instance."""
        ss: StaticSet[Hashable] = StaticSet()

        self.assertIsNone(ss.oftype)

    def test_init_with_different_iterables_and_hashables_expect_items_is_initialised(self) -> None:  # noqa: E501,B950
        """Check initialising with a iterable of hashables returns instance."""
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                for h_type, h in HASHABLES_IN_TUPLES.items():
                    if iter_type is str:
                        h_type = str
                    elif iter_type is bytes:
                        h_type = int

                    with self.subTest(hashables=h, hashable_type=h_type):
                        ss: StaticSet[Hashable] = StaticSet(func(h))

                        self.assertIsInstance(ss._items, set)
                        self.assertTrue(bool(ss._items))

    def test_init_with_different_iterables_and_hashables_expect_oftype_is_set_correctly(self) -> None:  # noqa: E501,B950
        """Check initialising with a iterable of hashables returns instance."""
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                for h_type, h in HASHABLES_IN_TUPLES.items():
                    if iter_type is str:
                        h_type = str
                    elif iter_type is bytes:
                        h_type = int

                    with self.subTest(hashables=h, hashable_type=h_type):
                        ss: StaticSet[Hashable] = StaticSet(func(h))

                        self.assertEqual(ss.oftype, h_type)

    def test_init_with_empty_self_expect_a_new_instance(self) -> None:
        """Check initialising with StaticSet instance returns new instance."""
        ss1: StaticSet = StaticSet()
        ss2: StaticSet = StaticSet(ss1)

        self.assertIsNot(ss1, ss2)
        self.assertFalse(bool(ss2._items))
        self.assertIsNone(ss2.oftype)

    def test_init_with_non_empty_self_expect_a_new_instance(self) -> None:
        """Check initialising with StaticSet instance returns new instance."""
        ss1: StaticSet = StaticSet((1, 11, 111, 1111))
        ss2: StaticSet = StaticSet(ss1)

        self.assertIsNot(ss1, ss2)
        self.assertTrue(bool(ss2._items))
        self.assertEqual(ss2.oftype, ss1.oftype)

    def test_init_with_unhashables_expect_typeerror(self) -> None:
        """Check initialising with non-hashables raises TypeError."""
        for nh_type, nh in NOT_HASHABLES_IN_TUPLES.items():
            with (
                self.subTest(unhashable_type=nh_type, unhashables=nh),
                self.assertRaises(TypeError)
            ):
                StaticSet(nh)

    def test_init_with_non_iterables_expect_typeerror(self) -> None:
        """Check initialising with none iterables raises TypeError."""
        for nit_type, nit in NOT_ITERABLES.items():
            with (
                self.subTest(object_type=nit_type, value=nit),
                self.assertRaises(TypeError)
            ):
                StaticSet(nit)  # type: ignore

    def test_init_with_mixed_types_expect_typeerror(self) -> None:
        """Check initiliasing with mixed types raises TypeError."""
        with self.assertRaises(TypeError):
            StaticSet(HASHABLES_IN_TUPLES[int] + HASHABLES_IN_TUPLES[float])


class TestAndStaticSet(unittest.TestCase):
    """Tests for the StaticSet & operator."""

    # empty & different iterables
    # # empty
    def test_empty_set_with_different_empty_iterables_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator with empty iterables."""
        empty_ss: StaticSet = StaticSet()
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                ss: StaticSet = empty_ss & func([])

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    # # One item
    def test_empty_set_with_different_iterables_with_one_item_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator with iterables of length = 1."""
        empty_ss: StaticSet = StaticSet()
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                ss: StaticSet = empty_ss & func([1])

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    # # Several items
    # # Include StaticSet too
    def test_empty_set_with_different_iterables_with_several_items_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator with iterables with several items."""
        empty_ss: StaticSet = StaticSet()
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                ss: StaticSet = empty_ss & func("1234")

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    # One item & different iterables
    # # ...
    def test_set_with_one_item_with_different_empty_iterables_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator with empty iterables."""
        one_ss: StaticSet = StaticSet([1])
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                ss: StaticSet = one_ss & func([])

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    def test_set_with_one_similar_item_expect_result_set_to_be_equal_to_original(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator when set with one item is compared."""
        for iter_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=iter_type, func=func):
                for h_type, h in HASHABLES_IN_TUPLES.items():
                    if iter_type is str:
                        h_type = str
                    elif iter_type is bytes:
                        h_type = int

                    with self.subTest(hashables=h, hashable_type=h_type):
                        one_ss: StaticSet = StaticSet(list(func(h))[:1])
                        ss: StaticSet = one_ss & func(h)

                        self.assertEqual(one_ss, ss)

    # Several items & different iterables
    # # ...
    def test_set_with_several_items_none_identical_to_iterable_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator when no identical items."""
        for it_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=it_type, func=func):
                several_ss: StaticSet = StaticSet(func(b"KLMNO"))
                ss: StaticSet = several_ss & func(b"PQRST")

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    def test_set_with_several_items_one_identical_to_iterable_expect_empty_set(self) -> None:  # noqa: E501,B950
        """Check behaviour of & operator when one identical item."""
        for it_type, func in ITERABLE_GENERATORS.items():
            with self.subTest(iterable_type=it_type, func=func):
                several_ss: StaticSet = StaticSet(func([*range(70, 76)]))
                ss: StaticSet = several_ss & func([*range(65, 70)])

                self.assertFalse(bool(ss._items))
                self.assertIsNone(ss.oftype)

    # TypeError: unhashables


class TestContainsStaticSet(unittest.TestCase):
    """Tests for StaticSet.__contains__."""

    # Empty
    def test_contains_with_empty_set_expect_false(self) -> None:
        """Check that in returns false when set is empty."""
        ss: StaticSet = StaticSet()

        self.assertNotIn(0, ss)
        self.assertNotIn("", ss)
        self.assertNotIn(False, ss)
        self.assertNotIn(set(), ss)
        self.assertNotIn(1, ss)
        self.assertNotIn(True, ss)

    # One item
    def test_contains_with_set_with_one_item_expect_true(self) -> None:
        """Check for the existence of the sole item in the set."""
        for hsh in HASHABLES_IN_TUPLES.values():
            with self.subTest(hashable=hsh[0]):
                ss = StaticSet((hsh[0],))

                self.assertIn(hsh[0], ss)

    # Several items
    def test_contains_with_set_with_several_items_expect_true_for_all(self) -> None:  # noqa: E501
        """Check for the existence of all items in the set."""
        for hsh in HASHABLES_IN_TUPLES.values():
            with self.subTest(tuple_of_hashables=hsh):
                ss = StaticSet(hsh)
                for i in hsh:
                    with self.subTest(hashable=i):
                        self.assertIn(i, ss)

    # TypeError unhashable
    def test_contains_an_unhashable_item_expect_typeerror(self) -> None:
        """Check that looking up unhashables raises TypeError."""
        with self.assertRaises(TypeError, msg="[] in StaticSet()"):
            _ = [] in StaticSet()  # type: ignore

        with self.assertRaises(
            TypeError,
            msg="StaticSet([3, 4]) in StaticSet({0, 2, 3, 4, 5})"
        ):
            _ = StaticSet([3, 4]) in StaticSet({0, 2, 3, 4, 5})

        with self.assertRaises(
                TypeError, msg='{"1", "2", "3"} in StaticSet("012345"'):
            _ = bytearray(b"123") in StaticSet(b"012345")  # type: ignore

        with self.assertRaises(TypeError, msg="{} in StaticSet((1, 2, 3))"):
            _ = {} in StaticSet((1, 2, 3))  # type: ignore

    def test_contains_a_set_type_expect_false(self) -> None:
        """Check that looking up a set type returns false."""
        ss = StaticSet({0, 1, 2, 3, 4, 5, 6, 7})

        self.assertNotIn({4, 2, 3}, ss)
        self.assertNotIn(frozenset([4, 3, 5, 6, 6, 7]), ss)


class TestEqualStaticSet(unittest.TestCase):
    """Tests for the StaticSet == operator."""

    # Empty == Empty

    # Empty == Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestIAndStaticSet(unittest.TestCase):
    """Tests for the StaticSet &= operator."""

    # Empty &= Empty

    # Empty &= Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestIOrStaticSet(unittest.TestCase):
    """Tests for the StaticSet |= operator."""

    # Empty |= Empty

    # Empty |= Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestISubStaticSet(unittest.TestCase):
    """Tests for the StaticSet -= operator."""

    # Empty -= Empty

    # Empty -= Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestIterStaticSet(unittest.TestCase):
    """Tests for iter(StaticSet)."""

    # Empty

    # Non-empty


class TestIXorStaticSet(unittest.TestCase):
    """Tests for the StaticSet ^= operator."""

    # Empty ^= Empty

    # Empty ^= Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestLessEqualStaticSet(unittest.TestCase):
    """Tests for the StaticSet <= operator."""

    # Empty <= Empty

    # Empty <= Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestLessStaticSet(unittest.TestCase):
    """Tests for the StaticSet < operator."""

    # Empty < Empty

    # Empty < Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestOrStaticSet(unittest.TestCase):
    """Tests for the StaticSet | operator."""

    # Empty | Empty

    # Empty | Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestReprStaticSet(unittest.TestCase):
    """Tests for repr(StaticSet)."""

    # Empty

    # Non-empty


class TestSubStaticSet(unittest.TestCase):
    """Tests for the StaticSet - operator."""

    # Empty - Empty

    # Empty - Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestXorStaticSet(unittest.TestCase):
    """Tests for the StaticSet ^ operator."""

    # Empty ^ Empty

    # Empty ^ Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestAddStaticSet(unittest.TestCase):
    """Tests for StaticSet.add."""

    # Add to empty from different iterables

    # Add to non-empty from different iterables

    # Add repeated items

    # TypeError: objects not the same type
    # # check parent classes and child classes

    # TypeError: not hashable


class TestClearStaticSet(unittest.TestCase):
    """Tests for StaticSet.clear."""

    # Empty

    # Non-empty


class TestCopyStaticSet(unittest.TestCase):
    """Tests for StaticSet.copy."""

    # Empty

    # Non-empty

    # Check Mutabilty


class TestDifferenceStaticSet(unittest.TestCase):
    """Tests for StaticSet.difference."""

    # Empty - Empty

    # Empty - Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestDifferennceUpdateStaticSet(unittest.TestCase):
    """Tests for StaticSet.difference_update."""

    # Empty -= Empty

    # Empty -= Non-empty
    # # Reverse should also be true
    # # Single vs Several iterables

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestDiscardStaticSet(unittest.TestCase):
    """Tests for StaticSet.discard."""

    # Empty

    # Non-empty

    # Non-existent object

    # TypeError: unhashable


class TestIntersectionStaticSet(unittest.TestCase):
    """Tests for StaticSet.intersction."""

    # Empty & Empty

    # Empty & Non-empty
    # # Reverse should also be true

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestIntersectionUpdateStaticSet(unittest.TestCase):
    """Tests for StaticSet.intersection_update."""

    # Empty &= Empty

    # Empty &= Non-empty
    # # Reverse should also be true
    # # Single vs Several iterables

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestRemoveStaticSet(unittest.TestCase):
    """Tests for StaticSet.remove."""

    # Empty

    # Non-empty

    # TypeError: unhashable

    # Keyerror: Non-existent object


class TestUnionStaticSet(unittest.TestCase):
    """Tests for StaticSet.union."""

    # Empty | Empty

    # Empty | Non-empty
    # # Reverse should also be true
    # # Single vs Several iterables

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


class TestUpdateStaticSet(unittest.TestCase):
    """Tests for StaticSet.update."""

    # Empty | Empty

    # Empty | Non-empty
    # # Reverse should also be true
    # # Single vs Several iterables

    # Similar items
    # # ...

    # Non-Similar items
    # # ...

    # TypeError: not a StaticSet


if __name__ == "__main__":
    unittest.main()
