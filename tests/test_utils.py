"""
Tests for panda3d_toolbox.utils module.

Covers the pure-Python utility functions that don't require a running
Panda3D ShowBase instance. Functions that depend on runtime.base / task_mgr
are tested with lightweight mocks where feasible.
"""

import math
import datetime
import inspect

import pytest

from panda3d.core import Vec3
from panda3d_toolbox import utils


# ---------------------------------------------------------------------------
# String conversion
# ---------------------------------------------------------------------------

class TestGetSnakeCase:

    def test_camel_to_snake(self):
        assert utils.get_snake_case("CamelCase") == "camel_case"

    def test_already_snake(self):
        assert utils.get_snake_case("already_snake") == "already_snake"

    def test_single_word(self):
        assert utils.get_snake_case("Word") == "word"

    def test_custom_splitter(self):
        assert utils.get_snake_case("CamelCase", splitter="-") == "camel-case"

    def test_multiple_uppercase(self):
        assert utils.get_snake_case("HTMLParser") == "h_t_m_l_parser"


class TestGetCamelCase:

    def test_snake_to_camel(self):
        assert utils.get_camel_case("my_variable") == "MyVariable"

    def test_single_word(self):
        assert utils.get_camel_case("word") == "Word"

    def test_already_capitalized(self):
        result = utils.get_camel_case("My_Variable")
        assert result == "MyVariable"


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

class TestGetTimeAsString:

    def test_without_seconds(self):
        result = utils.get_time_as_string(seconds=False)
        assert len(result) == 5  # HH:MM
        assert ":" in result

    def test_with_seconds(self):
        result = utils.get_time_as_string(seconds=True)
        assert len(result) == 8  # HH:MM:SS
        assert result.count(":") == 2


# ---------------------------------------------------------------------------
# is_awaitable_function
# ---------------------------------------------------------------------------

class TestIsAwaitableFunction:

    def test_sync_function(self):
        def sync():
            pass
        assert utils.is_awaitable_function(sync) is False

    def test_async_function(self):
        async def coro():
            pass
        assert utils.is_awaitable_function(coro) is True

    def test_non_callable_raises(self):
        with pytest.raises(AssertionError):
            utils.is_awaitable_function(42)


# ---------------------------------------------------------------------------
# perform_callback_on_condition
# ---------------------------------------------------------------------------

class TestPerformCallbackOnCondition:

    def test_true_condition_fires(self):
        results = []
        utils.perform_callback_on_condition(True, lambda: results.append(1))
        assert results == [1]

    def test_false_condition_skips(self):
        results = []
        utils.perform_callback_on_condition(False, lambda: results.append(1))
        assert results == []

    def test_passes_args(self):
        results = []
        utils.perform_callback_on_condition(True, lambda a, b: results.append(a + b), 2, 3)
        assert results == [5]


# ---------------------------------------------------------------------------
# diffs
# ---------------------------------------------------------------------------

class TestDiffs:

    def test_identical_lists(self):
        assert utils.diffs([1, 2, 3], [1, 2, 3]) == 0

    def test_all_different(self):
        assert utils.diffs([1, 2, 3], [4, 5, 6]) == 3

    def test_some_different(self):
        assert utils.diffs([1, 2, 3], [1, 5, 3]) == 1


# ---------------------------------------------------------------------------
# null_generator
# ---------------------------------------------------------------------------

class TestNullGenerator:

    def test_is_generator(self):
        gen = utils.null_generator()
        assert inspect.isgenerator(gen)

    def test_yields_nothing(self):
        assert list(utils.null_generator()) == []


# ---------------------------------------------------------------------------
# delegate
# ---------------------------------------------------------------------------

class TestDelegate:

    def test_sets_bound_method(self):
        class Target:
            pass

        class Source:
            def greet(self):
                return "hi"

        source = Source()
        target = Target()
        utils.delegate(target, source.greet)
        assert hasattr(target, "greet")
        assert target.greet() == "hi"


# ---------------------------------------------------------------------------
# foreach
# ---------------------------------------------------------------------------

class TestForeach:

    def test_applies_to_each_element(self):
        results = []
        utils.foreach([1, 2, 3], lambda x: results.append(x * 2))
        assert results == [2, 4, 6]

    def test_extra_args(self):
        results = []
        utils.foreach(["a", "b"], lambda x, suffix: results.append(x + suffix), "!")
        assert results == ["a!", "b!"]


