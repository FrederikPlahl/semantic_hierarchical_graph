from typing import Dict, List, Optional
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from semantic_hierarchical_graph.node import SHNode
import semantic_hierarchical_graph.utils as util


def draw_child_graph(parent_node: SHNode, path: Optional[Dict] = None, is_leaf: bool = False, view_axis: str = "z"):
    graph: nx.Graph = parent_node.leaf_graph if is_leaf else parent_node.child_graph  # type: ignore

    view = {"x": 0, "y": 1, "z": 2}
    view.pop(view_axis)
    pos_index = list(view.values())
    pos_dict = {node: (node.pos_abs[pos_index[0]], node.pos_abs[pos_index[1]])  # type: ignore
                for node in graph.nodes()}

    if path is not None:
        path_list = util.path_to_list(path, parent_node.hierarchy, is_leaf=is_leaf)
        edge_colors = []
        for u, v in graph.edges:
            if u in path_list and v in path_list:
                edge_colors.append('red')
            else:
                edge_colors.append(graph[u][v]["color"])
    else:
        edge_colors = None

    nx.draw(graph,
            pos=pos_dict,
            edge_color=edge_colors,
            labels=nx.get_node_attributes(graph, 'name'),
            with_labels=True)

    plt.show()


def draw_child_graph_3d(parent_node: SHNode, path: Optional[Dict] = None, is_leaf: bool = False):
    graph: nx.Graph = parent_node.leaf_graph if is_leaf else parent_node.child_graph  # type: ignore
    node_xyz = np.array([node.pos_abs for node in graph.nodes()])  # type: ignore
    edge_xyz = np.array([(u.pos_abs, v.pos_abs) for u, v in graph.edges])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(*node_xyz.T, s=100, ec="w")  # type: ignore

    for node in graph.nodes():
        ax.text(node.pos_abs[0], node.pos_abs[1], node.pos_abs[2],  # type: ignore
                node.unique_name, size=9, color='k')  # type: ignore

    for vizedge in edge_xyz:
        ax.plot(*vizedge.T, color="tab:gray")

    if path is not None:
        path_list = util.path_to_list(path, parent_node.hierarchy, is_leaf=is_leaf)
        if len(path_list) > 0:
            path_xyz = np.array([node.pos_abs for node in path_list])
            ax.plot(*path_xyz.T, color="tab:red")

    ax.grid(False)
    # Suppress tick labels
    for dim in (ax.xaxis, ax.yaxis, ax.zaxis):  # type: ignore
        dim.set_ticks([])
    # Set axes labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")  # type: ignore

    fig.tight_layout()
    plt.show()


def plot_times():
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    type = ['recursive', 'leaf graph']
    times = [85.7, 24.3]
    ax.set_ylabel('Time in μs')
    ax.set_title('Time comparison leaf graph vs. H-Graph')
    ax.bar(type, times)
    fig.tight_layout()
    plt.show()
