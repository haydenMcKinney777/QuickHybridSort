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


# ------------------------
# testing
# ------------------------

def generate_random_array(n):
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return arr

def test_runtime(n, k, trials=10):
    total_time = 0
    for _ in range(trials):
        arr = generate_random_array(n)
        expected = sorted(arr[:])
        start = time.perf_counter()
        QuickHybridSort(arr, k)
        end = time.perf_counter()
        total_time += (end - start)

        if arr != expected:
            print(f"❌ incorrect result for n={n}, k={k}")
            print(f"expected: {expected}")
            print(f"got     : {arr}")
            return -1
    return total_time / trials

# Array sizes and thresholds to test
n_values = [500, 1000, 5000, 10000, 100000, 1000000]
k_values = list(range(1, 51, 5))
print("Average runtime (seconds) for each (n, K):\n")
runtime_data = {n: [] for n in n_values}
optimal_k_per_n = {}

for n in n_values:
    best_k = None
    best_time = float('inf')
    print(f"\nn = {n}")
    for k in k_values:
        avg_time = test_runtime(n, k)
        if avg_time != -1:
            runtime_data[n].append(avg_time)
            print(f"  K = {k:<3} → {avg_time:.6f} sec")
            if avg_time < best_time:
                best_time = avg_time
                best_k = k
        else:
            print(f"  K = {k:<3} → ❌ Skipped due to incorrect result")
    if best_k is not None:
        optimal_k_per_n[n] = best_k

# Plot only the n values that have full runtime data
plt.figure(figsize=(10, 6))
for n in n_values:
    if len(runtime_data[n]) == len(k_values):
        plt.plot(k_values, runtime_data[n], marker='o', label=f"n = {n}")
    else:
        print(f"⚠️ Skipping n = {n} in plot (incomplete data)")

plt.title("QuickHybridSort Runtime vs Threshold K")
plt.xlabel("Threshold K")
plt.ylabel("Average Runtime (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot optimal K vs array size
plt.figure(figsize=(8, 5))
plt.plot(list(optimal_k_per_n.keys()), list(optimal_k_per_n.values()), marker='o')
plt.title("Optimal K vs Array Size n")
plt.xlabel("Array Size (n)")
plt.ylabel("Optimal K")
plt.grid(True)
plt.tight_layout()
plt.show()