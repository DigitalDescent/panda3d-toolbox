"""
Tests for panda3d_toolbox.prc module.

These tests exercise the wrapper functions around Panda3D's ConfigVariable system.
"""

import os

import pytest

from panda3d_toolbox import prc


# ---------------------------------------------------------------------------
# Basic get / set round-trips
# ---------------------------------------------------------------------------

class TestPrcStringRoundTrip:

    def test_set_and_get_string(self):
        prc.set_prc_string("test-string-key", "hello")
        assert prc.get_prc_string("test-string-key", "") == "hello"

    def test_get_string_default(self):
        result = prc.get_prc_string("nonexistent-key-str", "default_val")
        assert result == "default_val"


class TestPrcBoolRoundTrip:

    def test_set_and_get_bool(self):
        prc.set_prc_bool("test-bool-key", True)
        assert prc.get_prc_bool("test-bool-key", False) is True

    def test_get_bool_default(self):
        result = prc.get_prc_bool("nonexistent-key-bool", False)
        assert result is False


class TestPrcIntRoundTrip:

    def test_set_and_get_int(self):
        prc.set_prc_int("test-int-key", 42)
        assert prc.get_prc_int("test-int-key", 0) == 42

    def test_get_int_default(self):
        result = prc.get_prc_int("nonexistent-key-int", 99)
        assert result == 99

    def test_get_int_none_default_coerced_to_zero(self):
        result = prc.get_prc_int("nonexistent-key-int2", None)
        assert result == 0


class TestPrcDoubleRoundTrip:

    def test_set_and_get_double(self):
        prc.set_prc_double("test-double-key", 3.14)
        assert abs(prc.get_prc_double("test-double-key", 0.0) - 3.14) < 0.001

    def test_get_double_default(self):
        result = prc.get_prc_double("nonexistent-key-dbl", 1.5)
        assert result == 1.5


# ---------------------------------------------------------------------------
# load_prc_file_data
# ---------------------------------------------------------------------------

class TestLoadPrcFileData:

    def test_load_data_sets_value(self):
        prc.load_prc_file_data("test-loaded-key hello-world", label="test")
        assert prc.get_prc_string("test-loaded-key", "") == "hello-world"

    def test_load_headless_prc_data(self):
        prc.load_headless_prc_data()
        assert prc.get_prc_string("window-type", "") == "none"


# ---------------------------------------------------------------------------
# load_prc_file
# ---------------------------------------------------------------------------

class TestLoadPrcFile:

    def test_load_missing_file_raises(self):
        # Panda3D's notify.error raises an Exception for missing non-optional files
        with pytest.raises(Exception):
            prc.load_prc_file("this_file_does_not_exist.prc")

    def test_load_missing_optional_returns_false(self):
        result = prc.load_prc_file("this_file_does_not_exist.prc", optional=True)
        assert result is False

    def test_load_prc_file_data_equivalent(self):
        # Instead of loading from a temp file (which VFS can't see), verify
        # load_prc_file_data works as the underlying mechanism
        prc.load_prc_file_data("test-file-equiv-key 12345", label="test-file")
        assert prc.get_prc_string("test-file-equiv-key", "") == "12345"


# ---------------------------------------------------------------------------
# has_prc_key
# ---------------------------------------------------------------------------

class TestHasPrcKey:

    def test_has_key_after_set(self):
        prc.set_prc_string("has-key-test", "yes")
        assert prc.has_prc_key("has-key-test") is True

    def test_has_key_missing(self):
        assert prc.has_prc_key("definitely-not-set-zzzz") is False


# ---------------------------------------------------------------------------
# get_launch_* (environment variable override)
# ---------------------------------------------------------------------------

class TestLaunchHelpers:

    def test_get_launch_string_from_env(self, monkeypatch):
        # get_snake_case keeps hyphens, so env key is "MY-APP-NAME"
        monkeypatch.setenv("MY-APP-NAME", "OverriddenName")
        result = prc.get_launch_string("my-app-name", "default")
        assert result == "OverriddenName"

    def test_get_launch_string_default(self):
        result = prc.get_launch_string("unset-launch-str-zzz", "fallback")
        assert result == "fallback"

    def test_get_launch_int_from_env(self, monkeypatch):
        monkeypatch.setenv("MY-PORT", "8080")
        result = prc.get_launch_int("my-port", 3000)
        assert result == 8080

    def test_get_launch_double_from_env(self, monkeypatch):
        monkeypatch.setenv("MY-RATE", "2.5")
        result = prc.get_launch_double("my-rate", 1.0)
        assert abs(result - 2.5) < 0.001


# ---------------------------------------------------------------------------
# set_prc_value / get_prc_value  (generic helpers)
# ---------------------------------------------------------------------------

class TestGenericPrcValue:

    def test_set_and_get_via_generic(self):
        # First set a typed value so the type is known
        prc.set_prc_string("generic-test-key", "alpha")
        result = prc.get_prc_value("generic-test-key", "beta")
        assert result == "alpha"


# ---------------------------------------------------------------------------
# get_config_manager
# ---------------------------------------------------------------------------

class TestConfigManager:

    def test_returns_manager(self):
        mgr = prc.get_config_manager()
        assert mgr is not None
