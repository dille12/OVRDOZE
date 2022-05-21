def get_complete_routes(routes, end_nav_point, NAV_MESH):
    complete_routes = []
    while routes != []:
        route = routes[0]
        routes.remove(route)
        point = route[-1]
        #point_2 = get_point_from_list(point, NAV_MESH)

        for point_2 in NAV_MESH:
            if point == point_2["point"]:
                break



        if end_nav_point["point"] in point_2["connected"]:
            route.append(end_nav_point["point"])
            complete_routes.append(route)

        else:
            for point_3 in point_2["connected"]:
                if point_3 in route:
                    continue
                if route.copy() + [point_3] in routes:
                    continue
                routes.append(route.copy() + [point_3])

    return complete_routes