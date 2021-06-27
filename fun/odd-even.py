# How much faster is odd/even through bit-shifting faster than a conventional approach?

"""
Results:
	interesting because bitwise is actually slightly slower... but that may just be python
"""

import time


def conventional_num_is_odd(num):
	return num % 2


def bitwise_num_is_odd(num):
	return num & 1


# make it more difficult for any optimizations to occur
some_global_var = 0


def _perform_test(fn, num_iterations):
	start = time.time()
	for i in range(num_iterations):
		global some_global_var
		some_global_var = fn(i)
	return time.time() - start


for num_iterations in [1000, 10000, 100000, 1000000, 10000000]:
	print(f"Testing with {num_iterations} iterations")

	print("----> testing conventional")
	conventional_time = _perform_test(conventional_num_is_odd, num_iterations)
	print(f"----> conventional took {conventional_time} seconds")

	print("----> testing bitwise")
	conventional_time = _perform_test(bitwise_num_is_odd, num_iterations)
	print(f"----> bitwise took {conventional_time} seconds")

