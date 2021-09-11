'''
Test import times with the corresponding timetest.sh script.
Python will only import something once per execution.
So you need a separate script that starts a new python process.

Testing an individual function:
    -   imports test_this_function() from timetesting.py
    -   starts a timer after it is imported

'''

from time import time
from timetesting import test_this_function

START_TIME = time()

def run_test(initial_time=START_TIME):
    test_this_function() # Running function we want to test.

    time_after_test = time()
    print (f'runtime={time_after_test - START_TIME}')


if __name__ == '__main__':
    run_test()
