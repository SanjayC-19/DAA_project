import heapq

class Graph:
    def __init__(self):
        # Initializes an empty dictionary to store nodes and their neighbors with travel times
        self.nodes = {}
    
    def add_edge(self, start, end, time):
        # Adds an edge between two nodes in both directions for an undirected graph
        if start not in self.nodes:
            self.nodes[start] = []
        if end not in self.nodes:
            self.nodes[end] = []
        self.nodes[start].append((end, time))
        self.nodes[end].append((start, time))
    
    def update_traffic(self, start, end, extra_time):
        # Updates the travel time by adding extra time due to traffic conditions
        try:
            # Find the original time for this route
            original_time = next(time for neighbor, time in self.nodes[start] if neighbor == end)
        except StopIteration:
            print(f"No direct route exists between {start} and {end}.")
            return
        
        new_time = original_time + extra_time  # Add extra time to the original time
        
        # Update the time for both directions of the edge (since it's undirected)
        self.nodes[start] = [(neighbor, new_time if neighbor == end else time) for neighbor, time in self.nodes[start]]
        self.nodes[end] = [(neighbor, new_time if neighbor == start else time) for neighbor, time in self.nodes[end]]

    def dijkstra(self, start, end):
        # Uses Dijkstra's algorithm to find the shortest path from start to end
        queue = [(0, start)]  # Priority queue with (current time, node)
        times = {node: float('infinity') for node in self.nodes}  # Start with high travel times
        times[start] = 0  # Travel time to the start node is 0
        shortest_path_tree = {start: None}  # To reconstruct the path
        
        while queue:
            current_time, current_node = heapq.heappop(queue)  # Get node with shortest travel time
            
            if current_node == end:
                break  # Stop if we've reached the destination
            
            for neighbor, time in self.nodes[current_node]:
                travel_time = current_time + time  # Calculate time to neighbor
                
                if travel_time < times[neighbor]:  # Found a quicker path
                    times[neighbor] = travel_time
                    heapq.heappush(queue, (travel_time, neighbor))  # Push to queue with updated travel time
                    shortest_path_tree[neighbor] = current_node  # Record path

        # Reconstruct the shortest path by backtracking from the end node
        path, node = [], end
        while node is not None:
            path.append(node)
            node = shortest_path_tree[node]
        path.reverse()  # Reverse to get path from start to end
        
        return path, times[end]  # Return the path and total travel time

# Define Erode district taluks with approximate travel times (in minutes)
city_graph = Graph()
city_graph.add_edge("Erode", "Bhavani", 16)
city_graph.add_edge("Erode", "Perundurai", 20)
city_graph.add_edge("Erode", "Modakkurichi", 12)
city_graph.add_edge("Bhavani", "Gobichettipalayam", 23)
city_graph.add_edge("Gobichettipalayam", "Sathyamangalam", 30)
city_graph.add_edge("Perundurai", "Kangeyam", 24)
city_graph.add_edge("Modakkurichi", "Kangeyam", 28)

# Function to get user input for taluk names and ensure they are valid
def get_valid_taluk(prompt):
    while True:
        taluk = input(f"{prompt} (Options: {', '.join(city_graph.nodes.keys())}): ").strip().title()  # Standardize input to title case
        if taluk in city_graph.nodes:
            return taluk  # Return if taluk is valid
        else:
            print("Invalid PlaceEr name. Please try again.")

# Get starting and destination taluks from the user
start = get_valid_taluk("Enter the starting Place")
end = get_valid_taluk("Enter the destination Place")

# Find the shortest route and display it
print(f"\nFinding the shortest route from {start} to {end}...")
path, time = city_graph.dijkstra(start, end)
print(f"Path: {' -> '.join(path)} | Estimated travel time: {time} minutes")

# Ask user if they want to simulate traffic changes
update = input("\nDo you want to update traffic on any route? (yes/no): ").strip().lower()
if update == "yes":
    route_start = get_valid_taluk("Enter the starting Place of the route to update")
    route_end = get_valid_taluk("Enter the destination Place of the route to update")
    while True:
        try:
            extra_time = int(input("Enter the extra travel time (in minutes) due to traffic: "))
            if extra_time < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for extra travel time.")
    
    city_graph.update_traffic(route_start, route_end, extra_time)
    
    # Recalculate the shortest route after updating traffic
    print(f"\nUpdated route from {start} to {end} after traffic adjustment...")
    path, time = city_graph.dijkstra(start, end)
    print(f"Path: {' -> '.join(path)} | Estimated travel time: {time} minutes")
