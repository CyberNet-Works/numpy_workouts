import numpy as np

array1 = np.array(list(map(int, input().split())))

even_arr1 = array1[array1 % 2 == 0]
even_arr2= np.where(array1 % 2 == 0, array1, 0)

print(even_arr1)
print(even_arr2)

'''Filter NumPy Array
Idea Emoji
New to Practice?
Take a tour
Write a program to find even numbers from a NumPy array.

Take array elements as user input.
Write a condition to filter even numbers from an array.
Use where() to find even numbers.
Print the results.
Example
Test Input

[1, 2, 3, 4, 5, 6, 7] 
Expected Output

[2 4 6]
[0 2 0 4 0 6 0]
'''
