"""
Hayden McKinney
CS 3364 - Dr. Chinta
4/30/2025


Part 1 of final project for CS 3364 Design and Analysis of Algorithms
Quick Hybrid Sort algorithm: take in an array of ints and a threshold value. 
If a subarray has length <= k, call insertion sort. Else call quicksort

1. Return a sorted version of the array in ascending order. Can either implement this in-place or return a new array.

2. Measure average runtimes for various n and k based on random arrays, and plot the performance for at least 5 different n values while varying k.

3. Compare QuickHybridSort to Quicksort and Insertion Sort, and identify the optimal k value(s)

4. Repeat steps 2 and 3 using pre-sorted input arrays, and explain how and why the results differ. 
"""
import random
import time
import matplotlib.pyplot as plt
import numpy as np

def plotData(k_to_n_dictionary):
    keys = list(k_to_n_dictionary.keys())
    values = list(k_to_n_dictionary.values())

    plt.plot(keys, values, marker='o')
    plt.xlabel('array size')
    plt.ylabel('best k value')
    plt.title('Best k values for a given array size (QuickHybridSort)')
    plt.grid(True)
    plt.show()

def plotComparison(n_array_sizes, hybrid_times, quick_times, insert_times):
    plt.plot(n_array_sizes, hybrid_times, label='QuickHybridSort', marker='o')
    plt.plot(n_array_sizes, quick_times, label='QuickSort', marker='s')
    plt.plot(n_array_sizes[:3], insert_times, label='InsertionSort', marker='^')  # Only show InsertionSort for small n
    plt.xlabel('Array Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison of Sorting Algorithms')
    plt.legend()
    plt.grid(True)
    plt.show()

def Swap(A, i, j):
    A[i], A[j] = A[j], A[i]

def Partition(A, left, right):
    mid = (left + right) // 2
    pivot_candidates = [(A[left], left), (A[mid], mid), (A[right], right)]
    pivot_value, pivot_index = sorted(pivot_candidates)[1]
    Swap(A, left, pivot_index)  #pivot to the front
    pivot = A[left]
    i = left
    j = right+1

    while True:
        while True:
            i += 1
            if i >= right or A[i] >= pivot:
                break

        while True:
            j -= 1
            if j <= left or A[j] <= pivot:
                break

        if i < j:
            Swap(A, i, j)
        else:
            Swap(A, j, left)
            return j

def InsertionSort(A, left, right):
    for i in range(left+1, right+1):
        v = A[i]
        j = i-1
        while j >= left and A[j] > v:
            A[j+1] = A[j]
            j -= 1
        A[j+1] = v

def QuickSort(A, left, right, threshold):
    if right - left + 1 <= threshold:
        InsertionSort(A, left, right)
    elif left < right:
        S = Partition(A, left, right)
        QuickSort(A, left, S, threshold)
        QuickSort(A, S+1, right, threshold)

def QuickHybridSort(num_array, threshold):
    if len(num_array) <= 1:
        return
    QuickSort(num_array, 0, len(num_array)-1, threshold)

#------------------------------------
# measure quickHybridSort on sorted inputs for various k
#------------------------------------
print("\n\n==============================")
print("TASK 2")
print("==============================")

presorted_n_values = [5000, 10000, 25000, 50000, 100000]
k_values = [1, 5, 10, 15, 20, 30, 40, 50]
sorted_input_k_vs_time = {}

for n in presorted_n_values:
    times_for_k = []
    presorted_array = list(range(1, n+1))

    for k in k_values:
        arr = presorted_array.copy()
        start = time.perf_counter()
        QuickHybridSort(arr, k)
        end = time.perf_counter()
        times_for_k.append(end - start)

    sorted_input_k_vs_time[n] = times_for_k

for n in presorted_n_values:
    plt.plot(k_values, sorted_input_k_vs_time[n], label=f'n = {n}', marker='o')

