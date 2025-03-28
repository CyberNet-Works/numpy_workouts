#sum / mean / median / std
import numpy as np

array1 = np.array([[1,2,3],[4,5,6],[7,8,9]])

sum_rows = np.sum(array1, axis=0)
mean_rows = np.mean(array1, axis=0)
median_rows = np.median(array1, axis=0)
std_rows = np.std(array1, axis =0)

print(f'Sum along rows:{sum_rows}')
print(f'Mean along rows:{mean_rows}')
print(f'Median along rows:{median_rows}')

print(f'STD along rows:{std_rows.round(2)}')
