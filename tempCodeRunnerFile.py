import random
import time
import matplotlib.pyplot as plt
import numpy as np

def plotData(k_to_n_dictionary):
    keys = list(k_to_n_dictionary.keys())
    values = list(k_to_n_dictionary.values())
    
    plt.plot(keys,values)
    plt.xlabel('array size')
    plt.ylabel('best k value')
    plt.title('best k values for an "n" size array')
    plt.show()

def Swap(A, i, j):
    A[i], A[j] = A[j], A[i]

def Partition(A, left, right):
    pivot = A[left]
    i = left
    j = right+1                                                     #we start the counters right before the first element and right after the last so that the edges of array get included

    while True:
        while True:
            i = i+1                                                 #when the 'do' block is executed for the first time, i will now represent the index of the leftmost element in the array
            if A[i] >= pivot or i>=right:
                break

        while True:
            j = j-1
            if A[j] <= pivot or j<=left:
                break

        if i < j:                                                   #if i and j did not overlap
            Swap(A, i, j)
        else:
            Swap(A, j, left)                                        #if i and j overlap swap A[j] with the pivot
            return j 

def InsertionSort(A, left, right):
    for i in range(left+1, right+1):
        v = A[i]
        j = i-1
        while j >= left and A[j]>v:
            A[j+1] = A[j]
            j-=1
        A[j+1] = v

def QuickSort(A, left, right, threshold):                
    if right - left + 1 <= threshold:
        InsertionSort(A, left, right)
    elif left < right:
        S = Partition(A, left, right)
        QuickSort(A, left, S, threshold)
        QuickSort(A, S+1, right, threshold)


def QuickHybridSort(num_array, threshold):
    if len(num_array) == 0:
        return None
    elif len(num_array) == 1:
        return num_array
    else:
        left, right = 0, len(num_array)-1
        QuickSort(num_array, left, right, threshold)

#--------------------------------------------------------
#test cases
#--------------------------------------------------------

n_array_sizes = [5000, 10000, 25000, 50000, 75000, 100000, 250000, 500000, 850000]
k_values = [1, 5, 10, 15, 20, 30, 40, 50]
best_k_per_n_size_array = {}

for n in n_array_sizes:
    print("\n")

    best_k = None
    best_time = float('inf')
    base_arr = list(range(1, n+1))
    random.shuffle(base_arr)

    for k in k_values:
        arr = base_arr.copy()

        start = time.perf_counter()
        QuickHybridSort(arr, k)
        end = time.perf_counter()
        total_time = end - start

        if total_time < best_time:
            best_time = total_time
            best_k_per_n_size_array[n] = k

        print(f"Time of execution for array size n = {n}, threshold k = {k}: {total_time:.6f} seconds")

    print(f"\nk value that provides the fastest time for array size {n}: {best_k_per_n_size_array[n]}")

plotData(best_k_per_n_size_array)