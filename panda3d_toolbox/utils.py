"""
"""

import os
import sys
import datetime
import itertools
import datetime
import gc
import importlib

from functools import reduce

from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d_toolbox import runtime

__notify = directNotify.newCategory('utilities')

def get_time_as_string(seconds: bool = False) -> str:
    """
    Returns the current time as a string
    """

    now = datetime.datetime.now()
    output = None
    if seconds:
        output = '%02d:%02d:%02d' % (now.hour, now.minute, now.second)
    else:
        output = '%02d:%02d' % (now.hour, now.minute)

    return output

def diffs(lst1, lst2):
    """
    """

    return reduce(lambda x, y: x + y, itertools.starmap(lambda e1, e2: int(not e1 == e2), list(zip(lst1, lst2))))

def delegate(self, call) -> None:
    """
    """

    func_name = call.__func__.__name__
    setattr(self, func_name, call)

def null_generator():
    """
    Defines a null yield generator
    """

    if False:
        yield

def foreach(sequence: list, callable: object, *args, **kwargs) -> None:
    """
    Iterates through a sequence performing a callback on each element
    """

    for element in sequence:
        callable(element, *args, **kwargs)

def foreach_call_method_by_name(sequence: list, method_name: str, *args, **kw) -> list:
    """
    """

    results = []
    for element in sequence:
        callable = getattr(element, method_name, None)
        if callable:
            results.append(callable(*args, **kw))

    return results

def write_ini_file(filepath: str, input: object, output: object, template: str = '[Configuration]\n\n[Model]\n%(output)s: %(input)s\n') -> None:
    """
    Writes a new ini file to the requested output path location
    """

    __notify.info('write_ini_file: Creating ini file for "%s"... ' % input)
    fh = open(filepath, 'w')
    fh.write(template % {'input': input, 'output': output})
    fh.close()

def get_refcounts() -> list:
    """
    Returns a list of all references in the application
    """

    d = {}
    for m in list(sys.modules.values()):
        for sym in dir(m):
            o = getattr(m, sym)
            if type(o) is type:
                d[o] = sys.getrefcount(o)

    pairs = [(refcount, cls) for cls, refcount in list(d.items())]
    pairs.sort(reverse=True)

    return pairs

def get_all_references_of_type(t: object) -> list:
    """
    """

    result = []
    for r in gc.get_referrers(t):
        if isinstance(r, t):
            result.append(r)

    return result

def print_refcounts(max_refcounts: int = None) -> None:
    """
    """

    refcount_list = get_refcounts()
    if max_refcounts is not None:
        refcount_list = refcount_list[max_refcounts]
    
    for n, c in refcount_list:
        print('%10d %s (%s) instances: %d' % (
            n, c.__name__, str(c), len(get_all_references_of_type(c))))

def print_unreachable_garbage() -> None:
    """
    """

    garbage_list = gc.garbage
    if len(garbage_list) == 0:
        print('No garbage found')
    else:
        print('%d object in garbage found: ' % len(garbage_list))
        for garbage in garbage_list:
            print(str(garbage))

def set_if_not_set(dict: dict, other: dict) -> None:
    """
    Sets the values of a dictionary from another dictionary if the key
    is not already set.
    """

    for key, value in other.items():
        if key not in dict or dict[key] == None:
            dict[key] = value

def get_module_path(module_name):
    """
    Get the file path of a Python module, whether local or installed via pip.

    Args:
        module_name (str): The name of the module to locate.

    Returns:
        str: The path to the module's file, or None if the module cannot be found.
    """
    try:
        # Check if the module is already imported
        if module_name in sys.modules:
            module = sys.modules[module_name]
            return getattr(module, '__file__', None)

        # Try to find the module spec
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return os.path.abspath(spec.origin)
        else:
            return None
    except ModuleNotFoundError:
        return None