# ---------------------------------------------------------------------------
# foreach_call_method_by_name
# ---------------------------------------------------------------------------

class TestForeachCallMethodByName:

    def test_calls_method(self):
        class Obj:
            def value(self):
                return 42

        result = utils.foreach_call_method_by_name([Obj(), Obj()], "value")
        assert result == [42, 42]

    def test_skips_missing_method(self):
        class Obj:
            pass

        result = utils.foreach_call_method_by_name([Obj()], "nonexistent")
        assert result == []


# ---------------------------------------------------------------------------
# has_attributes
# ---------------------------------------------------------------------------

class TestHasAttributes:

    def test_all_present(self):
        class Obj:
            a = 1
            b = 2

        assert utils.has_attributes(Obj(), ["a", "b"]) is True

    def test_some_missing(self):
        class Obj:
            a = 1

        assert utils.has_attributes(Obj(), ["a", "missing"]) is False


# ---------------------------------------------------------------------------
# to_unicode / utf8_capitalize / utf8_lower
# ---------------------------------------------------------------------------

class TestUnicodeHelpers:

    def test_to_unicode_str(self):
        assert utils.to_unicode("hello") == "hello"

    def test_to_unicode_bytes(self):
        result = utils.to_unicode(b"hello")
        assert result == "hello"


# ---------------------------------------------------------------------------
# set_setters_from_dict
# ---------------------------------------------------------------------------

class TestSetSettersFromDict:

    def test_sets_values(self):
        class Obj:
            def __init__(self):
                self._name = None
                self._score = None

            def set_name(self, v):
                self._name = v

            def set_score(self, v):
                self._score = v

        obj = Obj()
        utils.set_setters_from_dict(obj, {"name": "Alice", "score": 100})
        assert obj._name == "Alice"
        assert obj._score == 100

    def test_missing_setter_raises(self):
        class Obj:
            pass

        with pytest.raises(AttributeError):
            utils.set_setters_from_dict(Obj(), {"missing": 1})


# ---------------------------------------------------------------------------
# calculate_circle_edge_point
# ---------------------------------------------------------------------------

class TestCalculateCircleEdgePoint:

    def test_zero_degrees(self):
        center = Vec3(0, 0, 0)
        point = utils.calculate_circle_edge_point(center, 10.0, 0)
        assert abs(point.get_x() - 5.0) < 0.001
        assert abs(point.get_y() - 0.0) < 0.001
        assert abs(point.get_z() - 0.0) < 0.001

    def test_90_degrees(self):
        center = Vec3(0, 0, 0)
        point = utils.calculate_circle_edge_point(center, 10.0, 90)
        assert abs(point.get_x() - 0.0) < 0.001
        assert abs(point.get_y() - 5.0) < 0.001

    def test_with_offset_center(self):
        center = Vec3(10, 20, 5)
        point = utils.calculate_circle_edge_point(center, 4.0, 0)
        assert abs(point.get_x() - 12.0) < 0.001
        assert abs(point.get_y() - 20.0) < 0.001
        assert abs(point.get_z() - 5.0) < 0.001

    def test_180_degrees(self):
        center = Vec3(0, 0, 0)
        point = utils.calculate_circle_edge_point(center, 10.0, 180)
        assert abs(point.get_x() - (-5.0)) < 0.001
        assert abs(point.get_y() - 0.0) < 0.001


# ---------------------------------------------------------------------------
# build_screenshot_filename
# ---------------------------------------------------------------------------

class TestBuildScreenshotFilename:

    def test_returns_png_path(self, tmp_path):
        path = utils.build_screenshot_filename(directory=str(tmp_path))
        assert path.endswith(".png")
        assert str(tmp_path) in path

    def test_custom_format(self, tmp_path):
        path = utils.build_screenshot_filename(directory=str(tmp_path), format="jpg")
        assert path.endswith(".jpg")

    def test_custom_basename(self, tmp_path):
        path = utils.build_screenshot_filename(basename="capture", directory=str(tmp_path))
        assert "capture" in path


# ---------------------------------------------------------------------------
# snap_to_grid
# ---------------------------------------------------------------------------

class TestSnapToGrid:

    def test_snaps_correctly(self):
        result = utils.snap_to_grid((5.7, 3.2, 9.9), (2, 2, 5))
        assert result == (4, 2, 5)

    def test_already_on_grid(self):
        result = utils.snap_to_grid((4, 6, 10), (2, 3, 5))
        assert result == (4, 6, 10)
