
import core.classes as classes
import core.los as los

from game_objects.maps import get_maps
import time
from core.pathfind_ASTAR import find_shortest_path_astar
from core.pathfind import find_shortest_path
import numpy as np
if __name__ == '__main__':
    maps = get_maps(None)
    total = 0
    longest = 0
    total_loops = 0
    first = True
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

        loops = 250


        print("STATRING CALC")

        for i in range(loops):
            print("New calc")
            total_loops += 1
            point1, point2 = map.get_random_point(), map.get_random_point()
            print("Start", point1, "End", point2)
            #print("FROM", point1, "TO", point2)
            t = time.perf_counter()
            r, i = find_shortest_path_astar(point1, point2, NAV_MESH, [map.numpy_array_wall_los, map.numpy_array_wall_no_los])
            #print(r)
            elapsed = time.perf_counter() - t
            if first:
                elapsed = 0
                first = False
            #print("Time elapsed:", elapsed)
            total += elapsed
            map.total += elapsed
            
            if not r:
                map.total_error += 1
            else:
                l = r[0]
                for x in r:
                    if not los.check_los_jit(np.array(l), np.array(x), map.numpy_array_wall_los):
                        map.total_error += 1
                        print("ROUTE ERROR", x, l, "not connected")
                        break
                    l = x
            longest = max([longest, elapsed])
            if longest == elapsed:
                longest_points = [point1, point2, NAV_MESH, [map.numpy_array_wall_los, map.numpy_array_wall_no_los]]

        print("MAP TOTAL:", map.total)

    print(f"AVERAGE TIME: {total/(total_loops)*1000:.2f}ms, ({(total/(total_loops))/(1/60):.2f} frames on 60fps)")
    for i in maps:
        print(f"{i.name} : {i.total}, ERRORS: {i.total_error/loops * 100:.2f}% ({i.total/loops*1000:.2f}ms per route)")

    print("WORST PERFORMING MAP:", sorted(maps, key=lambda x: x.total, reverse = True)[0].name, "\n\n\n\n")
    print("LONGEST CALC:", longest, "calculating again...")
    print(longest_points[:2])
    t = time.perf_counter()
    print(find_shortest_path_astar(longest_points[0], longest_points[1], longest_points[2], longest_points[3]))
    elapsed = time.perf_counter() - t
    print("Time elapsed:", elapsed)