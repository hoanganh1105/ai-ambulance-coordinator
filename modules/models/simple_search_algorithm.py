from modules.models.simple_street_graph import SimpleStreetGraph
import heapq
from typing import Callable

def simple_astar(G: SimpleStreetGraph,
                 source: int,
                 target: int,
                 heuristic: Callable[[dict, dict], float],
                 weight: str
                 ) -> list[int]:
    """
    Thuật toán A* chạy trên SimpleStreetGraph
    
    :param G: SimpleStreetGraph
    :type G: SimpleStreetGraph
    :param source: điểm bắt đầu
    :type source: int
    :param target: điểm kết thúc
    :type target: int
    :param heuristic: hàm heuristic
    :type heuristic: function
    :param weight: Description
    :type weight: str
    :return: Description
    :rtype: list[int]
    """
    # TO DO
    open_set = []
    heapq.heappush(open_set, (0, source))
    came_from = {}
    g_score = {node: float('inf') for node in G._node}
    g_score[source] = 0
    f_score = {node: float('inf') for node in G._node}
    f_score[source] = heuristic(source, target)
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return path[::-1]

        if current in closed_set: continue
        closed_set.add(current)

        for neighbor in G._adj.get(current, {}):
            edges = G._adj[current][neighbor]
            edge_data = next(iter(edges.values())) if edges else {}
            
            cost = edge_data.get(weight, edge_data.get('length', 0))
            
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []