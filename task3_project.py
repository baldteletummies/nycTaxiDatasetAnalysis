import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Function to load and map taxi zone IDs to their names from a CSV file
def load_zone_names(zone_file):
    zone_names = {}
    with open(zone_file, 'r') as f:
        next(f)  # Skip the header line in the CSV file
        for line in f:
            location_id, _, zone, _ = line.strip().split(',')
            zone_names[location_id] = zone  # Map location ID to zone name
    return zone_names

# Function to prepare graph data from trip records
def preparation_data(data_file, zone_file):
    zone_names = load_zone_names(zone_file)  # Load the zone names from the CSV
    graph_data = {}

    with open(data_file, 'r') as f:
        next(f)  # Skip the header line in the CSV file
        for line in f:
            domains = line.strip().split(',')
            pickup_loc = zone_names.get(domains[7], None)  # Get the name of the pickup zone
            dropoff_loc = zone_names.get(domains[8], None)  # Get the name of the dropoff zone

            # If both locations are valid, increment the trip count between them
            if pickup_loc is not None and dropoff_loc is not None:
                if pickup_loc not in graph_data:
                    graph_data[pickup_loc] = {}
                if dropoff_loc not in graph_data[pickup_loc]:
                    graph_data[pickup_loc][dropoff_loc] = 0
                
                graph_data[pickup_loc][dropoff_loc] += 1
    
    return graph_data

# Initialize file paths for the dataset and zone lookup table
data_file = "nyc_dataset_large.txt" #Change to desired file to be analyzed
zone_file = "taxi+_zone_lookup.csv"

# Prepare the data and create a graph
graph_data = preparation_data(data_file, zone_file)
G = nx.Graph()

# Add nodes and edges to the graph based on trip data
for pickup_loc in graph_data:
    G.add_node(pickup_loc)  # Add a node for each pickup location

for pickup_loc, dropoff_data in graph_data.items():
    for dropoff_loc, num_trips in dropoff_data.items():
        G.add_edge(pickup_loc, dropoff_loc, weight=num_trips)  # Add edges weighted by trip counts

'''
The edge widths are scaled based on the relative number of trips, providing visual emphasis on more frequent routes.
Node colors are determined by quartile thresholds based on trip frequencies, offering an intuitive color-coding to 
indicate the volume of trips associated with each node.
'''

# Calculate the total number of trips to scale edge widths
all_trips = sum(d['weight'] for _, _, d in G.edges(data=True))

# Define edge widths based on their relative weights
edge_widths = {(u, v): d['weight'] * 50 / all_trips * 10 for u, v, d in G.edges(data=True)}

# Count trips associated with each node
node_trips = {}
for pickup_loc, dropoff_data in graph_data.items():
    # Aggregate trip counts for pickup locations
    if pickup_loc not in node_trips:
        node_trips[pickup_loc] = sum(dropoff_data.values())
    else:
        node_trips[pickup_loc] += sum(dropoff_data.values())
    
    # Aggregate trip counts for dropoff locations
    for dropoff_loc, num_trips in dropoff_data.items():
        if dropoff_loc not in node_trips:
            node_trips[dropoff_loc] = num_trips
        else:
            node_trips[dropoff_loc] += num_trips

# Identify the range of trip counts to determine color thresholds
min_trips = min(node_trips.values())
max_trips = max(node_trips.values())
q1_threshold = int(round(min_trips + (max_trips - min_trips) * 0.25))
q2_threshold = int(round(min_trips + (max_trips - min_trips) * 0.5))
q3_threshold = int(round(min_trips + (max_trips - min_trips) * 0.75))

# Assign colors to nodes based on the number of trips
node_colors = {}
for node, trips in node_trips.items():
    if trips <= q1_threshold:
        node_colors[node] = 'yellowgreen'
    elif trips <= q2_threshold:
        node_colors[node] = 'green'
    elif trips <= q3_threshold:
        node_colors[node] = 'blue'
    else:
        node_colors[node] = 'purple'
        
# Choose a layout algorithm for positioning nodes
pos = nx.kamada_kawai_layout(G)

# Plotting the graph with colored nodes according to trip counts
plt.figure(figsize=(12, 8))  # Set the size of the figure
nx.draw(G, pos, with_labels=False, node_size=200, node_color=[node_colors[node] for node in G.nodes()], font_size=6, font_weight="bold", width=[edge_widths[edge] for edge in G.edges()])

# Add a legend to help identify color ranges
legend_handles = [
    mpatches.Patch(color='yellowgreen', label=f'Q1 ({min_trips:.0f}-{q1_threshold:.0f})'),
    mpatches.Patch(color='green', label=f'Q2 ({q1_threshold:.0f}-{q2_threshold:.0f})'),
    mpatches.Patch(color='blue', label=f'Q3 ({q2_threshold:.0f}-{q3_threshold:.0f})'),
    mpatches.Patch(color='purple', label=f'Q4 ({q3_threshold:.0f}-{max_trips:.0f})')
]
plt.legend(handles=legend_handles, loc='upper left')
plt.show()

def find_connected_components(G):
    """
    Finds and prints the connected components of the given graph 
    """
    # Since the graph is directed by default, converts it to undirected for finding connected components
    undirected_G = G.to_undirected()
    # Finding connected components
    components = list(nx.connected_components(undirected_G))
    return components

# Assuming 'G' is the graph created previously
components = find_connected_components(G)
print("Connected Components:")
for i, component in enumerate(components, 1):
    print(f"Component {i}: {component}")
