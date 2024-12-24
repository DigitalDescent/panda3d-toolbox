"""
The runtime module provides a set of utility functions for determining the current
runtime environment of the application. This includes checking if the application
is running as a developer build, production build, or inside a virtual environment.
"""

import builtins
import sys as __sys
import os as __os

#----------------------------------------------------------------------------------------------------------------------------------#

def is_debugger() -> bool:
    """
    Returns true if the application is being run from a debugger.
    This method is designed to detect the debugging method used by VSCode.
    """

    return 'debugpy' in __sys.modules

def is_venv() -> bool:
    """
    Returns true if the application is being run inside
    a virtual environment
    """

    real_prefix = hasattr(__sys, 'real_prefix')
    base_prefix = hasattr(__sys, 'base_prefix') and __sys.base_prefix != __sys.prefix

    return real_prefix or base_prefix

def is_frozen() -> bool:
    """
    Returns true if the application is being run from within
    a frozen Python environment
    """

    import importlib
    spec = importlib.util.find_spec(__name__)
    return spec is not None and spec.origin is not None

def is_interactive() -> bool:
    """
    Returns true if the application is being run from an
    interactive command prompt
    """

    import sys
    return hasattr(sys, 'ps1') and hasattr(sys, 'ps2')


def is_dev() -> bool:
    """
    Returns true if the application is current
    running in developer mode
    """
    
    if hasattr(builtins, '__dev__'):
        return builtins.__dev__
    
    module = __get_module()
    if not module.has_dev():
        return False
    
    return module.get_dev()

def is_developer_build() -> bool:
    """
    Returns true if the application is currently
    running as a developer build
    """
    
    return (is_dev() or is_interactive() or is_debugger()) and not is_frozen()

def is_docker_build() -> bool:
    """
    Returns true if the application is currently 
    running inside a Docker container.
    """

    try:
        # Check for Docker-specific cgroup file
        with open('/proc/1/cgroup', 'r') as f:
            content = f.read()
            if 'docker' in content or 'containerd' in content:
                return True
    except FileNotFoundError:
        pass
    
    # Check for Docker environment file
    if __os.path.exists('/.dockerenv'):
        return True
    
    return False

def is_production_build() -> bool:
    """
    Returns true if the application is currently
    running as a production build
    """

    return not is_developer_build() or is_docker_build()

def get_repository() -> object:
    """
    Returns the Client repository object or AI repository object
    if either exist. Otherwise returning NoneType
    """

    module = __get_module()
    if not module.has_base():
        return None
    
    base = module.get_base()
    if hasattr(base, 'air'):
        return base.air
    elif hasattr(base, 'cr'):
        return base.cr
    else:
        raise AttributeError('base has no repository object')

def is_panda3d_build() -> bool:
    """
    Returns true if the application is currently
    running as a Panda3d build
    """

    return is_frozen()

def is_nuitka_build() -> bool:
    """
    Returns true if the application is currently
    running as a Nuitka build
    """

    return False #TODO: Implement Nuitka build detection

def is_built_executable() -> bool:
    """
    Returns true if the application is currently
    running as a built executable
    """

    panda_build = is_panda3d_build()
    nuitka_build = is_nuitka_build()

    return panda_build or nuitka_build

def get_base_executable_name() -> str:
    """
    Returns the base executable name
    """

    # If the script being run is a __main__.py file then our executable
    # name should be our parent directory name. This is also true if the application
    # is currently being run from a debugger such as the one included in VSCode.
    # Alternatively if APP_NAME is supplied as an environment variable then we should
    # use that as the base executable name.
    executable_name = __sys.argv[0]
    if executable_name.endswith('__main__.py') or is_debugger():
        # Check if the APP_NAME environment variable is set
        # and use that as the base executable name
        if __os.environ.get('APP_NAME', None) is not None:
            return __os.environ.get('APP_NAME')

        # Get the parent directory of the script being run and
        # make its name the executable name
        executable_path = __os.path.abspath(executable_name)
        executable_name = __os.path.dirname(executable_path)
        return executable_name
    else:
        # Get the base name of the executable. If the executable name is '-m'
        # then we should use the APP_NAME environment variable as the base name
        basename = __os.path.basename(executable_name)
        if basename == '-m':
            basename = __os.environ.get('APP_NAME', 'panda3d')

        # Remove the file extension from the basename and
        # return that as the base executable name
        basename = __os.path.splitext(basename)[0]
        return basename

executable_name = get_base_executable_name()

#----------------------------------------------------------------------------------------------------------------------------------#

def __get_module() -> object:
    """
    Returns the runtime module's object instance
    """

    return __sys.modules[__name__]

def __has_variable(variable_name: str) -> bool:
    """
    Returns true if the runtime module has the requested variable name defined.
    Is served out via the custom __getattr__ function as has_x() method names
    """

    module = __get_module()
    defined = hasattr(module, variable_name)
    found = False

    if defined:
        attr = getattr(module, variable_name)
        found = attr != None

    return found

def __get_variable(variable_name: str) -> object:
    """
    Returns the requested variable from the runtime module if it exists.
    Otherwise returning NoneType
    """

    if not __has_variable(variable_name):
        return None

    module = __get_module()
    return getattr(module, variable_name)

def __set_variable(variable_name: str, value: object) -> None:
    """
    Sets the requested variable in the runtime module
    """

    module = __get_module()
    setattr(module, variable_name, value)

def __getattr__(key: str) -> object:
    """
    Custom get attribute handler for allowing access to the has_x method names
    of the engine runtime module. Also exposes the builtins module
    for the legacy Panda3d builtins provided by the ShowBase instance
    """

    result = None
    is_has_method = key.startswith('has_')
    is_get_method = key.startswith('get_')
    is_set_method = key.startswith('set_')

    if len(key) > 4:
        variable_name = key[4:]
    else:
        variable_name = key

    if is_has_method:
        result = lambda: __has_variable(variable_name)
    elif is_get_method:
        result = lambda: __get_variable(variable_name)
    elif is_set_method:
        result = lambda value: __set_variable(variable_name, value)
    elif hasattr(builtins, key):
        result = getattr(builtins, key)

    if not result:
        raise AttributeError('runtime module has no attribute: %s' % key)

    return result

#----------------------------------------------------------------------------------------------------------------------------------#