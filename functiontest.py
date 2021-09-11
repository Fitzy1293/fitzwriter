'''
Testing things program

Testing an individual function:
    -   imports test_this_function() from timetesting.py
    -   starts a timer after it is imported
    -   runs test function
    -   prints time delta

This also works for testing the time it takes to import modules.
Once a module is imported, it won't be imported again during the same execution.

So testing the time it takes to import libraries in a loop like below is pointless, because it's only imported once, then skipped.
    for i in range(10):
        import randomlibrary

Unfortunately this means that to test how long it takes to import stuff, you have to execute another python process.
'''

from time import time
from timetesting import test_this_function

START_TIME = time()

def run_test():
    test_this_function() # Running function we want to test.

    time_after_test = time()
    time_delta = time_after_test - START_TIME
    time_delta_scientific_notation = f'{time_delta:.2E}'
    time_delta_decimal = f'{time_delta:.3g}'

    print (f'{time_delta_scientific_notation} -> runtime={time_delta:.12F}')


if __name__ == '__main__':
    run_test()
