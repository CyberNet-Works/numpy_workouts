#np stack
#must pass one iterable containing arrays — not multiple separate arguments.
#must have the same shape otherwise error

import numpy as np
array1 = np.array((list(map(int, input("Enter Four numbers: ").split()))))
array2 = np.array([5,6,7,8])

result = np.stack((array1, array2))

print(result)
