"""
"""

import re

# -----------------------------------------------------------------

_SNAKE_NAME_RE = re.compile('(?<!^)(?=[A-Z])')

# -----------------------------------------------------------------

def get_snake_case(text: str, splitter='_') -> str:
    """
    Returns the snake case version of the requested string
    """

    return _SNAKE_NAME_RE.sub(splitter, text).lower()

def get_camel_case(text: str, splitter='_') -> str:
    """
    Returns the camel case version of the requested string
    """

    return ''.join(x.capitalize() or splitter for x in text.split(splitter))

def get_environ_name(text: str) -> str:
    """
    Returns the environment variable name for the requested string
    """

    text = text.replace('-', '_')
    return get_snake_case(text).upper()

def to_unicode(string: str) -> str:
    """
    """

    if type(string) == str:
        return string

    try:
        return str(string.decode('utf-8'))
    except UnicodeError:
        return ''

def utf8_capitalize(string: str) -> str:
    """
    """

    return to_unicode(string).capitalize().encode('utf-8')

def utf8_lower(string: str) -> str:
    """
    """

    return to_unicode(string).lower().encode('utf-8')
