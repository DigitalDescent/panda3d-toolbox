"""
Tests for panda3d_toolbox.logging module.

Tests cover the helper functions and the PythonLogHandler class.
Functions that interact heavily with Panda3D's Notify or the file system
are tested via mocking where appropriate.
"""

import io
import os
import pytest

from panda3d_toolbox import logging as p3d_logging


# ---------------------------------------------------------------------------
# get_notify_category / get_notify_categories
# ---------------------------------------------------------------------------

class TestNotifyCategories:

    def test_get_notify_category_creates(self):
        cat = p3d_logging.get_notify_category("unit-test-cat")
        assert cat is not None

    def test_get_notify_categories_returns_collection(self):
        cats = p3d_logging.get_notify_categories()
        assert cats is not None


# ---------------------------------------------------------------------------
# log helpers
# ---------------------------------------------------------------------------

class TestLogFunction:

    def test_log_info_does_not_raise(self):
        # Smoke test – just verify no exception
        p3d_logging.log("test message", name="test-log-cat", type="info")

    def test_log_with_invalid_type_raises(self):
        with pytest.raises(AssertionError):
            p3d_logging.log("msg", name="test-log-cat", type="nonexistent_level")


# ---------------------------------------------------------------------------
# condition_log
# ---------------------------------------------------------------------------

class TestConditionLog:

    def test_condition_true_calls_logger(self):
        calls = []

        class FakeLogger:
            def info(self, msg):
                calls.append(msg)

        p3d_logging.condition_log(FakeLogger(), True, "hello", "info")
        assert calls == ["hello"]

    def test_condition_false_skips_logger(self):
        calls = []

        class FakeLogger:
            def info(self, msg):
                calls.append(msg)

        p3d_logging.condition_log(FakeLogger(), False, "hello", "info")
        assert calls == []

    def test_condition_error(self):
        calls = []

        class FakeLogger:
            def error(self, msg):
                calls.append(msg)

        p3d_logging.condition_error(FakeLogger(), True, "err")
        assert calls == ["err"]

    def test_condition_warn(self):
        calls = []

        class FakeLogger:
            def warning(self, msg):
                calls.append(msg)

        p3d_logging.condition_warn(FakeLogger(), True, "warn")
        assert calls == ["warn"]

    def test_condition_info(self):
        calls = []

        class FakeLogger:
            def info(self, msg):
                calls.append(msg)

        p3d_logging.condition_info(FakeLogger(), True, "information")
        assert calls == ["information"]

    def test_condition_debug(self):
        calls = []

        class FakeLogger:
            def debug(self, msg):
                calls.append(msg)

        p3d_logging.condition_debug(FakeLogger(), True, "dbg")
        assert calls == ["dbg"]


# ---------------------------------------------------------------------------
# get_log_directory
# ---------------------------------------------------------------------------

class TestGetLogDirectory:

    def test_default_log_directory(self):
        log_dir = p3d_logging.get_log_directory()
        assert isinstance(log_dir, str)
        assert "logs" in log_dir


# ---------------------------------------------------------------------------
# PythonLogHandler
# ---------------------------------------------------------------------------

class TestPythonLogHandler:

    def test_write_goes_to_both_streams(self):
        original = io.StringIO()
        log_stream = io.StringIO()

        handler = p3d_logging.PythonLogHandler(original, log_stream)
        handler.write("hello world")

        assert original.getvalue() == "hello world"
        assert log_stream.getvalue() == "hello world"

    def test_flush_flushes_both(self):
        original = io.StringIO()
        log_stream = io.StringIO()

        handler = p3d_logging.PythonLogHandler(original, log_stream)
        # Should not raise
        handler.flush()

    def test_multiple_writes(self):
        original = io.StringIO()
        log_stream = io.StringIO()

        handler = p3d_logging.PythonLogHandler(original, log_stream)
        handler.write("one")
        handler.write("two")

        assert original.getvalue() == "onetwo"
        assert log_stream.getvalue() == "onetwo"
