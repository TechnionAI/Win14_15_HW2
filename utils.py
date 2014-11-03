"""Generic utility functions
"""
from multiprocessing import Process, Queue
import time


class PlayerExceededTimeError(RuntimeError):
    pass


def function_wrapper(func, args, kwargs, result_queue):
    """Runs the given function and measures its runtime.

    :param func: The function to run.
    :param args: The function arguments as tuple.
    :param kwargs: The function kwargs as dict.
    :param result_queue: The inter-process queue to communicate with the parent.
    :return: A tuple: The function return value, and its runtime.
    """
    start = time.clock()
    result = func(*args, **kwargs)
    runtime = time.clock() - start
    result_queue.put((result, runtime))


def run_with_limited_time(func, args, kwargs, time_limit):
    """Runs a function with time limit

    :param func: The function to run.
    :param args: The functions args, given as tuple.
    :param kwargs: The functions keywords, given as dict.
    :param time_limit: The time limit in seconds (can be float).
    :return: A tuple: The function's return value unchanged, and the running time for the function.
    :raises PlayerExceededTimeError: If player exceeded its given time.
    """
    q = Queue()
    p = Process(target=function_wrapper, args=(func, args, kwargs, q))
    p.start()

    # This is just for limiting the runtime of the other process, so we stop eventually.
    # It doesn't really measure the runtime.
    p.join(time_limit * 1.1)

    if p.is_alive():
        p.terminate()
        raise PlayerExceededTimeError

    return q.get()

if __name__ == '__main__':
    def f(t, s):
        start_time = time.clock()
        while time.clock() - start_time < t:
            for i in range(10**3):
                pass
        return s * 2

    print run_with_limited_time(f, (1.5, 'a'), {}, 2.5)
    try:
        print run_with_limited_time(f, (3.5, 'b'), {}, 2.5)
    except PlayerExceededTimeError:
        print 'OK'

    print run_with_limited_time(f, (1.5, 4), {}, float('inf'))