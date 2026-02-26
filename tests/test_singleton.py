"""
Tests for panda3d_toolbox.singleton module.
"""

import pytest

from panda3d_toolbox.singleton import Singleton


# ---------------------------------------------------------------------------
# Helpers – fresh subclass per test to avoid cross-test pollution
# ---------------------------------------------------------------------------

def _make_singleton_class(name="TestSingleton"):
    """Return a new Singleton subclass so each test starts clean."""
    cls = type(name, (Singleton,), {"_singleton_instance": None})
    return cls


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSingletonInstantiation:
    """Verify the basic lifecycle of a Singleton."""

    def test_is_instantiated_false_initially(self):
        cls = _make_singleton_class()
        assert cls.is_instantiated() is False

    def test_instantiate_singleton_creates_instance(self):
        cls = _make_singleton_class()
        instance = cls.instantiate_singleton()
        assert instance is not None
        assert cls.is_instantiated() is True

    def test_get_singleton_returns_same_instance(self):
        cls = _make_singleton_class()
        a = cls.instantiate_singleton()
        b = cls.get_singleton()
        assert a is b

    def test_instantiate_singleton_is_idempotent(self):
        cls = _make_singleton_class()
        a = cls.instantiate_singleton()
        b = cls.instantiate_singleton()
        assert a is b

    def test_direct_constructor_raises_on_second_call(self):
        cls = _make_singleton_class()
        cls()
        with pytest.raises(RuntimeError):
            cls()

    def test_get_singleton_silent_returns_none(self):
        cls = _make_singleton_class()
        result = cls.get_singleton(silent=True)
        assert result is None


class TestSingletonReset:
    """Verify reset_singleton behaviour."""

    def test_reset_to_none_clears_instance(self):
        cls = _make_singleton_class()
        cls.instantiate_singleton()
        assert cls.is_instantiated() is True
        cls.reset_singleton(None)
        assert cls.is_instantiated() is False

    def test_reset_to_new_instance(self):
        cls = _make_singleton_class()
        first = cls.instantiate_singleton()
        # Manually create a second (bypass __init__ guard for reset test)
        second = object.__new__(cls)
        cls.reset_singleton(second)
        assert cls.get_singleton() is second
        assert cls.get_singleton() is not first

    def test_reset_calls_destroy_on_old_instance(self):
        destroyed = []

        cls = _make_singleton_class("DestroyTestSingleton")
        cls.destroy = lambda self: destroyed.append(id(self))

        old = cls.instantiate_singleton()
        old_id = id(old)

        new_inst = object.__new__(cls)
        cls.reset_singleton(new_inst)

        assert old_id in destroyed


class TestSingletonIsolation:
    """Separate subclasses should have independent singletons."""

    def test_independent_subclasses(self):
        cls_a = _make_singleton_class("A")
        cls_b = _make_singleton_class("B")

        a = cls_a.instantiate_singleton()
        b = cls_b.instantiate_singleton()

        assert a is not b
        assert cls_a.get_singleton() is a
        assert cls_b.get_singleton() is b
