"""
Tests for panda3d_toolbox.bootstrap module.
"""

import pytest

from panda3d_toolbox.bootstrap import (
    create_class_entry,
    create_singleton_entry,
    get_class_registry,
)
from panda3d_toolbox.registry import ClassRegistry


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_registry():
    """Reset the ClassRegistry singleton around each test."""
    ClassRegistry.reset_singleton(None)
    yield
    ClassRegistry.reset_singleton(None)


# ---------------------------------------------------------------------------
# create_class_entry
# ---------------------------------------------------------------------------

class TestCreateClassEntry:

    def test_basic_entry(self):
        entry = create_class_entry("mypackage.models.Player")
        class_name, object_path, meta = entry
        assert class_name == "Player"
        assert object_path == "mypackage.models.Player"
        assert meta == {}

    def test_entry_with_meta(self):
        entry = create_class_entry("mypackage.models.Player", meta={"role": "pc"})
        _, _, meta = entry
        assert meta == {"role": "pc"}

    def test_single_component_path(self):
        entry = create_class_entry("Player")
        class_name, object_path, _ = entry
        assert class_name == "Player"
        assert object_path == "Player"


# ---------------------------------------------------------------------------
# create_singleton_entry
# ---------------------------------------------------------------------------

class TestCreateSingletonEntry:

    def test_basic_entry(self):
        entry = create_singleton_entry("mypackage.managers.AudioManager")
        module_path, class_name, meta = entry
        assert module_path == "mypackage.managers"
        assert class_name == "AudioManager"
        assert meta == {}

    def test_entry_with_meta(self):
        entry = create_singleton_entry("mypackage.managers.AudioManager", meta={"priority": 1})
        _, _, meta = entry
        assert meta == {"priority": 1}


# ---------------------------------------------------------------------------
# get_class_registry
# ---------------------------------------------------------------------------

class TestGetClassRegistry:

    def test_returns_class_registry_instance(self):
        reg = get_class_registry()
        assert isinstance(reg, ClassRegistry)

    def test_returns_same_instance_twice(self):
        a = get_class_registry()
        b = get_class_registry()
        assert a is b
