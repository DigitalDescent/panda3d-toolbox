"""
"""

import os
import sys
import datetime

from direct.directnotify.DirectNotifyGlobal import directNotify

from panda3d.core import Filename
from panda3d_toolbox import runtime

__notify = directNotify.newCategory('system')


def open_web_url(url: str) -> bool:
    """
    Attempts to open the website url. Returning true on sucess
    otherwise False on failure.
    """

    success = False
    if sys.platform == 'darwin':
        os.system('/usr/bin/open %s' % url)
    elif sys.platform == 'linux':
        import webbrowser
        webbrowser.open(url)
        success = True
    else:
        try:
            import webbrowser
            webbrowser.open(url)
            success = True
        except:
            os.system('explorer "%s"' % url)

    return success


def open_os_directory(path: str) -> bool:
    """
    Opens a directory path in the operation system's file explorer.
    Returning true on success, otherwise false.
    """

    success = False
    if sys.platform == 'darwin':
        __notify.warning('open_os_directory is not supported on platform: %s' % sys.platform)
    elif sys.platform == 'linux2' or sys.platform == 'linux':
        __notify.warning('open_os_directory is not supported on platform: %s' % sys.platform)
    else:
        os.system('explorer "%s"' % path)
        success = True

    return success

def get_local_data_directory() -> str:
    """
    Returns the application's local data directory
    """

    from panda3d_toolbox import prc
    folder_name = prc.get_prc_string('data-folder', 'Panda3D')

    if sys.platform in ['win32', 'cygwin', 'msys']:
        return os.path.join(os.getenv('LOCALAPPDATA'), folder_name)
    else:
        __notify.warning('get_local_data_directory is not supported on platform: %s. Defaulting to install directory' % sys.platform)
        return '.'

def get_local_data_path(path: str) -> str:
    """
    Returns the path relative to the application's local data directory
    """

    return os.path.join(get_local_data_directory(), path)
 
def get_screenshot_directory(absolute: bool = False) -> str:
    """
    Returns the application's screenshot directory
    """
    
    return get_local_data_path('screenshots')

def open_screenshot_directory() -> bool:
    """
    Opens the application's screenshot directory in the operation system's
    file browser window. Returning true on success, otherwise false.
    """

    return open_os_directory(get_screenshot_directory(True))

def build_screenshot_filename(basename: str = 'screenshot', directory: str = None, format: str = 'png') -> str:
    """
    Builds the file path for a newly created screenshot
    """

    if directory is None:
        directory = get_screenshot_directory()

    now = datetime.datetime.now()
    filename = now.strftime(basename + '_%y%m%d_%H%M%S')
    path = os.path.join(directory, filename +' .' + format)
    appendix = 0

    while os.path.exists(path):
        appendix += 1
        path = os.path.join(directory, filename + '_' + str(appendix) + '.' + format)

    return path

def save_screenshot(directory: str = None, format: str = 'png', win: object = None):
    """
    Saves a screenshot of the current render output to file
    """

    if not win:
        win = runtime.base.win

    path = build_screenshot_filename(directory=directory, format=format)
    win.save_screenshot(Filename(path))
    __notify.info('Saved Screenshot: %s' % path)