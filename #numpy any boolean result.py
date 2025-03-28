#numpy any boolean result
import numpy as np

array1 = np.array([1, 2, 3, 4, 5])

# check if any element is greater than 3
result = np.any(array1 > 3)
print(result)  # Output: True

# check if any element is negative
result = np.any(array1 < 0)
print(result)  # Output: False