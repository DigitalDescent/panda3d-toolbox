"""
Tests for panda3d_toolbox.registry module.
"""

import pytest

from panda3d_toolbox.registry import ClassRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def registry():
    """Provide a fresh ClassRegistry for each test."""
    ClassRegistry.reset_singleton(None)
    reg = ClassRegistry.instantiate_singleton()
    yield reg
    ClassRegistry.reset_singleton(None)


# A simple class we can register by module path
class _DummyClass:
    """Dummy for registry import tests."""
    pass


DUMMY_MODULE_PATH = f"{__name__}._DummyClass"


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:

    def test_register_class(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        assert registry.is_registered("_DummyClass")

    def test_register_class_alias(self, registry):
        registry.register_class_alias("Alias", "_DummyClass", DUMMY_MODULE_PATH)
        assert registry.is_registered("Alias")
        assert not registry.is_registered("_DummyClass")

    def test_duplicate_register_is_noop(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        # Registering again should not raise, just warn
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        assert registry.is_registered("_DummyClass")

    def test_unregister_class(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        registry.unregister_class("_DummyClass")
        assert not registry.is_registered("_DummyClass")

    def test_unregister_missing_class_is_noop(self, registry):
        # Should not raise
        registry.unregister_class("DoesNotExist")


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

class TestRetrieval:

    def test_get_class_returns_class(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        cls = registry.get_class("_DummyClass")
        assert cls is _DummyClass

    def test_get_class_unknown_returns_none(self, registry):
        result = registry.get_class("Unknown")
        assert result is None


# ---------------------------------------------------------------------------
# Batch registration
# ---------------------------------------------------------------------------

class TestBatchRegistration:

    def test_batch_register_classes(self, registry):
        class_list = [
            ("_DummyClass", DUMMY_MODULE_PATH, {}),
        ]
        registry.batch_register_classes(class_list)
        assert registry.is_registered("_DummyClass")

    def test_batch_register_with_meta_list(self, registry):
        class_list = [
            ("_DummyClass", DUMMY_MODULE_PATH, {}),
        ]
        meta_list = [
            ("_DummyClass", "category", "test"),
        ]
        registry.batch_register_classes(class_list, meta_list)
        assert registry.get_class_meta("_DummyClass", "category") == "test"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

class TestMetadata:

    def test_set_and_get_meta(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH, tag="value")
        assert registry.get_class_meta("_DummyClass", "tag") == "value"

    def test_get_all_meta(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH, a=1, b=2)
        meta = registry.get_class_meta("_DummyClass")
        assert meta == {"a": 1, "b": 2}

    def test_get_meta_default(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        result = registry.get_class_meta("_DummyClass", "missing", default="fallback")
        assert result == "fallback"

    def test_set_meta_on_registered_class(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        registry.set_class_meta("_DummyClass", "key", "val")
        assert registry.get_class_meta("_DummyClass", "key") == "val"

    def test_set_meta_on_unregistered_class_is_noop(self, registry):
        # Should not raise
        registry.set_class_meta("NoSuchClass", "key", "val")

    def test_get_meta_on_unregistered_class_returns_none(self, registry):
        result = registry.get_class_meta("NoSuchClass", "key")
        assert result is None


# ---------------------------------------------------------------------------
# Iteration
# ---------------------------------------------------------------------------

class TestIteration:

    def test_iter_yields_registered_classes(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        items = list(registry)
        assert len(items) == 1
        name, data = items[0]
        assert name == "_DummyClass"

    def test_classes_property(self, registry):
        registry.register_class("_DummyClass", DUMMY_MODULE_PATH)
        assert "_DummyClass" in registry.classes
