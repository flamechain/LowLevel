'''
Custom testing framework
'''

import time
import inspect

import termcolor


class Results:
    def __init__(self):
        self.done = 0
        self.total = 0
        self.success = 0
        self.failed = 0
        self.equates = {}
        self.groups = {}
        self.start = time.time()
        self.stop = False
        self.failedFunc = []
        self.running = False
        self.groupsRan = []
        self.groupsExcluded = []


class TestSettings:
    def __init__(self, stopOnFirstFail=False):
        self.stopOnFirstFail = stopOnFirstFail


results = Results()
settings = TestSettings()

def testSettings(**kwargs):
    if 'stopOnFirstFail' in kwargs:
        settings.stopOnFirstFail = kwargs['stopOnFirstFail']

def group(group='default'):
    '''Adds test to group'''
    def inner(func):
        def wrapper(*args, **kwargs):

            global results

            if group in results.groups:
                results.groups[group].append(func)

            else:
               results.groups[group] = [func]

        wrapper()
    return inner

def test():
    '''Handles equate_* statements for each test'''
    def inner(func):
        def wrapper(*args, **kwargs):
            global results, settings

            results.total += 1

            if (results.stop == False) and (results.running == True):

                results.done += 1
                plus = termcolor.colored('+', 'green')
                minus = termcolor.colored('-', 'red')

                try:
                    func()

                    for i in results.equates:
                        if results.equates[i] == False:
                            results.failed += 1
                            results.failedFunc.append(func)
                            print('[%s] Function %s failed.' % (minus, func.__name__))

                            for j in results.equates:
                                if results.equates[j] == False:
                                    print('    %s' % j)

                            results.equates = {}

                            if settings.stopOnFirstFail:
                                results.stop = True

                            return

                    results.success += 1
                    print('[%s] Function %s succeded.' % (plus, func.__name__))
    
                except Exception as e:
                    results.done -= 1
                    print('[%s] Function %s %s\n    %s %s' % (minus, func.__name__, termcolor.colored('failed to execute.', 'red'),termcolor.colored('Raised Exception:', 'red'), e))

                equates = {}

        return wrapper

    return inner

def runTests(toRun=['all'], exclude=[]) -> None:
    '''Runs tests'''
    global results

    print()
    results.running = True

    for i in results.groups:
        if ('all' in toRun) or (i in toRun):
            if i not in exclude:
                for j in results.groups[i]:
                    j()

    results.groupsRan = toRun
    results.groupsExcluded = exclude

def showTestResults() -> None:
    '''Shows results of tests'''
    global results

    end = time.time()
    runtime = round(end-results.start, 2)
    testssuccess = '%d tests succeded' % results.success
    outof = 'out of'
    failnum = results.failed
    failed = '%d tests failed' % results.failed
    done = results.done
    total = results.total

    if settings.stopOnFirstFail:
        msg = 'Stopped on first failure.'
    else:
        msg = ''

    if results.success == total:
        testssuccess = termcolor.colored(testssuccess, 'green')

    if done < total:
        done = termcolor.colored(str(done), 'red')
        total = termcolor.colored(str(total), 'red')
        outof = termcolor.colored(outof, 'red')

    if failnum > 0:
        failed = termcolor.colored(failed + ':', 'red')

    ran = str(results.groupsRan)
    if ran == "['all']":
        ran = 'all'
    if results.groupsExcluded != []:
        if len(results.groupsExcluded) == 1:
            ran += ', excluding %s' % results.groupsExcluded[0]
        else:
            ran += ', excluding %s' % results.groupsExcluded
    print('\nTest Results:\n\nRan %s %s %s tests. %s\nGroups ran: %s\n-----------------------------------------------\n    %s\n    %s' % (done, outof, total, msg, ran, testssuccess, failed))

    for i in results.failedFunc:
        print('        ' + termcolor.colored(i.__name__, 'red'))

    print('\n    Total Runtime: %ss\n-----------------------------------------------' % str(runtime))

