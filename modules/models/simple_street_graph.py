class SimpleStreetGraph:
    """
    A minimal directed multigraph for modeling states with spatial coordinates.
    """
    def __init__(self):
        """
        Internal data structures:
        - self._nodes: {node_id: {attributes}}
        {attributes} ít nhất phải có 'x' and 'y' (toạ độ)
        node_id phải là int
        - self._adj: {u: {v: {key: {attributes}}}}
        {attributes} ít nhất phải có 'length' và 'highway'
        u, v là id của node, key phải là int
        """
        self._nodes = {}
        self._adj = {} 
        # Có thể định nghĩa thêm các attribute khác.

    # ---------- Data Ingestion ----------
    def add_node(self, n: int, **attrs):
        """
        Thêm node.
        :param n: node muốn thêm vào.
        :type n: int
        :param attrs: attribute của node
        """
        # TO DO

    def add_edge(self, u: int, v: int, key: int = None, **attrs):
        """
        Thêm cạnh.
        :param u: cạnh bắt đầu
        :type u: int
        :param v: cạnh kết thúc
        :type v: int
        :param key: key của cạnh. Nếu đã tồn tại thì ghi đè, nếu là None thì tạo cạnh với key mới.
        :type key: int
        :param attrs: attribute của cạnh
        """
        # TO DO

    # ---------- Other ----------
    # Có thể định nghĩa thêm property, method...
    def edges(self, nbunch=None, keys=False, data=False):
        """
        Generator trả về edges.
        Mimic NetworkX MultiDiGraph.edges()
        
        :param nbunch: node hoặc list node để query edges từ. Nếu None thì return tất cả edges.
        :type nbunch: int or list[int]
        :param keys: Nếu True thì include key trong output
        :type keys: bool
        :param data: Nếu True thì include edge attributes trong output
        :type data: bool
        :return: generator trả về edges
        
        Examples:
            G.edges()  # (u, v), (u, v), ...
            G.edges(keys=True)  # (u, v, key), (u, v, key), ...
            G.edges(data=True)  # (u, v, {attrs}), (u, v, {attrs}), ...
            G.edges(keys=True, data=True)  # (u, v, key, {attrs}), ...
        """
        if nbunch is None:
            nbunch = self._adj
        
        for u in nbunch:
            if u in self._adj:
                for v in self._adj[u]:
                    for key in self._adj[u][v]:
                        if keys and data:
                            yield (u, v, key, self._adj[u][v][key])
                        elif keys:
                            yield (u, v, key)
                        elif data:
                            yield (u, v, self._adj[u][v][key])
                        else:
                            yield (u, v)
    


def graph_from_place(place_name: str, network_type: str='drive') -> SimpleStreetGraph:
    """
    Create SimpleStreetMap from OSM place name (mimics osmnx.graph_from_place)
    by converting the Multigraph returned by osmnx.graph_from_place into an instance of this class

    :param place_name: Name of place (e.g., 'Manhattan, New York')
    :type place_name: str
    :param network_type: 'drive', 'walk', 'bike', 'all'
    :type network_type: str
    :return: SimpleStreetGraph
    :rtype: SimpleStreetGraph
    """
    # TO DO

def plot_graph_route(G: SimpleStreetGraph, route: list[int] = None, route_color: str = 'r', route_linewidth: float = 4, node_size: float = 15):
    """
    Hiển thị bản đồ, background màu #111111, cạnh màu #999999
    :param G: Đồ thị đường đi
    :type G: SimpleStreetGraph
    :param route: đường đi dạng list id của các node
    :type route: list[int]
    :param route_color: màu sắc highlight route
    :type route_color: str
    :param route_linewidth: độ dày route
    :type route_linewidth: float
    :param node_size: kích thước node
    :type node_size: float
    """
    # TO DO