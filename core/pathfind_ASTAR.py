import heapq
import core.los as los
import numpy as np
from game_objects.maps import get_maps
import time

def get_point_from_list(point, dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2
    raise ValueError

def heuristic_cost_estimate(point, goal):
    """Euclidean distance heuristic."""
    return los.get_dist_points(point, goal)

def reconstruct_path(came_from, current):
    """Reconstructs the path after reaching the goal."""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def find_shortest_path_astar(start_pos, end_pos, NAV_MESH, walls):
    """
    A* Pathfinding algorithm to find the shortest route using the navmesh points
    """
    # Convert start and end positions to numpy arrays
    s_np = np.array(start_pos)
    e_np = np.array(end_pos)

    # Check if endpoint is already visible from starting point.
    if los.check_los_jit(s_np, e_np, walls[0], walls[1]):
        return [end_pos], False  # Direct path is available

    # Step 1: Create dictionaries to hold data for distances to start and end
    dist_start = {}
    dist_end = {}

    # Step 2: Get distances from start to all nav points, and from end to all nav points
    for nav_point in NAV_MESH:
        point = nav_point["point"]
        dist_start[los.get_dist_points(start_pos, point)] = nav_point
        dist_end[los.get_dist_points(end_pos, point)] = nav_point

    # Step 3: Find visible start and end points in NAV_MESH
    start_nav_point = None
    end_nav_point = None

    # Find the closest nav point to the start and end positions that has line-of-sight visibility
    for x in sorted(dist_start):
        if los.check_los_jit(s_np, np.array(dist_start[x]["point"]), walls[0], walls[1]):
            start_nav_point = dist_start[x]
            break

    for x in sorted(dist_end):
        if los.check_los_jit(e_np, np.array(dist_end[x]["point"]), walls[0], walls[1]):
            end_nav_point = dist_end[x]
            break

    # If no valid start or end nav points are found, return failure
    if not start_nav_point or not end_nav_point:
        return [end_pos], False

    # Step 4: Initialize open and closed sets (using a priority queue for open set)
    open_set = []
    heapq.heappush(open_set, (0, start_nav_point["point"]))  # (f-cost, point)
    
    came_from = {}  # To reconstruct the path

    # g-scores (cost from start to a point)
    g_score = {tuple(start_nav_point["point"]): 0}
    
    # f-scores (g-score + heuristic estimate to goal)
    f_score = {tuple(start_nav_point["point"]): heuristic_cost_estimate(start_nav_point["point"], end_pos)}

    closed_set = set()

    # Step 5: A* main loop
    while open_set:
        current_f, current_point = heapq.heappop(open_set)
        current_tuple = tuple(current_point)

        # If we reach the goal, reconstruct the path
        if current_tuple == tuple(end_nav_point["point"]):
            return reconstruct_path(came_from, current_tuple), False

        # Add the current point to the closed set
        closed_set.add(current_tuple)

        # Step 6: Explore the neighbors (connected points)
        current_point_data = get_point_from_list(current_point, NAV_MESH)
        for neighbor_point in current_point_data["connected"]:
            neighbor_tuple = tuple(neighbor_point)

            if neighbor_tuple in closed_set:
                continue  # Skip neighbors already in the closed set

            tentative_g_score = g_score[current_tuple] + los.get_dist_points(current_point, neighbor_point)

            if neighbor_tuple not in g_score or tentative_g_score < g_score[neighbor_tuple]:
                # This path to neighbor is better than previous one
                came_from[neighbor_tuple] = current_tuple
                g_score[neighbor_tuple] = tentative_g_score
                f_score[neighbor_tuple] = tentative_g_score + heuristic_cost_estimate(neighbor_point, end_pos)

                if neighbor_tuple not in [x[1] for x in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor_tuple], neighbor_point))

    # If we exhaust the open set without finding a path, return failure
    return [end_pos], False

# Example usage:
# r, i = find_shortest_path_astar(start_pos, end_pos, NAV_MESH, [walls_array_los, walls_array_no_los])
