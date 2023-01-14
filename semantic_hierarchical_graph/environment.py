from typing import Any, List, Union
import numpy as np
import matplotlib.pyplot as plt
from shapely.plotting import plot_polygon, plot_line
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import nearest_points


class Environment():
    def __init__(self, name: Any, limits: np.ndarray):
        self.name = name
        self.limits = limits
        self.scene: List[Polygon] = []
        self.path: List[LineString] = []

    def add_obstacle(self, obstacle):
        self.scene.append(obstacle)

    def add_path(self, path):
        self.path.append(path)

    def point_in_collision(self, pos):
        """
        Return whether a point is
        in collision -> True
        Free -> False
        Touching (same boundary points but no same interior points) is not considered as collision.
        """
        for value in self.scene:
            if value.intersects(Point(pos[0], pos[1])):
                if value.touches(Point(pos[0], pos[1])):
                    return False
                else:
                    return True
        return False

    def line_in_collision(self, start_point: Point, end_point: Point):
        """
        Check whether a line from start_pos to end_pos is colliding.
        Touching (same boundary points but no same interior points) is not considered as collision.
        """
        for value in self.scene:
            if value.intersects(LineString([start_point, end_point])):
                if value.touches(LineString([start_point, end_point])):
                    return False
                else:
                    return True
        return False

    def get_connection(self, point1: Point, point2: Point) -> Union[LineString, None]:
        if self.line_in_collision(point1, point2):
            # print("Connection in collision between", point1, point2)
            return None
        else:
            connection = LineString([point1, point2])
            return connection

    def find_shortest_connection(self, pos):
        """ Find the shortest path from pos to any path that is not in collision """
        if not isinstance(pos, Point):
            point = Point(pos[0], pos[1])
        closest_path = min(self.path, key=lambda x: x.distance(point))
        closest_point: Point = nearest_points(closest_path, point)[0]
        return self.get_connection(closest_point, point)

    def find_all_shortest_connections(self):
        """ Find all shortest connections between all shapes in path that are not in collision """
        new_connections = []
        for path in self.path:
            # print("Path: ", path)
            rest_path = list(self.path)
            # for exclude_path in exclude:
            rest_path.remove(path)
            if len(rest_path) == 0:
                return new_connections
            for other_path in rest_path:
                # print("Other path: ", other_path)
                closest_point_path = Point(min(path.coords, key=lambda x: other_path.distance(Point(x[0], x[1]))))
                # print("Closest point path: ", closest_point_path)
                closest_point_other_path: Point = nearest_points(other_path, closest_point_path)[0]
                # print("Closest point other path: ", closest_point_other_path)
                connection = self.get_connection(closest_point_path, closest_point_other_path)
                if connection is not None:
                    new_connections.append(connection)

        return new_connections

    def clear_bridge_nodes(self, bridge_points: List):
        walls = self.scene[0]
        for point in bridge_points:
            self.scene[0] = walls.difference(Point(point).buffer(2))

    def clear_bridge_edges(self, bridge_edges: List):
        walls = self.scene[0]
        for edge in bridge_edges:
            self.scene[0] = walls.difference(LineString(edge).buffer(2, cap_style="flat"))

    def plot(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.invert_yaxis()
        ax.set_aspect("equal")
        for value in self.scene:
            plot_polygon(value, ax=ax, add_points=False, color="red", alpha=0.8)

        for value in self.path:
            plot_line(value, ax=ax, add_points=False, color="blue", alpha=0.8)

        plt.show()
