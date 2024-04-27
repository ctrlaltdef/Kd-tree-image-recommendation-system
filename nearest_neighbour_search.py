from math import sqrt
from rgb_to_hue import rgb_to_hue
from saturation import saturation
from value import*
# Function to calculate the Euclidean distance between two points in RGB space

def distance(point1, point2):
    r1, g1, b1 = point1
    r2, g2, b2 = point2
    return sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
# Function to perform nearest neighbor search
def nearest_neighbor_search(root, query_color, k=10, value_tolerance=30, hue_tolerance=30, saturation_tolerance=30):
    # Function to update the list of best neighbors with a new point
   
    def update_best_neighbors(best_neighbors, new_point, query_color, k, value_tolerance, hue_tolerance, saturation_tolerance):
        # Update the list of best neighbors with the new_point if it is closer to the query color
        filename, color = new_point  # Unpack the filename and color tuple
        
        # Calculate the distance between the query color and the new point
        distance_new = distance(query_color, color)
        
        
        # Calculate the difference between query and new point for hue, saturation and value
        hue_diff = abs(query_color[0] - color[0])
        saturation_diff=abs(query_color[1]-color[1])
        value_diff=abs(query_color[2]-color[2])

        # Check if both RGB differences and hue difference are within tolerances
        if (hue_diff <= hue_tolerance) and (saturation_diff<=saturation_tolerance) and (value_diff<=value_tolerance):
            # Find the position to insert the new point in the list
            i = 0
            while i < len(best_neighbors) and distance(query_color, best_neighbors[i][1]) < distance_new:
                i += 1
            
            # Insert the new point in the correct position
            best_neighbors.insert(i, new_point)
            
            # Keep only the top k neighbors
            if len(best_neighbors) > k:
                best_neighbors.pop()
            
        return best_neighbors
        # Recursive function to perform nearest neighbor search
    def nearest_neighbor_rec(node, query_color, k, best_neighbors, axis=0):
        if node is None:
            return best_neighbors
        
        # Update the best neighbors list with the current node's point and filename
        best_neighbors = update_best_neighbors(best_neighbors, (node['filename'], node['point']), query_color, k, value_tolerance, hue_tolerance, saturation_tolerance)
        
        # Choose the axis for the next level
        new_axis = (axis + 1) % len(query_color)
        
        # Recursively explore the appropriate subtrees based on the query color
        if query_color[axis] < node['point'][axis]:
            best_neighbors = nearest_neighbor_rec(node['left'], query_color, k, best_neighbors, new_axis)
        else:
            best_neighbors = nearest_neighbor_rec(node['right'], query_color, k, best_neighbors, new_axis)
        
        # Check if need to explore the other side of the tree
        if best_neighbors and abs(node['point'][axis] - query_color[axis]) < distance(query_color, best_neighbors[-1][1]):
            if query_color[axis] < node['point'][axis]:
                best_neighbors = nearest_neighbor_rec(node['right'], query_color, k, best_neighbors, new_axis)
            else:
                best_neighbors = nearest_neighbor_rec(node['left'], query_color, k, best_neighbors, new_axis)
        
        return best_neighbors
    # Start the nearest neighbor search from the root of the tree
    return nearest_neighbor_rec(root, query_color, k, [])