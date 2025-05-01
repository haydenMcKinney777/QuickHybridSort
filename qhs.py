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