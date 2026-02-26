"""
Tests for panda3d_toolbox.application module.

The Application class requires a Panda3D ShowBase, which needs a graphics
context. These tests focus on the parts that can be exercised in a headless /
windowless environment using load_headless_prc_data, plus unit-level tests
for helper methods.
"""

import builtins
from enum import IntEnum

import pytest

from panda3d_toolbox import prc
from panda3d_toolbox.application import Application, HeadlessApplication


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def headless_app():
    """Create a HeadlessApplication for testing.

    HeadlessApplication sets window-type=none so no GPU/display is needed.
    """
    prc.load_prc_file_data("window-type none\naudio-library-name null\naudio-active false", label="test-headless")
    app = HeadlessApplication()
    yield app
    app.destroy()


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestHeadlessApplicationConstruction:

    def test_creates_successfully(self, headless_app):
        assert headless_app is not None

    def test_exit_code_defaults_to_zero(self, headless_app):
        assert headless_app.exit_code == 0

    def test_dev_flag_set(self, headless_app):
        assert hasattr(builtins, "__dev__")


# ---------------------------------------------------------------------------
# set_exit_code
# ---------------------------------------------------------------------------

class TestSetExitCode:

    def test_set_exit_code_int(self, headless_app):
        headless_app.set_exit_code(42)
        assert headless_app.exit_code == 42

    def test_set_exit_code_enum(self, headless_app):
        class ExitCode(IntEnum):
            SUCCESS = 0
            FAILURE = 1

        headless_app.set_exit_code(ExitCode.FAILURE)
        assert headless_app.exit_code == 1


# ---------------------------------------------------------------------------
# set_exit_callback
# ---------------------------------------------------------------------------

class TestSetExitCallback:

    def test_sets_callback(self, headless_app):
        def on_exit():
            pass

        headless_app.set_exit_callback(on_exit)
        assert headless_app.exitFunc is on_exit

    def test_rejects_non_callable(self, headless_app):
        with pytest.raises(AssertionError):
            headless_app.set_exit_callback("not callable")


# ---------------------------------------------------------------------------
# Window helpers (no-op when win is None)
# ---------------------------------------------------------------------------

class TestWindowlessHelpers:

    def test_set_window_title_noop(self, headless_app):
        # Should not raise even though there is no window
        headless_app.set_window_title("Test")

    def test_set_window_dimensions_noop(self, headless_app):
        headless_app.set_window_dimensions((0, 0), (800, 600))

    def test_get_window_dimensions_returns_defaults(self, headless_app):
        origin, size = headless_app.get_window_dimensions()
        assert origin == (-1, -1)
        assert size == (-1, -1)

    def test_set_clear_color_noop(self, headless_app):
        headless_app.set_clear_color((0, 0, 0, 1))


# ---------------------------------------------------------------------------
# is_oobe
# ---------------------------------------------------------------------------

class TestIsOobe:

    def test_default_false(self, headless_app):
        assert headless_app.is_oobe() is False
