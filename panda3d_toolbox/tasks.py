"""
"""

from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d_toolbox import runtime, reflections

# -----------------------------------------------------------------

__notify = directNotify.newCategory('tasks')
BACKGROUND_THREAD_NAME = 'background-tasks'

# -----------------------------------------------------------------

def start_background_thread() -> None:
    """
    Starts a background thread chain in the Panda3D
    task manager
    """

    runtime.task_mgr.setupTaskChain(
        BACKGROUND_THREAD_NAME, 
        numThreads = 1,
        threadPriority = 0)

def run_func_async(func: object, name: str = None) -> None:
    """
    Runs a the requested function under a coroutine
    """

    assert func != None
    assert callable(func)

    if name is None:
        name = '%s-async-task' % func.__name__

    async def async_wrapper(task) -> int:
        """
        Async wrapper for the callback
        """

        await func()
        return task.done

    create_task(async_wrapper, name)

def perform_callback_on_condition(condition: bool, callback: object, *args, **kwargs) -> None:
    """
    Performs the required callback if the condition is True
    """

    assert callback != None
    assert callable(callback)

    # Check if the condition is true
    if not condition:
        return

    if reflections.is_awaitable_function(callback):
        run_func_async(callback, '%s-callback-async' % callback.__name__)
    else:
        callback(*args, **kwargs)

def __create_task_name(obj, task):
    """
    Creates a name for a task based on the obj its being used on
    """

    cls_name = obj.__class__.__name__
    if hasattr(obj, 'get_name'):
        name = obj.get_name()
        return '%s.%s(%s)' % (cls_name, task, name)

    return '%s.%s(<%d>)' % (cls_name, task, id(obj))

def create_task(task_func, task_name = '', priority = 0, task_chain_name: str = None):
    """
    Creates a new task with the task manager
    """

    task_name = __create_task_name(task_func.__self__, task_name or task_func.__name__)
    return runtime.task_mgr.add(task_func, task_name, priority, taskChain=task_chain_name)

def create_delayed_task(task_func, delay, task_name = '', priority = 0):
    """
    Creates a new delayed task with the task manager
    """

    task_name = __create_task_name(task_func.__self__, task_name or task_func.__name__)
    return runtime.task_mgr.do_method_later(task_func, task_name, priority)

def remove_task(task):
    """
    Removes a task from the task manager
    """

    runtime.task_mgr.remove(task)

def create_thread(thread_name, thread_priority=0, prc_check: str = None):
    """
    Creates a new task manager thread
    """

    threads=0
    if prc_check != None:
        from panda3d_toolbox import prc
        if prc.get_prc_bool(prc_check, False):
            threads=1

    runtime.task_mgr.setupTaskChain(
        thread_name, 
        numThreads=threads, 
        threadPriority=thread_priority)
    
class _DoMethodAfterNFrames(object):
    """
    """

    def __init__(self, frames_to_wait: int, method: object, args: list):
        self.__frames_to_wait = frames_to_wait
        self.__method = method
        self.__args = args

    def task_function(self, task: object) -> int:
        """
        """

        self.__frames_to_wait -= 1
        
        if self.__frames_to_wait <= 0:
            self.__method(*self.__args)

            return task.done

        return task.cont

def do_method_after_n_frames(frames_to_wait: int, method: object, args: list = [], priority: int = 0) -> None:
    """
    """

    if frames_to_wait > 0:
        create_task(_DoMethodAfterNFrames(frames_to_wait, method, args).task_func, priority=priority)
    else:
        __notify.error('Invalid request. do_method_after_n_frames received a frames wait of 0')