import core.los as los
from game_objects.maps import get_maps
import numpy as np
import time
if __name__ == '__main__':
    maps = get_maps(None)
    errors = 0
    for map in maps:
        walls = map.generate_wall_structure2()
        map.generate_numpy_wall_points()
        NAV_MESH = map.read_navmesh(walls)
        map.compile_navmesh(1)
        loops = 1000

        for i in range(loops):


            point1, point2 = map.get_random_point(), map.get_random_point()
            t = time.perf_counter()
            res = los.check_los_jit(point1, point2, map.numpy_array_wall_los)
            delta = time.perf_counter() - t
            print(f"JIT RESULT: {res} Time: {delta*1000:.2f}ms", )

            t = time.perf_counter()
            res2 = los.check_los(point1, point2, walls)
            delta = time.perf_counter() - t
            print(f"NORMAL RESULT: {res2} Time: {delta*1000:.2f}ms", )

            if res != res:
                errors += 1

    print("Errors:", errors)
