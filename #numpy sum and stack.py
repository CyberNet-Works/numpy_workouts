#numpy sum and stack
import numpy as np

# take two arrays as user input
array1 = np.array(list(map(int, input().split())))
array2 = np.array(list(map(int, input().split())))

# calculate the sum of each array 
arr_sum = np.sum(array1, axis = 0)
arr_sum2 = np.sum(array2, axis = 0)


# stack the resulting arrays together 
arr_stack = np.stack((arr_sum, arr_sum2))

# print the stacked array
print(arr_stack)