def EXPECT_EQ(a, b) -> None:
    '''Fails if values are not equal'''
    global results

    if (a == b) or (a.__repr__() == b) or (a == b.__repr__()) or (a.__repr__() == b.__repr__()):
        results.equates[str(a) + str(b) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        if names[1].startswith(' '):
            names[1] = names[1][1:]

        message = termcolor.colored('Failed EXPECT_EQ:', 'red')
        results.equates[f'{message} {a} != {b} ({names[0]}, {names[1]})'] = False

def EXPECT_NOT_EQ(a, b) -> None:
    '''Fails if values are equal'''
    global results

    if (a != b) or (a.__repr__() != b) or (a != b.__repr__()) or (a.__repr__() != b.__repr__()):
        results.equates[str(a) + str(b) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        if names[1].startswith(' '):
            names[1] = names[1][1:]

        message = termcolor.colored('Failed EXPECT_NOT_EQ:', 'red')
        results.equates[f'{message} {a} == {b} ({names[0]}, {names[1]})'] = False

def EXPECT_FALSE(a) -> None:
    '''Fails if value is not false'''
    global results

    if (a == False) or (a.__repr__() == False):
        results.equates[str(a) + str(b) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        message = termcolor.colored('Failed EXPECT_FALSE:', 'red')
        results.equates[f'{message} {a} != False ({names[0]})'] = False

def EXPECT_TRUE(a) -> None:
    '''Fails if value is not true'''
    global results

    if (a == True) or (a.__repr__() == True):
        results.equates[str(a) + str(b) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        message = termcolor.colored('Failed EXPECT_TRUE:', 'red')
        results.equates[f'{message} {a} != True ({names[0]})'] = False

def EXPECT_ERROR(func: object, expectedErrors=[Exception], params=[]) -> None:
    '''Fails if func does not raise exception'''
    global results

    ex = None

    if isinstance(expectedErrors, list):
        pass
    else:
        expectedErrors = [expectedErrors]

    try:
        func(params)
        a = 'false'

    except Exception as e:
        ex = e
        excepts = [str(i.__name__) for i in expectedErrors]
        if (str(type(e).__name__) in excepts) or (Exception in expectedErrors):
            a = True

        else:
            a = False

    if a == True:
        results.equates[str(a) + str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in args:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        if names[1].startswith(' '):
            names[1] = names[1][1:]

        message = termcolor.colored('Failed EXPECT_ERROR:', 'red')
        exceptsstrings = [str(i.__name__) for i in expectedErrors]
        exceptsstrings = str(exceptsstrings)
        if a == 'false':
            results.equates[f'{message} Function {func.__name__} did not raise exception. ({names[0]}, {exceptsstrings})'] = False
        elif a == False:
            text = termcolor.colored('Exception Raised:', 'red')
            results.equates[f'{message} Expection raised by {func.__name__} was not in exception list. ({names[0]}, ' + exceptsstrings.replace("'", "") + f')\n    {text} {str(type(ex).__name__)}'] = False

def EXPECT_ALL_EQ(*args) -> None:
    '''Fails if all values are not equal'''
    global results

    val = args[0]
    a = True

    for i in args:
        if i != val:
            if i.__repr__() != val:
                if i != val.__repr__():
                    if i.__repr__() != val.__repr__():
                        a = False

    if a == True:
        results.equates[str(time.time())] = True

    else:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        nargs = string[string.find('(') + 1:-1].split(',')
        names = []

        for i in nargs:
            if i.find('=') != -1:
                names.append(i.split('=')[1].strip())

            else:
                names.append(i)

        for i in range(len(names)):
            if names[i].startswith(' '):
                names[i] = names[i][1:]

        message = termcolor.colored('Failed EXPECT_ALL_EQ:', 'red')
        joined = " != ".join([str(i) for i in args])
        results.equates[f'{message} {joined} ({", ".join(names)})'] = False
