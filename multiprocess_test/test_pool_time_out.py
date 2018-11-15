import subprocess
from multiprocessing import Pool
import time


def sleeping_10(x):
    print('%i got!' % x)
    for i in range(0, 10):
        time.sleep(1)
        print('%i process, ticks %i' % (x, i))
    print('%i ended!' % x)
    return 1


def sleeping_x(x):
    print('%i got!' % x)
    for i in range(0, x):
        time.sleep(1)
        print('%i process, ticks %i' % (x, i))
    print('%i ended!' % x)
    return 1


def dead_loop(x):
    print('%i got!' % x)
    while(1):
        pass


if __name__ == '__main__':
    with Pool(processes=2) as pool:
        tasks = [pool.apply_async(sleeping_10, (x,)) for x in range(0, 2)]
        result = []
        for one in tasks:
            try:
                result.append(one.get(timeout=2))
            except:
                print('catch error!')
                result.append(None)
        print(result)
    """
    output is:
        0 got!
        1 got!
        0 process, ticks 0
        1 process, ticks 0
        catch error!
        0 process, ticks 1
        1 process, ticks 1
        0 process, ticks 2
        1 process, ticks 2
        catch error!
        [None, None]
    it is confirmed that each process still have 2 seconds in machines time.
    but actually, it takes almost 4 seconds in real world time.
    
    note, machine time is affected by other processes. as i closed one process, makes the CPU becomes
    IDLE, it tooks shorter to trigger the ticks.
    """

    with Pool(processes=2) as pool:
        tasks = [pool.apply_async(dead_loop, (x,)) for x in range(0, 2)]
        result = []
        for one in tasks:
            try:
                result.append(one.get(timeout=2))
            except:
                result.append(None)
        print(result)
    """
    output is:
        0 got!
        1 got!
        [None, None]
    """

    with Pool(processes=2) as pool:
        tasks = [pool.apply_async(sleeping_x, (x,)) for x in range(1, 5)]
        result = []
        for one in tasks:
            try:
                result.append(one.get(timeout=2))
            except:
                print('catch error!')
                result.append(None)
        print(result)
    """
    1 got!
    2 got!
    1 process, ticks 0
    1 ended!
    3 got!
    2 process, ticks 0
    3 process, ticks 0
    2 process, ticks 1
    2 ended!
    4 got!
    3 process, ticks 1
    4 process, ticks 0
    3 process, ticks 2
    3 ended!
    4 process, ticks 1
    4 process, ticks 2
    catch error!
    [1, 1, 1, None]
    4 process, ticks 3
    4 ended!
    """
