"""
Shared pytest fixtures and configuration for panda3d-toolbox tests.
"""

import builtins
import pytest


@pytest.fixture(autouse=True)
def _ensure_dev_flag():
    """Ensure __dev__ is defined on builtins so runtime helpers don't fail."""
    if not hasattr(builtins, '__dev__'):
        builtins.__dev__ = True
    yield
