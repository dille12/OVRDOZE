import los
from maps import get_maps
import time
import random

def get_point_from_list(point, dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2


def find_shortest_path(start_pos, end_pos, NAV_MESH, walls, quick=True, cache = False):
    """
    Calculates the shortest route to a point using the navmesh points
    """

    t = time.perf_counter()

    if los.check_los(start_pos, end_pos, walls):  #Check if endpoint is already visible from starting point.
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
            if los.check_los(start_pos, dist_start[x]["point"], walls):  #Get closest visible starting nav point.
                start_nav_point = dist_start[x]
                break
        for x in sorted(dist_end):
            if los.check_los(end_pos, dist_end[x]["point"], walls): #Get closest visible ending nav point from route ending point.
                end_nav_point = dist_end[x]
                break
    except Exception as e:
        print(e)
        return [end_pos], False # if none are visible, return nothing

    if not start_nav_point or not end_nav_point:
        return [end_pos], False # if none are visible, return nothing


    complete_routes = []
    routes = []
    for conne in start_nav_point["connected"]:
        routes.append([start_nav_point["point"], conne]) # init loop with all connected points from start point

    max_len = round(len(NAV_MESH)/2 + 2) # Maximum route length
    routes_max = 0
    routes_end_points = []
    while routes != []:
        if len(complete_routes) > 1: #Break loop once two complete routes have been found
            break

        if time.perf_counter() - t > 1: # Return error if routes can't be found in one second
            return False, False

        route = random.choice(routes) # Get a random choice from incomplete routes
        routes.remove(route) # Remove it from the list
        if route[-1] in routes_end_points: # Remove routes end point from a list that keeps track of routes' ending points.
            routes_end_points.remove(route[-1]) #This prevents duplicate routes.
        routes_max = max([routes_max, len(routes)]) # For debugging purposes keep track how many incomplete routes are there.
        if len(route) >= max_len: # If route exceeds maximum route length, kill route.
            continue
        point = route[-1]
        point_2 = get_point_from_list(point, NAV_MESH) # Get routes last point from navmesh.
        if end_nav_point["point"] in point_2["connected"]: # Check if ending point is connected to route.
            route.append(end_nav_point["point"])
            complete_routes.append(route) # Complete route
            routes_end_points.clear()


        else: # Ending point is not connected to the route
            for point_3 in point_2["connected"]: # Generate new routes from connected points
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
                    routes.append(route.copy() + [point_3]) # Append the route to the list of routes
                    routes_end_points.append(point_3) # Add the ending point to the list that keeps track of ending points.


    shortest_route = {"dist": 10000, "route": []} # Init computing the shortest route.



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
    for map in maps:
        walls = map.generate_wall_structure2()
        NAV_MESH = map.read_navmesh(walls)
        print("navmesh:", NAV_MESH)
        map.compile_navmesh(1)

        loops = 2500

        for i in range(loops):
            point1, point2 = map.get_random_point(walls), map.get_random_point(walls)
            #print("FROM", point1, "TO", point2)
            t = time.perf_counter()
            r, i = find_shortest_path(point1, point2, NAV_MESH, walls)
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

        print(f"AVERAGE TIME: {total/(loops*len(maps))*1000:.2f}ms, ({(total/(loops*len(maps)))/(1/60):.2f} frames on 60fps)")
        for i in maps:
            print(f"{i.name} : {i.total}, ERRORS: {i.total_error} ({i.total/2.5:.2f}ms per route)")

        print("WORST PERFORMING MAP:", sorted(maps, key=lambda x: x.total, reverse = True)[0].name)
        print("LONGEST CALC:", longest, "calculating again...")
        print(longest_points)
        t = time.perf_counter()
        print(find_shortest_path(longest_points[0], longest_points[1], NAV_MESH, walls))
        elapsed = time.perf_counter() - t
        print("Time elapsed:", elapsed)
