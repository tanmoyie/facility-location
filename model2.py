"""

"""

import numpy as np


def solve(facility):
    # Take each of 5 warehouse lat and lon
    cor2 = []
    for i in range(len(facility)):
        lat = facility["latitude"][i]
        lon = facility["longitude"][i]
        cor2.append([lon, lat])

        points = [tuple(x) for x in cor2]

        lon = np.array([point[0] for point in points])
        lat = np.array([point[1] for point in points])

        def weiszfeld(points):

            max_error = 0.0000000001

            lon = np.array([point[0] for point in points])
            lat = np.array([point[1] for point in points])

            ext_condition = True

            start_x = np.average(lon)
            start_y = np.average(lat)

            while ext_condition:
                sod = (((lon - start_x) ** 2) + ((lat - start_y) ** 2)) ** 0.5

                new_x = sum(lon / sod) / sum(1 / sod)
                new_y = sum(lat / sod) / sum(1 / sod)

                ext_condition = (abs(new_x - start_x) > max_error) or (abs(new_y - start_y) > max_error)

                start_y = new_y
                start_x = new_x

                print(new_x, new_y)

            return ...

        # it's an iterative proces and last one is the final coordinate where we will cite new warehouse
        if __name__ == "__main__":
            weiszfeld(points)
