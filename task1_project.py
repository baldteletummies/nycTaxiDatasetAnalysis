# Luiss - Management and Computer Science - Algorithm 2022/2023 
# Please fill the empty parts with your solution
from typing import Tuple, List, Dict
import csv

def read_file(file_path: str) -> any:
    """
    This function reads the dataset containg all the information about the 
    trips. The information are stored in a .txt file.
    
    Parameters:
    :file_path: The current path where the file you want to read is located
    
    @return: A data structure containing the information from the original data
    """

    # TODO: Implement here your solution
   
    with open(file_path, "r") as dataset:
        #Initilaize 'csv.DictReader' that converts every line into a dict.
        #Keys of the dict are obtained from the first row
        csv_reader = csv.DictReader(dataset) 
        #List comperhension
        #each row is added to the list 'data' as a dictionary.
        data = [row for row in csv_reader]
    return data



def calculate_stats(data: List[Tuple[int, float, float, float]]) -> Tuple[float, float, float]:
    """
    This function calculates the minimum, maximum, and average values for the number of passengers, fare amount,
    total amount, and tips amount.
    
    Parameters:
    :data: The data structure used to calculate the statistics. It is a list of tuples, where each tuple contains
        the number of passengers, fare amount, total amount, and tips amount.
        An int representing the number of passengers,
        A float representing the fare amount,
        Another float representing the total amount, and
        A float representing the tips amount.
    If any error occurs, return the default value (0.0, 0.0, 0.0)
    @return: A tuple containing the minimum, maximum, and average values for the specified statistics in $ where needed.
    """
    #TODO: Implement here your solution
    #Initialize a dictionary for specified fields
    stats = {
        "passenger_count": {"min": float('inf'), "max": float('-inf'), "sum": 0, "count": 0},
        "fare_amount": {"min": float('inf'), "max": float('-inf'), "sum": 0, "count": 0},
        "total_amount": {"min": float('inf'), "max": float('-inf'), "sum": 0, "count": 0},
        "tip_amount": {"min": float('inf'), "max": float('-inf'), "sum": 0, "count": 0},
    }
    #Double for loop for each row and each key in the dataset
    for row in data:
        for key in stats.keys():
            try:
                #Attempt
                #Convert current value on the row to a float 
                value = float(row[key])
                #Update min and  max
                stats[key]["min"] = min(stats[key]["min"], value)
                stats[key]["max"] = max(stats[key]["max"], value)
                #Increment the sum and count for the key by the current value and 1
                stats[key]["sum"] += value
                stats[key]["count"] += 1
                 # In case of error (if conversion to float fails) skip value and continue with the next
            except ValueError:
                continue  

    #Once all rows have been processed, iterate through the keys in stats again
    for key in stats.keys():
        #If the count for the key is greater than 0, calculate the average
        if stats[key]["count"] > 0:
            avg = stats[key]["sum"] / stats[key]["count"]
            #Update the stats dictionary for the key
            stats[key] = {"min": stats[key]["min"], "max": stats[key]["max"], "avg": avg}
        else:
            #Set min, max, and avg to 0.0, indicating no valid entries were found
            stats[key] = {"min": 0.0, "max": 0.0, "avg": 0.0}
    #Return the updated stats dictionary
    return stats


#Create a function that calculate the speed of a trip in Kmh and calculate same metrics as before
from datetime import datetime

def calculate_speed(data: List[Tuple[str, str, float]]) -> Tuple[float, float, float]:
    """
    This function calculates the minimum, maximum, and average speed of trips.
    
    Parameters:
    :data: The data structure used to calculate the statistics. It is a list of tuples, where each tuple contains
        the pickup timestamp, dropoff timestamp, and distance of the trip in miles.
    
    @return: A tuple containing the minimum, maximum, and average speed for the trips in kmh.
    """
    #Initializing list
    speeds = [] 
    
    for trip in data:
        #Parse pick up and drop off times
        pickup_time = datetime.strptime(trip['tpep_pickup_datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        dropoff_time = datetime.strptime(trip['tpep_dropoff_datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        distance_miles = float(trip['trip_distance'])
        
        #Calculating number of hourse from the drop off and pick up times
        duration_hours = (dropoff_time - pickup_time).total_seconds() / 3600
        
        #If the duration of hours is grearter than 0, claculate the distance for km/h
        if duration_hours > 0:
            speed_kmh = (distance_miles * 1.60934) / duration_hours
            speeds.append(speed_kmh)
    
    #Assign variables for print
    #Default values ('0') are allocated to avoid errors
    min_speed = min(speeds) if speeds else 0
    max_speed = max(speeds) if speeds else 0
    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    
    return "min speed:",min_speed, "max speed:",max_speed, "avg speed:",avg_speed
   

#Count the number of trips outgoing from the following pickup zones: 1 (Newark), 132 (JFK Airport), 74 (East Harlem Manhattan), 43 (Central Park) 
#the zones should be expressed in plain text rather than their codified version, you will have CSV with all the codes and their respective zone
from typing import List, Dict

def count_trips(data: List[int], zones: Dict[int, str]) -> Dict[str, int]:
    
    """
    This function counts the number of trips outgoing from the specified pickup zones.
    
    Parameters:
    :data: The data structure used to calculate the statistics. It is a list of integers, where each integer represents
           the pickup zone ID for a trip.
    :zones: A dictionary containing the mapping between the zone code and the zone name.
    
    @return: A dictionary containing the number of trips for each specified zone name.
    """
    #Initilizing an empty dictionary
    trip_count = {}

    for row in data:
        #Extracting and converting 'PULocationID' into an integer if exists
        zone_id = int(row['PULocationID']) if 'PULocationID' in row and row['PULocationID'].isdigit() else None
        #Check if the extracted zone_id is in the predefined list of zones
        if zone_id in zones:
            #If yes retrieve the zone name using the zone_id from the zones mapping
            zone_name = zones[zone_id]
            # Update the trip count
            #If zone doesn't exist in the dict, add it to the dict and add 1
            #If zone exists, add 1
            trip_count[zone_name] = trip_count.get(zone_name, 0) + 1
    return trip_count
   
file_path = 'nyc_dataset_small.txt'  #Change according to the desired dataset to be analysed

content = read_file(file_path) #Call for read_file

stats = calculate_stats(content) #Call for calculate_stats

speed = calculate_speed(content) #Call for calculate_speed

zone = {
    1: "Newark",
    132: "JFK Airport",
    74: "East Harlem Manhattan",
    43: "Central Park",
} #data for 'zones' @ count_trips
trips = count_trips(content, zone) #Call for count_trips

'''Uncomment to print desired algorithm'''
#print(stats) 
#print(speed)
#print(trips)
