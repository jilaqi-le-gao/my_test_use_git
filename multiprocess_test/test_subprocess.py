import subprocess
from multiprocessing import Pool


def using_subprocess_wait(x):
    print('%i got!' % x)
    one = subprocess.Popen('sleep %i' % x, shell=True)
    one.wait()
    print('%i ended!' % x)
    return x


def using_subprocess_timeout(x):
    print('%i got!' % x)
    one = subprocess.Popen('sleep %i' % x, shell=True)
    try:
        one.wait(timeout=5)
    except:
        return None
    print('%i ended!' % x)
    return x


if __name__ == '__main__':
    with Pool(processes=2) as pool:
        tasks = [pool.apply_async(using_subprocess_wait, (x,)) for x in range(3, 7)]
        result = []
        for one in tasks:
            try:
                result.append(one.get(timeout=3))
            except:
                print('catch error!')
                result.append(None)
        print(result)
    """
    3 got!
    4 got!
    catch error!
    3 ended!
    5 got!
    4 ended!
    6 got!
    catch error!
    5 ended!
    catch error!
    [None, 4, None, None]
    6 ended!
    """

    with Pool(processes=2) as pool:
        tasks = [pool.apply_async(using_subprocess_timeout, (x,)) for x in range(3, 7)]
        result = []
        for one in tasks:
            result.append(one.get())
        print(result)

    """
    3 got!
    4 got!
    3 ended!
    5 got!
    4 ended!
    6 got!
    [3, 4, None, None]
    """

    """
    从运行的实际结果来看，由于python的GIL锁的关系，所以pool的监测timeout的时间其实不如subprocess的Popen来的靠谱。
    所以，单纯的Python脚本函数用pool调用的timeout检测还可以试试。
    但是如果本身就是用subprocess调用脚本，或者脚本本身的运行时间需要严格的控制，最好还是用subprocess调用命令后，
    在用wait的timeout检测，时间非常的稳，就是系统的运行时间。
    """