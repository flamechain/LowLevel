import termcolor
import time
import inspect

# Global Variables

total = 0
done = 0
success = 0
failed = 0
equates = {}
start = time.time()

# Logging Level
level = 0

# Testing Framework

def runTest(priorety=0):
    '''Handles equate_* statements for each test'''
    def inner(func):
        def wrapper(*args, **kwargs):
            global success, failed, total, done, equates, level
            if priorety >= level:

                total += 1
                done += 1
                plus = termcolor.colored('+', 'green')
                minus = termcolor.colored('-', 'red')

                plus = '+'
                minus = '-'

                try:
                    func()

                    for i in equates:
                        if equates[i] == False:
                            failed += 1
                            print('[%s] Function %s failed.' % (minus, func.__name__))
                            for j in equates:
                                if equates[j] == False:
                                    # print('    %s %s' % (termcolor.colored('Failed expect_eq:', 'red'), j))
                                    print('    %s %s' % ('Failed expect_eq:', j))
                            equates = {}

                            return

                    success += 1
                    print('[%s] Function %s succeded.' % (plus, func.__name__))

                except Exception as e:
                    done -= 1
                    # print('[%s] Function %s %s\n    %s %s' % (minus, func.__name__, termcolor.colored('failed to execute.', 'red'),termcolor.colored('Raised Exception:', 'red'), e))
                    print('[%s] Function %s %s\n    %s %s' % (minus, func.__name__, 'failed to execute.', 'Raised Exception:', e))

                equates = {}
        return wrapper()
    return inner

def showTestResults():
    global success, failed, total, done

    end = time.time()
    runtime = round(end-start, 2)
    testssuccess = '%d tests succeded' % success
    outof = 'out of'
    failnum = failed
    failed = '%d tests failed' % failed
    if success == total:
        # testssuccess = termcolor.colored(testssuccess, 'green')
        testssuccess = testssuccess
    if done < total:
        # done = termcolor.colored(str(done), 'red')
        # total = termcolor.colored(str(total), 'red')
        # outof = termcolor.colored(outof, 'red')
        done = str(done)
        totl = str(total)
    if failnum > 0:
        # failed = termcolor.colored(failed, 'red')
        failed = failed

    print('\nTest Results:\n\nRan %s %s %s tests.    \n--------------------------------------\n    %s\n    %s\n\n    Total Runtime: %ss\n--------------------------------------' % (done, outof, total, testssuccess, failed, str(runtime)))

def expect_eq(a, b):
    '''Stores result in list'''
    global equates

    if a == b:
        equates[str(a) + str(b) + str(time.time())] = True

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
        equates[f'{a} != {b} ({names[0]}, {names[1]})'] = False
