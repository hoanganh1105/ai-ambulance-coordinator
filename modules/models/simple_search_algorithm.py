from simple_street_graph import SimpleStreetGraph

def simple_astar(G: SimpleStreetGraph,
                 source: int,
                 target: int,
                 heuristic: function,
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