#numpy_project
import numpy as np

# function to initialize and store data
def initialize_data():

    subject = np.array(['English', 'Maths', 'Science', 'Social', 'History'])
    students = np.array(['Alice', 'Bob', 'Charlie', 'Dan'])
    marks = np.array([[81, 78, 80, 60, 63],
                      [50, 60, 65, 48, 55],
                      [30, 83, 97, 79, 75],
                      [99, 55, 60, 48, 30]])
    return subject, students, marks

# main function
def main():
    # call the function initialize_data
    subject, students, marks = initialize_data()
    print(subject)
    print(students)
    print(marks)

# call the main function
main()