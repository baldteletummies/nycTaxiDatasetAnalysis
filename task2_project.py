
import csv 
import time 
import random
from typing import Tuple, List, Dict
import matplotlib.pyplot as plt

def read_file(file_path: str) -> any: 
    data = [] 
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

file_path = "nyc_dataset_small.txt" #Change txt file to get the desired data anaylzed
data = read_file(file_path)

#Stores the needed types of data which is extracted from the dataset
num_passengers = []
fare_amounts = []
total_amounts = []
tips_amounts = []

def gatherData(toBeGathered: str) -> list:
   # Returns a list of the predefined data domains
   #The data is appened into the lists
    try:
        match toBeGathered:
                case "num_passengers": # Extract number of passengers
                    for entry in data:
                        if entry.get('passenger_count'):
                            num_passengers.append(int(float(entry.get('passenger_count', 0))))
                    return num_passengers
                case "fare_amounts": # Extract fare amounts
                    for entry in data:
                        if entry.get('fare_amount'):
                            fare_amounts.append(float(entry.get('fare_amount', 0.0)))
                    return fare_amounts
                case "total_amounts": # Extract total amounts
                    for entry in data:
                        if entry.get('total_amount'):
                            total_amounts.append(float(entry.get('total_amount', 0.0)))
                    return total_amounts  
                case "tips_amounts": # Extract tip amounts
                    for entry in data:
                        if entry.get('tip_amount'):
                            tips_amounts.append(float(entry.get('tip_amount', 0.0)))
                    return tips_amounts 
                case _: # Default case
                    return []
    except Exception:
        print("ERROR: Could Not Return Data")
        return []


def bubbleSort(toBeSorted: list) -> list:

    '''The bubble_sort function is a straightforward implementation of the bubble sort 
    algorithm which is O(n^2) in complexity. This sorting method is more suitable for 
    small datasets'''

    start_time = time.time() # Start timer
    n = len(toBeSorted) 
    swapped = True # Flag to indicate if any elements were swapped during a pass
    while swapped:
        swapped = False # Resets the flag for each pass
        for i in range(1, n):
            if toBeSorted[i - 1] > toBeSorted[i]: # Compares the current element with its previous element
                toBeSorted[i - 1], toBeSorted[i] = toBeSorted[i], toBeSorted[i - 1] # Swaps the elements if they are in the wrong order
                swapped = True
        n -= 1  # Each pass finds the largest item and puts it at the end, so we can ignore the end in subsequent passes
    end_time = time.time() #Ends timer
    return toBeSorted, end_time - start_time

def quickSort(toBeSorted: list) -> list:

    '''The quick_sort function is implemented as a typical recursive sort with a random 
    pivot selection to help avoid worst-case performance on sorted datasets. It generally 
    performs with O(n log n) complexity, making it more suitable for larger datasets.'''

    start_time = time.time() # Start timer

    #Base case: If the list has one or fewer elements, it is already sorted
    if len(toBeSorted) <= 1:
        end_time = time.time() # End timer
        return toBeSorted, end_time - start_time

    else:
        pivot_index = random.randint(0, len(toBeSorted) - 1)
        pivot = toBeSorted[pivot_index]
        left = [x for x in toBeSorted if x < pivot]  # Values smaller than pivot
        right = [x for x in toBeSorted if x > pivot]  # Values larger than pivot
        equal = [x for x in toBeSorted if x == pivot]  # Equal to pivot

        # Recursively sort the left and right partitions
        left_sorted, left_time = quickSort(left)
        right_sorted, right_time = quickSort(right)

        end_time = time.time() #timer ends
        execution_time = end_time - start_time + left_time + right_time # Calculate the total execution time including sorting and merging

        return left_sorted + equal + right_sorted, execution_time # Merge the sorted partitions and the equal elements


def compare_sorting_algorithms(data_type: str):
    # Gathers data based on the specified domain
    data = gatherData(data_type)
    
    # Makes a copy of data for fair comparison
    data_quick_sort = data.copy()
    data_bubble_sort = data.copy()
    
    # Measures Quick Sort
    _, quick_sort_time = quickSort(data_quick_sort)
    print(f"Quick Sort time for {data_type}: {quick_sort_time:.6f} seconds")

    # Measures Bubble Sort
    _, bubble_sort_time = bubbleSort(data_bubble_sort)
    print(f"Bubble Sort time for {data_type}: {bubble_sort_time:.6f} seconds")

    # Calculates the difference in time
    time_difference = quick_sort_time - bubble_sort_time
    if time_difference < 0:
        print(f"Quick Sort is faster by {-time_difference:.6f} seconds")
    else:
        print(f"Bubble Sort is faster by {time_difference:.6f} seconds")


def visual_compare_sorting_algorithms(data_types: List[str]):
    # Initializes lists to store the sorting times
    quick_sort_times = []
    bubble_sort_times = []
    labels = []

    for data_type in data_types:
        data = gatherData(data_type)
        data_quick_sort = data.copy()
        data_bubble_sort = data.copy()
        
        # Measures Quick Sort- taken from the Quick Sort function
        _, quick_sort_time = quickSort(data_quick_sort)
        
        # Measures Bubble Sort- taken from the Bubble Sort function
        _, bubble_sort_time = bubbleSort(data_bubble_sort)

        # Stores the results for plotting
        quick_sort_times.append(quick_sort_time)
        bubble_sort_times.append(bubble_sort_time)
        labels.append(data_type)

    # Plotting the results
    x = range(len(data_types))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, quick_sort_times, width, label='Quick Sort')
    rects2 = ax.bar([p + width for p in x], bubble_sort_times, width, label='Bubble Sort')

    # Adds some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Seconds')
    ax.set_title('Comparison of Sorting Algorithm Speeds')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels)
    ax.legend()

    # Function to attach a text label above each bar in rects, displaying its height.
    # This helps in quickly seeing the numeric values without needing to estimate from the plot scale
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    # Displays the plot created
    plt.show()

'''
COMMENTS ON THE SORTING ALGORITHMS

The results strongly suggest that Quick Sort is superior in handling larger datasets 
due to its consistent performance and better scalability. While Bubble Sort may be 
used for small datasets or those nearly sorted (where its complexity can approach O(n)), 
its performance on larger, unsorted datasets is impractical. This analysis reinforces the 
importance of choosing the right algorithm based on data size and expected data order to 
optimize performance in real-world applications.
'''

'''Uncomment to print sorted data for each sorting algorithm'''
#print(quickSort(gatherData("num_passengers"))) 
#print(quickSort(gatherData("tips_amounts"))) 
#print(quickSort(gatherData("total_amounts")))
#print(quickSort(gatherData("fare_amounts")))

'''Uncomment to print sorted data for each sorting algorithm'''

#print(bubbleSort(gatherData("num_passengers"))) 
#print(bubbleSort(gatherData("tips_amounts")))
#print(bubbleSort(gatherData("total_amounts")))
#print(bubbleSort(gatherData("fare_amounts")))

'''Uncomment to compare sorting methods for individual data domains'''
#compare_sorting_algorithms("num_passengers")
#compare_sorting_algorithms("tips_amounts")
#compare_sorting_algorithms("total_amounts")
#compare_sorting_algorithms("fare_amounts")

'''Uncomment to compare sorting methods with all data domains'''
#visual_compare_sorting_algorithms(["num_passengers", "tips_amounts", "total_amounts", "fare_amounts"])