"""
Tests for panda3d_toolbox.runtime module.
"""

import builtins
import sys

import pytest

from panda3d_toolbox import runtime


# ---------------------------------------------------------------------------
# Environment detection helpers
# ---------------------------------------------------------------------------

class TestIsVenv:

    def test_detects_real_prefix(self, monkeypatch):
        monkeypatch.setattr(sys, "real_prefix", "/usr", raising=False)
        assert runtime.is_venv() is True

    def test_detects_base_prefix_mismatch(self, monkeypatch):
        if hasattr(sys, "real_prefix"):
            monkeypatch.delattr(sys, "real_prefix")
        monkeypatch.setattr(sys, "base_prefix", "/different")
        monkeypatch.setattr(sys, "prefix", "/current")
        assert runtime.is_venv() is True

    def test_no_venv(self, monkeypatch):
        if hasattr(sys, "real_prefix"):
            monkeypatch.delattr(sys, "real_prefix")
        monkeypatch.setattr(sys, "base_prefix", sys.prefix)
        assert runtime.is_venv() is False


class TestIsInteractive:

    def test_interactive_when_ps1_and_ps2(self, monkeypatch):
        monkeypatch.setattr(sys, "ps1", ">>> ", raising=False)
        monkeypatch.setattr(sys, "ps2", "... ", raising=False)
        assert runtime.is_interactive() is True

    def test_not_interactive(self, monkeypatch):
        if hasattr(sys, "ps1"):
            monkeypatch.delattr(sys, "ps1")
        assert runtime.is_interactive() is False


class TestBuildDetection:

    def test_is_production_opposite_of_developer(self):
        assert runtime.is_production_build() != runtime.is_developer_build()

    def test_is_built_executable_matches_panda3d_build(self):
        assert runtime.is_built_executable() == runtime.is_panda3d_build()


# ---------------------------------------------------------------------------
# Dynamic attribute access (has_*, get_*, set_*)
# ---------------------------------------------------------------------------

class TestDynamicAttributes:

    def test_set_and_get(self):
        runtime.set_foo("bar")
        assert runtime.get_foo() == "bar"
        assert runtime.has_foo() is True

        # Clean up
        runtime.set_foo(None)

    def test_has_returns_false_for_undefined(self):
        assert runtime.has_zzz_undefined() is False

    def test_get_returns_none_for_undefined(self):
        assert runtime.get_zzz_undefined() is None

    def test_getattr_raises_for_unknown_key(self):
        with pytest.raises(AttributeError):
            runtime.xyz  # not has_/get_/set_ prefix and not a builtin


# ---------------------------------------------------------------------------
# executable_name
# ---------------------------------------------------------------------------

class TestExecutableName:

    def test_executable_name_is_string(self):
        assert isinstance(runtime.executable_name, str)
        assert len(runtime.executable_name) > 0