plt.xlabel("Threshold k value")
plt.ylabel("Execution Time (seconds)")
plt.title("QuickHybridSort on Sorted Inputs: Time vs k")
plt.legend()
plt.grid(True)
plt.show()

#------------------------------------
#------------------------------------
print("\n\n==============================")
print("TASK 3: Comparing All Sorts on Sorted Inputs")
print("==============================")

hybrid_sorted_times = []
quick_sorted_times = []
insert_sorted_times = []
best_k_on_sorted = {}

for n in presorted_n_values:
    sorted_array = list(range(1, n+1))
    best_time = float('inf')
    best_k = None

    for k in k_values:
        arr = sorted_array.copy()
        start = time.perf_counter()
        QuickHybridSort(arr, k)
        duration = time.perf_counter() - start
        if duration < best_time:
            best_time = duration
            best_k = k

    best_k_on_sorted[n] = best_k

    #hybrid using best k
    arr = sorted_array.copy()
    start = time.perf_counter()
    QuickHybridSort(arr, best_k)
    hybrid_sorted_times.append(time.perf_counter() - start)

    #pure QuickSort (threshold 0)
    arr = sorted_array.copy()
    start = time.perf_counter()
    QuickSort(arr, 0, len(arr)-1, 0)
    quick_sorted_times.append(time.perf_counter() - start)

    #snsertionSort
    arr = sorted_array.copy()
    start = time.perf_counter()
    InsertionSort(arr, 0, len(arr)-1)
    insert_sorted_times.append(time.perf_counter() - start)

#plot the comparison for sorted inputs
plt.plot(presorted_n_values, hybrid_sorted_times, label='QuickHybridSort', marker='o')
plt.plot(presorted_n_values, quick_sorted_times, label='QuickSort', marker='s')
plt.plot(presorted_n_values, insert_sorted_times, label='InsertionSort', marker='^')
plt.xlabel("Array Size (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Sorted Input: Comparison of Sorting Algorithms")
plt.legend()
plt.grid(True)
plt.show()

print("\nBest k values on sorted inputs:")
for n, k in best_k_on_sorted.items():
    print(f"n = {n}: best k = {k}")


#------------------------------------
#test
#------------------------------------

n_array_sizes = [5000, 10000, 25000, 50000, 75000, 100000, 250000]
k_values = [1, 5, 10, 15, 20, 30, 40, 50]
best_k_per_n_size_array = {}

hybrid_times = []
quick_times = []
insert_times = []

for n in n_array_sizes:
    print(f"\nTesting array size: {n}")
    best_k = None
    best_time = float('inf')
    base_arr = list(range(1, n+1))
    random.shuffle(base_arr)

    #find best k for hybrid sort
    for k in k_values:
        arr = base_arr.copy()
        expected = sorted(arr)

        start = time.perf_counter()
        QuickHybridSort(arr, k)
        end = time.perf_counter()
        total_time = end - start

        if arr == expected and total_time < best_time:
            best_time = total_time
            best_k = k
            best_k_per_n_size_array[n] = k

    #time the best hybrid sort
    hybrid_arr = base_arr.copy()
    start = time.perf_counter()
    QuickHybridSort(hybrid_arr, best_k)
    hybrid_times.append(time.perf_counter() - start)

    #time the pure quick sort (with threshold 0)
    quick_arr = base_arr.copy()
    start = time.perf_counter()
    QuickSort(quick_arr, 0, len(quick_arr)-1, 0)
    quick_times.append(time.perf_counter() - start)

    #time insertion sort for small arrays only
    if n <= 25000:
        insert_arr = base_arr.copy()
        start = time.perf_counter()
        InsertionSort(insert_arr, 0, len(insert_arr)-1)
        insert_times.append(time.perf_counter() - start)

print("\nBest k values by array size:")
for n, k in best_k_per_n_size_array.items():
    print(f"n = {n}: best k = {k}")

plotData(best_k_per_n_size_array)

plotComparison(n_array_sizes, hybrid_times, quick_times, insert_times)