#numpy all boolean result
import numpy as np

array1 = list(map(int, input("Enter Some numbers: ").split()))
arr = np.array(array1)
result = np.all(arr > 3)
print(result)