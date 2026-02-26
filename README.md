# Panda3D Toolbox

[![Build, Test, and Publish](https://github.com/thetestgame/panda3d-toolbox/actions/workflows/main.yml/badge.svg)](https://github.com/thetestgame/panda3d-toolbox/actions/workflows/main.yml)
![PyPI - Version](https://img.shields.io/pypi/v/panda3d-toolbox)
![License](https://img.shields.io/github/license/thetestgame/panda3d-toolbox)

A collection of utilities, base classes, and patterns for building applications with the [Panda3D](https://www.panda3d.org/) game engine. Provides a standardized application framework, runtime configuration helpers, logging integration, a singleton pattern, a class registry, and more.

## Features

- **Application Framework** — `Application` and `HeadlessApplication` base classes extending Panda3D's `ShowBase` with built-in PRC configuration loading, virtual file system setup, window management helpers, antialiasing control, and graceful error handling.
- **PRC Configuration Wrapper** — A comprehensive wrapper around Panda3D's runtime configuration system for loading `.prc` files and data, and reading/writing typed config values (`bool`, `int`, `double`, `string`, `color`, `filename`, `search_path`, etc.). Includes `get_launch_*` helpers that resolve values from environment variables first, then PRC.
- **Logging Utilities** — Functions for writing to Panda3D's `DirectNotify` categories, conditional logging, log file output that merges Python's `stdout`/`stderr` with Panda3D's `Notify` stream into a single timestamped file.
- **Singleton Pattern** — A reusable `Singleton` base class with `instantiate_singleton`, `get_singleton`, `reset_singleton`, and `is_instantiated` class methods.
- **Class Registry** — A singleton-based `ClassRegistry` for registering, retrieving, and querying classes with metadata. Supports lazy module importing, aliased registration, batch registration, and metadata queries.
- **Bootstrap Helpers** — Functions for batch-instantiating singletons and registering classes during module initialization.
- **Runtime Introspection** — Utilities for detecting virtual environments, frozen/compiled builds, interactive sessions, developer vs. production mode, and dynamic attribute access (`has_*`, `get_*`, `set_*`) on the runtime module.
- **General Utilities** — String case conversion, URL opening, time formatting, async task helpers, task manager wrappers, math and geometry helpers, file system operations, and more.

## Installation

```bash
pip install panda3d-toolbox
```

### Requirements

- Python 3
- [panda3d](https://pypi.org/project/panda3d/)
- [panda3d-vfs](https://pypi.org/project/panda3d-vfs/)

## Quick Start

### Creating an Application

```python
from panda3d_toolbox.application import Application

class MyGame(Application):
    def __init__(self):
        super().__init__()
        self.set_window_title("My Panda3D Game")

app = MyGame()
exit_code = app.execute()
```

### Headless Application

```python
from panda3d_toolbox.application import HeadlessApplication

class MyServer(HeadlessApplication):
    def __init__(self):
        super().__init__()
        # No window or audio — ideal for game servers

server = MyServer()
server.execute()
```

### Working with PRC Configuration

```python
from panda3d_toolbox import prc

# Load a PRC file
prc.load_prc_file("config/game.prc")

# Load inline PRC data
prc.load_prc_file_data("window-title My Game\nfullscreen false", label="game-config")

# Read and write config values
title = prc.get_prc_string("window-title", "Default Title")
prc.set_prc_bool("fullscreen", True)

# Retrieve values with environment variable override
# If APP_PORT env var is set it takes precedence over the PRC value
port = prc.get_launch_int("app-port", 7199)
```

### Using the Singleton Pattern

```python
from panda3d_toolbox.singleton import Singleton

class GameManager(Singleton):
    def __init__(self):
        super().__init__()
        self.score = 0

# Create or retrieve the singleton instance
manager = GameManager.instantiate_singleton()
same_manager = GameManager.get_singleton()
```

### Logging

```python
from panda3d_toolbox import logging

# Write to a named Panda3D notify category
logging.log("Player connected", name="network", type="info")

# Convenience helpers
logging.log_info("Loading assets...")
logging.log_error("Failed to load model")

# Conditional logging
logging.condition_warn(logger, health < 10, "Player health is critically low")

# Configure file-based logging (merges Python + Panda3D output)
logging.configure_log_file()
```

### Class Registry & Bootstrap

```python
from panda3d_toolbox.bootstrap import bootstrap_module, create_class_entry, create_singleton_entry

# Register classes and singletons during module setup
bootstrap_module(
    class_list=[
        create_class_entry("mypackage.player.Player"),
    ],
    singleton_list=[
        create_singleton_entry("mypackage.managers.AudioManager"),
    ],
)
```

## Module Reference

| Module | Description |
|---|---|
| `application` | `Application` and `HeadlessApplication` base classes for windowed and headless Panda3D apps |
| `prc` | Wrapper for Panda3D's PRC runtime configuration (load, get, set) |
| `logging` | Panda3D notify logging utilities, conditional logging, and log file configuration |
| `singleton` | Reusable `Singleton` base class |
| `registry` | `ClassRegistry` singleton for class registration, retrieval, and metadata queries |
| `bootstrap` | Batch class registration and singleton instantiation helpers |
| `runtime` | Runtime state and environment introspection (frozen, venv, dev mode, etc.) |
| `utils` | General-purpose utilities (string conversion, tasks, math, file ops, etc.) |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
