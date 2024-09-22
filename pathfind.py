import los
import time
import random
import numpy as np

def get_point_from_list(point, dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2
    raise ValueError

def recoursive_line_iteration(route, from_point, to_point, dict, end_nav_point):

    if route[-1] in end_nav_point["connected"]:
        return
    if len(to_point["connected"]) == 2:
        for p in (p for p in to_point["connected"] if p not in route):
            route.append(p)
            recoursive_line_iteration(route, to_point, get_point_from_list(p, dict), dict, end_nav_point)



# nav_test = [
#                 {"point" : [1,1], "connected" : [ [2, 1] ] },
#                 {"point" : [2, 1], "connected" : [ [1, 1], [3, 1] ] },
#                 {"point" : [3, 1], "connected" : [ [2, 1], [3, 2], [4, 1] ] },
#                 {"point" : [4, 1], "connected" : [ [3, 1] ] },
#                 {"point" : [3, 2], "connected" : [ [3, 1]]}
#             ]
#
# route = [[1,1], [2,1]]
# recoursive_line_iteration(route, get_point_from_list([1,1], nav_test), get_point_from_list([2,1], nav_test), nav_test)
# print(route)
# input()

def get_closest_route_to_finish_point(routes, end_point):
    closest = None
    closest_dist = 99999
    for x in routes:
        d = los.get_dist_points(x[-1], end_point)
        if d < closest_dist:
            closest_dist = d
            closest = x
    return closest



def find_shortest_path(start_pos, end_pos, NAV_MESH, walls, quick=True, cache = False):
    """
    Calculates the shortest route to a point using the navmesh points
    """
    t = time.perf_counter()

    s_np = np.array(start_pos)
    e_np = np.array(end_pos)

    if los.check_los_jit(s_np, e_np, walls[0], walls[1]):  #Check if endpoint is already visible from starting point.
        return [end_pos], False #Returns just endpoint
    dist_start = {}
    dist_end = {}
    for nav_point in NAV_MESH:  #Every nav_point is a dictionary of the point and which points are connected ie.
        point = nav_point["point"] #{"point" : [100,100], "connected" : [200,200], [300, 100]}
        dist_start[los.get_dist_points(start_pos, point)] = nav_point #Get distances to all points from starting point
        dist_end[los.get_dist_points(end_pos, point)] = nav_point #Get distances to all points from ending point

    start_nav_point = False
    end_nav_point = False

    try:
        for x in sorted(dist_start):
            if los.check_los_jit(s_np, np.array(dist_start[x]["point"]), walls[0], walls[1]):  #Get closest visible starting nav point.
                start_nav_point = dist_start[x]
                break
        for x in sorted(dist_end):
            if los.check_los_jit(e_np, np.array(dist_end[x]["point"]), walls[0], walls[1]): #Get closest visible ending nav point from route ending point.
                end_nav_point = dist_end[x]
                break
    except Exception as e:
        print(e)
        return [end_pos], False # if none are visible, return nothing

    if not start_nav_point or not end_nav_point:
        return [end_pos], False # if none are visible, return nothing

    complete_routes = []
    routes = []
    routes_end_points = []
    for conne in start_nav_point["connected"]:
        routes.append([start_nav_point["point"], conne]) # init loop with all connected points from start point
        routes_end_points.append(conne)

    max_len = round(len(NAV_MESH)/2 + 2) # Maximum route length
    routes_max = 0


    while routes != []:
        if len(complete_routes) > 0: #Break loop once two complete routes have been found
            break

        # if time.perf_counter() - t > 0.1: # Return error if routes can't be found in one second
        #     return False, False

        route = get_closest_route_to_finish_point(routes, end_nav_point["point"]) # Get a random choice from incomplete routes

        routes.remove(route)
        #print("Distance to end:", los.get_dist_points(route[-1], end_nav_point["point"]))
         # Remove it from the list
        if route[-1] in routes_end_points: # Remove routes end point from a list that keeps track of routes' ending points.
            routes_end_points.remove(route[-1]) #This prevents duplicate routes.
        routes_max = max([routes_max, len(routes)]) # For debugging purposes keep track how many incomplete routes are there.
        if len(route) >= max_len: # If route exceeds maximum route length, kill route.
            continue
        point = route[-1]
        point_2 = get_point_from_list(point, NAV_MESH) # Get routes last point from navmesh.
        if end_nav_point["point"] is point_2["point"]: # Check if ending point is connected to route.
            complete_routes.append(route) # Complete route
            continue
        if end_nav_point["point"] in point_2["connected"]: # Check if ending point is connected to route.
            route.append(end_nav_point["point"])
            complete_routes.append(route) # Complete route
            continue




        else: # Ending point is not connected to the route
            for point_3 in point_2["connected"]: # Generate new routes from connected points
                route_copy = route.copy()
                if point_3 in route: # Check point is in the route already.
                    continue
                if route.copy() + [point_3] in routes: # Check if a route exists already.
                    continue

                good_point = True
                if point_3 in routes_end_points: # Check if there is a route that ends in this point already.
                    for route_2 in (route_2 for route_2 in routes if route_2[-1] == point_3): # Get all routes that end here
                        if len(route) + 1 >= len(route_2): # If current route is longer than the existing route, skip current route.
                            good_point = False
                            break
                        else:
                            routes.remove(route_2) # kill the existing route and replace it with shorter current one.

                if good_point:

                    route_copy.append(point_3)
                    recoursive_line_iteration(route_copy, get_point_from_list(route[-1], NAV_MESH), get_point_from_list(point_3, NAV_MESH), NAV_MESH, end_nav_point)
                    if route_copy[-1] is end_nav_point["point"]:
                        complete_route.append(route_copy)
                    elif route_copy not in routes:
                        routes_end_points.append(route_copy[-1]) # Add the ending point to the list that keeps track of ending points.
                        routes.append(route_copy)
    shortest_route = {"dist": 100000, "route": []} # Init computing the shortest route.

    if not routes and not complete_routes:
        print("NOTHING FOUND")



    for route in complete_routes:
        route_ref = {"dist": 0, "route": route}
        last_pos = start_pos
        for point in route: # compute the distance of all points in the route
            route_ref["dist"] += los.get_dist_points(last_pos, point)

        if route_ref["dist"] < shortest_route["dist"]: # if route is shorter than the currently shortest one, replace it.
            shortest_route = route_ref
            shortest_route["route"].append(end_pos)

    if cache: # For debugging, keeps track of calculating times
        cache.path_times["calc"][0] += 1
        cache.path_times["calc"][1] += time.perf_counter() - t
        cache.path_times["max"] = max([cache.path_times["max"], time.perf_counter() - t])

    return shortest_route["route"], False

if __name__ == '__main__':
    maps = get_maps(None)
    total = 0
    longest = 0
    total_loops = 0
    for map in maps:

        # if map.name != "Downtown":
        #     continue

        walls = map.generate_wall_structure2()
        map.generate_numpy_wall_points()
        no_los_walls = map.no_los_walls
        print(no_los_walls)
        NAV_MESH = map.read_navmesh(walls)
        print("navmesh:", NAV_MESH)
        map.compile_navmesh(1)

        loops = 2500


        print("STATRING CALC")

        for i in range(loops):
            print("New calc")
            total_loops += 1
            point1, point2 = map.get_random_point(), map.get_random_point()
            print("Start", point1, "End", point2)
            #print("FROM", point1, "TO", point2)
            t = time.perf_counter()
            r, i = find_shortest_path(point1, point2, NAV_MESH, [map.numpy_array_wall_los, map.numpy_array_wall_no_los])
            #print(r)
            elapsed = time.perf_counter() - t
            #print("Time elapsed:", elapsed)
            total += elapsed
            map.total += elapsed
            if not r:
                map.total_error += 1
            longest = max([longest, elapsed])
            longest_points = [point1, point2]

        print("MAP TOTAL:", map.total)

    print(f"AVERAGE TIME: {total/(total_loops)*1000:.2f}ms, ({(total/(total_loops))/(1/60):.2f} frames on 60fps)")
    for i in maps:
        print(f"{i.name} : {i.total}, ERRORS: {i.total_error/loops * 100:.2f}% ({i.total/loops*1000:.2f}ms per route)")

    print("WORST PERFORMING MAP:", sorted(maps, key=lambda x: x.total, reverse = True)[0].name, "\n\n\n\n")
    print("LONGEST CALC:", longest, "calculating again...")
    print(longest_points)
    t = time.perf_counter()
    print(find_shortest_path(longest_points[0], longest_points[1], NAV_MESH, [map.numpy_array_wall_los, map.numpy_array_wall_no_los]))
    elapsed = time.perf_counter() - t
    print("Time elapsed:", elapsed)
